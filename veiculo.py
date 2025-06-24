from abc import ABC, abstractmethod
import datetime

class Veiculo(ABC):
    def __init__(self, placa):
        self.placa = placa
        self.entrada = datetime.datetime.now()

    @abstractmethod
    def calcular_preco(self, minutos):
        pass

    def __str__(self):
        return f"{self.__class__.__name__.upper()} - {self.placa}"
