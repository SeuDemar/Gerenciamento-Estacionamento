from parking_manager import ParkingManager

def main():
    manager = ParkingManager()

    while True:
        print("\n--- Sistema de Gerenciamento de Estacionamento ---")
        print("1. Estacionar carro")
        print("2. Remover carro")
        print("3. Listar carros estacionados")
        print("4. Sair")

        choice = input("Escolha uma opcao: ")

        if choice == "1":
            license_plate = input("Digite a placa do carro: ").strip().upper()
            print(manager.park_car(license_plate))
        elif choice == "2":
            license_plate = input("Digite a placa do carro para remover: ").strip().upper()
            print(manager.remove_car(license_plate))
        elif choice == "3":
            print(manager.list_cars())
        elif choice == "4":
            print("Saindo do sistema. Ate logo!")
            break
        else:
            print("Opcao invalida. Tente novamente.")

if __name__ == "__main__":
    main()
