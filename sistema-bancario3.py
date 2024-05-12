import os
from abc import ABC, abstractmethod
from datetime import datetime


# Classes
# //////////////////////////////////////////
# Classe iteradora de contas
class IteradorContas:
    def __init__(self, contas, tipo):
        self.tipo_impressao = tipo
        self.contas = contas
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._indice]
            if self.tipo_impressao == 1:
                return f"Número: {conta.numero} || Saldo: {conta.saldo}"
            else:
                return f"Agência: {conta.agencia} \nNúmero: {conta.numero} \nProprietário: {conta.cliente.nome} \nSaldo: {conta.saldo}"
        
        except IndexError:
            raise StopIteration
        
        finally:
            self._indice += 1       


# Classe Transacao
class Transacao(ABC):
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


# Classe Conta
class Conta:
    def __init__(self, numero: int, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(cliente=cliente, numero=numero)

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
        excedeu_saldo = valor > saldo

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


# Classe Cliente
class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Limite de transações diárias atingido.")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self._contas.append(conta)


# Classe Historico
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar_transacao(self, transacao: Transacao):
        self._transacoes.append(
            {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes_dia = []

        for transacao in self._transacoes:
            if transacao["data"] == data_atual:
                transacoes_dia.append(transacao)
        return transacoes_dia

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao


# Classe PessoaFisica
class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime.date, endereco: str):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento
    
    @property
    def endereco(self):
        return self._endereco


# Classe ContaCorrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        limite = self._limite
        limite_saques = self._limite_saques

        excedeu_limite = valor > limite
        excedeu_limite_saques = (True if len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__]) >= limite_saques else False)

        if excedeu_limite:
            print("O valor solicitado está acima do limite de saque estabelecido.")
            return False
        elif excedeu_limite_saques:
            print("O número máximo de saques diários foi alcançado.")
            return False
        else:
            return super().sacar(valor)


# Classe Deposito
class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        transacao_feita = conta.depositar(self.valor)

        if transacao_feita:
            conta.historico.registrar_transacao(self)


# Classe Saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        transacao_feita = conta.sacar(self.valor)

        if transacao_feita:
            conta.historico.registrar_transacao(self)


# Funções
# //////////////////////////////////////////
# Função imprimir_separador
def imprimir_separador() -> None:
    print("====================================")

# Interface do terminal
def interface() -> int:
    print(
        """
=========== Banco Python ===========
Selecione um número abaixo de acordo
com o desejar fazer:

1 - Depósito
2 - Saque
3 - Extrato
4 - Cadastrar usuário
5 - Criar conta
6 - Exibir contas
7 - Exibir clientes
8 - Encerrar execução
"""
    )
    opcao = int(input("Sua opção: "))
    imprimir_separador()
    return opcao


def log_transacao(func):
    def retorno_func(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}") if resultado != False else None
        return resultado

    return retorno_func


@log_transacao
def depositar(clientes) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente_filtrado = filtrar_cliente(cpf, clientes)
    if cliente_filtrado:
        if len(cliente_filtrado.contas) == 0:
            print("O cliente não possui contas.")
            return False

        contas = cliente_filtrado.contas
        exibir_contas(contas, 1)
        imprimir_separador()
        numero = int(input("Selecione uma conta: "))
        conta_filtrada = [conta for conta in contas if conta.numero == numero]
        if conta_filtrada == []:
            print("Conta inválida.")
            return False

        conta_filtrada = conta_filtrada.pop()
        valor = float(input("Qual é o valor a ser depositado?: "))
        transacao = Deposito(valor)        
        cliente_filtrado.realizar_transacao(conta=conta_filtrada, transacao=transacao)
        return True
    
    else:
        print("O CPF informado não está vinculado a nenhum cliente.")
        return False


