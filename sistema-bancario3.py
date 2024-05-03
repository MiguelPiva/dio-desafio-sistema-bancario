from abc import ABC, abstractmethod
from datetime import date
import os


class Transacao(ABC):
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Conta():
    def __init__(self, numero: int, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)
    
    @property
    def saldo(self) -> float:
        return self._saldo    
    
    @property
    def numero(self) -> int:
        return self._numero
    
    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    

    def sacar(self, valor: float) -> bool:
        saldo = self._saldo
        saque_invalido = valor < 0
        excedeu_saldo = valor < saldo
        
        if saque_invalido:
            print("Não é possível sacar um valor menor ou igual a zero.")
            return False
        
        elif excedeu_saldo:
            print("Saldo insuficiente.")
            return False
        
        else:
            self._saldo -= valor
            print(f"R$ {valor:.2f} sacado com sucesso.")
            return True
        


    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print(f"R$ {valor:.2f} depositado com sucesso.")
            return True
        else:
            print("Não é possível depositar um valor menor ou igual a zero.")
            return False


class Cliente():
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    
    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)


class Historico():
    def __init__(self):
        self._transacoes = []

    def registrar_transacao(transacao: Transacao):

        pass


class Pessoa_fisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)


class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite = 800, limite_saques = 3):
        super().__init__(cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        limite = self._limite
        limite_saques = self._limite_saques

        excedeu_limite = valor > self._limite
        excedeu_limite_saques = True if len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__ ]) < 3 else False


class Deposito(Transacao):
    def valor(self, valor: float):
        pass


    def registrar(self, conta: Conta):
        pass

class Saque(Transacao):
    def valor(self, valor: float):
        pass

    
    def registrar(self, conta: Conta):
        pass