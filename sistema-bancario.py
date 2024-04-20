# Importando bibliotecas
# //////////////////////////////////////////
import os


# Funções
# //////////////////////////////////////////
def interface() -> int:
    print("""
=========== Banco Python ===========
Selecione um número abaixo de acordo
com o desejar fazer:
            
1 - Depósito
2 - Saque
3 - Extrato
4 - Cadastrar usuário
5 - Criar conta
6 - Exibir contas
7 - Exibir usuários
8 - Encerrar execução
""")
    opcao = int(input("Sua opção: "))
    print("====================================")
    return opcao


def cadastrar_usuario(nome: str, nascimento: str, cpf: str, endereço: str) -> dict:
    usuario = {"nome": nome,
                "nascimento": nascimento,
                "cpf": cpf,
                "endereço": endereço
                }
    return usuario


def criar_conta(num_agencia: str, numero_conta: str, cpf_proprietario: str) -> dict:
    conta = {"agencia": num_agencia,
            "numero": numero_conta,
            "cpf": cpf_proprietario
            }
    return conta


def verificar_usuario(cpf: str, cpfs: list) -> bool:
    if cpf in cpfs:
        return False
    else:
        return True
    

def exibir_usuario(usuarios: dict) -> None:
    for usuario in usuarios.values():
        print(f"Nome: {usuario['nome']} | Nascimento: {usuario['nascimento']} | CPF: {usuario['cpf']} | Endereço: {usuario['endereço']}")
    return


def exibir_contas(contas: list) -> None:
    for conta in contas:
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']} | CPF: {conta['cpf']}")
    return


def exibir_extrato(saldo: float, /, *, extrato: list) -> None:
    print(f"Depósitos: {' | '.join(extrato[0])}")
    print(f"Saques: {' | '.join(extrato[1])}")
    print(f"\nSaldo: R$ {saldo:.2f}")
    return


def depositar(saldo: float, valor: float, /):
    if valor > 0:
        return (saldo+valor), (f"R$ {valor:.2f}")
    else:
        print("Não é possível depositar um valor menor ou igual a zero.")
        return (saldo), (f"R$ {valor:.2f}")


def sacar(*, saldo: float, valor: float, limite_saque: float, limite_saques: int, quantidade_saques: int):
    verif_1 = valor > 0
    verif_2 = valor < saldo
    verif_3 = valor < limite_saque
    verif_4 = quantidade_saques < limite_saques

    if (verif_1 and verif_2 and verif_3 and verif_4):
        print(f"R$ {valor:.2f} sacado com sucesso.")
    
    elif not verif_1:
        print("Não é possível sacar um valor menor ou igual a zero.")
    elif not verif_2:
        print("Saldo insuficiente.")
    elif not verif_3:
        print("O valor excede seu limite de saque.")
    elif not verif_4:
        print("Limite de saques diários atingido.")

    return (saldo), (f"R$ {valor:.2f}")


# Código principal
# //////////////////////////////////////////
if __name__ == "__main__":
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    LIMITE_SAQUE = 3000.00

    depositos_realizados = []
    saques_realizados = []
    usuarios = {}
    contas = []
    saldo = 0.0

    while True:
        os.system("cls")
        opcao = interface()
        
        match opcao:
            # Depositar
            case 1:
                valor = float(input("Digite o valor do depósito: "))
                extrato = ""
                saldo, extrato = depositar(saldo, valor)
                if extrato != "R$ 0.00":
                    depositos_realizados.append(extrato)

            # Sacar
            case 2:
                valor = float(input("Digite o valor do saque: "))
                extrato = ""
                saldo, extrato = sacar(saldo=saldo, valor=valor, limite_saque=LIMITE_SAQUE, limite_saques=LIMITE_SAQUES, quantidade_saques=len(saques_realizados))
                if extrato != "R$ 0.00" and len(saques_realizados) < LIMITE_SAQUES:
                    saques_realizados.append(extrato)
            
            # Exibir extrato
            case 3:
                exibir_extrato(saldo, extrato=(depositos_realizados, saques_realizados))

            # Cadastrar usuário
            case 4:
                usuario = {}
                usuario = cadastrar_usuario(input("Nome: "), input("Data de nascimento (dd/mm/aaaa): "), input("CPF (somente números): "), input("Endereço (logradouro, num - bairro - cidade/sigla do estado): "))
                if verificar_usuario(usuario["cpf"], usuarios.keys()):
                    print("Usuário cadastrado com sucesso.")
                    usuarios[usuario["cpf"]] = usuario
                else:
                    print("CPF já cadastrado.")

            # Criar conta
            case 5:
                num_conta = len(contas) + 1
                nova_conta = criar_conta(AGENCIA, str(num_conta), input("CPF do proprietário (apenas números): "))
                if verificar_usuario(nova_conta["cpf"], usuarios.keys()):
                    print("Não existe usuário cadastrado com esse CPF.")
                else:
                    contas.append(nova_conta)
                    print("Conta criada com sucesso.")

            # Exibir contas
            case 6:
                exibir_contas(contas)

            # Exibir usuários
            case 7:
                exibir_usuario(usuarios)

            # Encerrar execução	
            case 8:
                break
            
            # Opção inválida
            case _:
                print("Opção inválida, escolha novamente.")

        input("Pressione Enter para continuar...")
        