@log_transacao
def sacar(clientes) -> bool:
    cpf = input("Informe o CPF (somente números): ")
    cliente_filtrado = filtrar_cliente(cpf, clientes)
    if cliente_filtrado:
        if len(cliente_filtrado.contas) == 0:
            print("O cliente não possui contas.")
            return False

        contas = cliente_filtrado.contas
        exibir_contas(contas, 1)
        imprimir_separador()
        numero = int(input("Selecione uma conta: "))
        conta_filtrada = [conta for conta in contas if conta.numero == numero]
        if conta_filtrada == []:
            print("Conta inválida.")
            return False

        conta_filtrada = conta_filtrada.pop()
        valor = float(input("Qual é o valor a ser sacado?: "))
        transacao = Saque(valor)
        return True
        cliente_filtrado.realizar_transacao(conta=conta_filtrada, transacao=transacao)
    
    else:
        print("O CPF informado não está vinculado a nenhum cliente.")
        return False


# Função mostrar_extrato
def mostrar_extrato(clientes) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente_filtrado = filtrar_cliente(cpf, clientes)
    if cliente_filtrado:
        if len(cliente_filtrado.contas) == 0:
            print("O cliente não possui contas.")
            return

        contas = cliente_filtrado.contas
        exibir_contas(contas, 1)
        imprimir_separador()
        numero = int(input("Selecione uma conta: "))
        conta_filtrada = [conta for conta in contas if conta.numero == numero]
        if conta_filtrada == []:
            print("Conta inválida.")
            return

        total_depositos = 0
        total_saques = 0
        for transacao in conta_filtrada[0].historico.gerar_relatorio(tipo_transacao="saque"):
            print(f"Data: {transacao['data']} || Tipo: {transacao['tipo']} || Valor: {transacao['valor']}")
            if transacao["tipo"] == Saque.__name__:
                total_saques += transacao["valor"]

        for transacao in conta_filtrada[0].historico.gerar_relatorio(tipo_transacao="deposito"):
            print(f"Data: {transacao['data']} || Tipo: {transacao['tipo']} || Valor: {transacao['valor']}")
            if transacao["tipo"] == Deposito.__name__:
                total_depositos += transacao["valor"]

        imprimir_separador()
        print(f"Valor depositado total: {total_depositos}")
        print(f"Valor sacado total: {total_saques}")
        print(f"Saldo atual: {conta_filtrada[0].saldo}")


# Função filtrar_cliente
def filtrar_cliente(cpf, clientes):
    cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrado[0] if cliente_filtrado else None


# Função criar_cliente
def criar_cliente(clientes) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("O CPF informado já está vinculado a um cliente.")

    else:
        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        data_nascimento = datetime.strptime(data_nascimento, "%d-%m-%Y").date()
        cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
        clientes.append(cliente)


# Função criar_conta
def criar_conta(numero_conta, clientes, contas) -> None:
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.adicionar_conta(conta)
        print("Conta criada com sucesso.")

    else:
        print("O CPF informado não está vinculado a nenhum cliente.")


# Função exibir_contas
def exibir_contas(contas, info) -> None:
    if info == 1:
        for conta in IteradorContas(contas, 1):
            print(conta)
    else:
        for conta in IteradorContas(contas, 2):
            print(conta)
            print("||||||||||||||||||||||||||||||||||||")


# Função exibir_clientes
def exibir_clientes(clientes) -> None:
    for cliente in clientes:
        nascimento = cliente.data_nascimento.strftime("%d-%m-%Y")
        print(f"Nome: {cliente.nome} \nCPF: {cliente.cpf} \nnascimento: {nascimento} \nEndereço: {cliente.endereco}")
        print("||||||||||||||||||||||||||||||||||||")

# Código principal
# //////////////////////////////////////////
if __name__ == "__main__":
    clientes = []
    contas = []

    while True:
        os.system("cls")
        opcao = interface()

        match opcao:
            case 1:
                depositar(clientes)

            case 2:
                sacar(clientes)

            case 3:
                mostrar_extrato(clientes)

            case 4:
                criar_cliente(clientes)

            case 5:
                numero_conta = len(contas) + 1
                criar_conta(numero_conta=numero_conta, clientes=clientes, contas=contas)

            case 6:
                exibir_contas(contas, 2)

            case 7:
                exibir_clientes(clientes)

            case 8:
                print("Encerrando sessão...")
                break

            case _:
                print("Opção inválida, escolha novamente.")

        input("Pressione Enter para continuar...")
