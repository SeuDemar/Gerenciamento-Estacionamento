import datetime

class ParkingManager:
    def __init__(self):
        self.parked_cars = self.carregar_exemplos()

    def carregar_exemplos(self):
        # Dados simulando JSON embutido
        dados_json = {
            "ABC1234": "2025-05-12T08:30:00",
            "XYZ5678": "2025-05-12T09:45:00"
        }

        # Converte strings para objetos datetime
        return {
            placa: datetime.datetime.fromisoformat(hora)
            for placa, hora in dados_json.items()
        }

    def park_car(self, license_plate):
        if license_plate in self.parked_cars:
            return f"Carro com placa {license_plate} ja esta no estacionamento."
        self.parked_cars[license_plate] = datetime.datetime.now()
        return f"Carro com placa {license_plate} estacionado com sucesso."

    def remove_car(self, license_plate):
        if license_plate not in self.parked_cars:
            return f"Carro com placa {license_plate} nao encontrado no estacionamento."
        
        entry_time = self.parked_cars.pop(license_plate)
        exit_time = datetime.datetime.now()

        duration = exit_time - entry_time
        minutes = int(duration.total_seconds() // 60)

        valor_total = self.calcular_valor(minutes)

        horas = minutes // 60
        minutos_restantes = minutes % 60
        tempo_formatado = f"{horas}h {minutos_restantes}min"

        return (
            f"Carro com placa {license_plate} saiu.\n"
            f"Tempo estacionado: {tempo_formatado}\n"
            f"Valor a pagar: R$ {valor_total:.2f}"
        )

    def calcular_valor(self, minutos):
        if minutos <= 120:
            return 0.00
        horas_extras = (minutos - 120 + 59) // 60  # arredonda para cima
        return round(horas_extras * 2.00, 2)

    def list_cars(self):
        if not self.parked_cars:
            return "Estacionamento vazio."
        result = "Carros atualmente no estacionamento:\n"
        for plate, time in self.parked_cars.items():
            entry_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
            duration = datetime.datetime.now() - time
            minutes = int(duration.total_seconds() // 60)
            valor_total = self.calcular_valor(minutes)

            horas = minutes // 60
            minutos_restantes = minutes % 60
            tempo_formatado = f"{horas}h {minutos_restantes}min"

            result += f"  - Placa: {plate}, Estacionado desde: {entry_time_str}\n"
            result += f"    Tempo: {tempo_formatado}\n"
            result += f"    Valor ate agora: R$ {valor_total:.2f}\n"
        return result
