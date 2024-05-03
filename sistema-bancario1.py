# Importando bibliotecas
import os


# Variáveis
opr_deposito = []
opr_saque = []
saldo = 0


# Ciclo principal
while True:
    os.system("cls")
    print("""
=========== Banco Python ===========
Selecione um número entre 1 e 4
de acordo os valores abai
1 - Depósito
2 - Saque
3 - Extrato
4 - Sair
====================================""")
    opcao = int(input("Sua opção: "))
    print("====================================")

    match opcao:
        case 1:
            valor = float(input("Digite o valor do depósito: "))
            verif_1 = valor > 0
            if verif_1 == True:
                saldo += valor
                opr_deposito.append(f"R$ {valor:.2f}")
                print(f"R$ {valor:.2f} depositado com sucesso.", )
            else:
                print("Não é possível depositar um valor menor ou igual a zero.")

        case 2:
            valor = float(input("Digite o valor do saque: "))
            verif_1 = valor > 0
            verif_2 = valor < saldo
            verif_3 = len(opr_saque) < 3
            if (verif_1 and verif_2 and verif_3):
                saldo -= valor
                opr_saque.append(f"R$ {valor:.2f}")
                print(f"R$ {valor:.2f} sacado com sucesso.")
            elif not verif_1:
                print("Não é possível sacar um valor menor ou igual a zero.")
            elif not verif_2:
                print("Saldo insuficiente.")
            elif not verif_3:
                print("Limite de saques diários atingido.")

        case 3:
            print(f"Depósitos: {' - '.join(opr_deposito)}")
            print(f"Saques: {' - '.join(opr_saque)}")
            print(f"Saldo: R$ {saldo:.2f}")

        case 4:
            break

        case _:
            print("Opção inválida, escolha novamente.")

    input("Pressione Enter para continuar...")