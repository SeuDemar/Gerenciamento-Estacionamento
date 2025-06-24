import datetime
from datetime import timedelta
from carro import Carro
from moto import Moto
from bicicleta import Bicicleta

PRECOS = {
    "CARRO": {
        "manha": 5.0,
        "tarde": 7.0,
        "noite": 10.0,
        "dia": 20.0
    },
    "MOTO": {
        "manha": 3.0,
        "tarde": 4.0,
        "noite": 6.0,
        "dia": 15.0
    },
    "BICICLETA": {
        "fixo": 2.0
    }
}

vagas = {i: None for i in range(1, 6)}

def mostrar_vagas():
    print("\n=== 🅿️ ESTACIONAMENTO ===")
    linha_visual = ""
    for numero, veiculo in vagas.items():
        linha_visual += "[O] " if veiculo else "[ ] "
    print(linha_visual.strip())

    print("\n📋 Detalhes das vagas:")
    for numero, veiculo in vagas.items():
        if veiculo is None:
            print(f"[ ] Vaga {numero} - Livre")
        else:
            print(f"[O] Vaga {numero} - Ocupada por {veiculo}")
    print()

def escolher_tipo_veiculo():
    print("\nTipos de veículo:")
    print("1. Carro")
    print("2. Moto")
    print("3. Bicicleta")
    tipo = input("Escolha o tipo do veículo: ")

    if tipo == "1":
        return Carro
    elif tipo == "2":
        return Moto
    elif tipo == "3":
        return Bicicleta
    else:
        print("🚫 Tipo inválido.")
        return None

def estacionar_veiculo():
    tipo_classe = escolher_tipo_veiculo()
    if tipo_classe is None:
        return

    placa = input("Digite a placa (ou identificador para bicicleta): ").upper()
    for numero, veiculo in vagas.items():
        if veiculo is None:
            vagas[numero] = tipo_classe(placa)
            print(f"✅ Veículo {placa} estacionado na vaga {numero}.")
            return
    print("🚫 Estacionamento cheio!")


def calcular_preco_veiculo(veiculo, saida):
    entrada = veiculo.entrada
    tempo = saida - entrada
    minutos = tempo.total_seconds() / 60

    tipo = veiculo.__class__.__name__.upper()

    if tipo == "BICICLETA":
        return PRECOS["BICICLETA"]["fixo"]

    preco = PRECOS[tipo]
    total = 0

    # Dias inteiros
    dias = int(minutos // (24 * 60))
    total += dias * preco["dia"]
    minutos_restantes = minutos % (24 * 60)

    horario_atual = entrada + timedelta(days=dias)

    while minutos_restantes > 0:
        hora = horario_atual.hour

        if 6 <= hora < 12:
            total += preco["manha"]
            proximo = horario_atual.replace(hour=12, minute=0, second=0, microsecond=0)
        elif 12 <= hora < 18:
            total += preco["tarde"]
            proximo = horario_atual.replace(hour=18, minute=0, second=0, microsecond=0)
        else:
            if hora < 6:
                proximo = horario_atual.replace(hour=6, minute=0, second=0, microsecond=0)
            else:
                proximo = (horario_atual + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)

            total += preco["noite"]

        minutos_gastos = (proximo - horario_atual).total_seconds() / 60

        if minutos_gastos > minutos_restantes:
            break

        minutos_restantes -= minutos_gastos
        horario_atual = proximo

    return total


def imprimir_comanda(veiculo, entrada, saida, preco):
    print("\n=== 🧾 COMANDA ===")
    print(f"Veículo: {veiculo.__class__.__name__.upper()}")
    print(f"Placa: {veiculo.placa}")
    print(f"Entrada: {entrada.strftime('%d/%m/%Y %H:%M')}")
    print(f"Saída:   {saida.strftime('%d/%m/%Y %H:%M')}")
    tempo = (saida - entrada).total_seconds() / 60
    print(f"Tempo estacionado: {int(tempo)} minutos")
    print(f"Valor a pagar: R$ {preco:.2f}")
    print("========================")


def retirar_veiculo():
    mostrar_vagas()
    placa = input("Digite a placa do veículo para retirar: ").upper()

    for numero, veiculo in vagas.items():
        if veiculo is not None and veiculo.placa == placa:
            saida = datetime.datetime.now()
            preco = calcular_preco_veiculo(veiculo, saida)
            entrada = veiculo.entrada

            imprimir_comanda(veiculo, entrada, saida, preco)

            pagamento = input("Confirmar pagamento? (s/n): ").lower()
            if pagamento == 's':
                vagas[numero] = None
                print("✅ Pagamento realizado. Vaga liberada.")
            else:
                print("🚫 Pagamento não confirmado. Veículo permanece estacionado.")
            return

    print("🚫 Veículo não encontrado.")


def passar_dias(dias):
    for veiculo in vagas.values():
        if veiculo is not None:
            veiculo.entrada -= timedelta(days=dias)
    print(f"⏳ {dias} dia(s) passaram.")


def menu():
    while True:
        print("\n=== 🅿️ Sistema de Estacionamento ===")
        print("1. Estacionar veículo")
        print("2. Retirar veículo e pagar")
        print("3. Mostrar vagas")
        print("4. Simular passar dias")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            estacionar_veiculo()
        elif opcao == "2":
            retirar_veiculo()
        elif opcao == "3":
            mostrar_vagas()
        elif opcao == "4":
            dias = int(input("Quantos dias deseja simular? "))
            passar_dias(dias)
        elif opcao == "5":
            print("👋 Saindo... Até logo!")
            break
        else:
            print("🚫 Opção inválida.")

if __name__ == "__main__":
    menu()
