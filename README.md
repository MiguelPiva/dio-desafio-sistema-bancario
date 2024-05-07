## Etapa 1
- Três operações básicas: depósito, saque e extrato:
    - **Depósito**: Recebe apenas valores positivos. Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato;
    - **Saque**: Máximo de 3 diários. Só é possível se o usuário tiver saldo suficiente. Todos os saques devem ser armazenados em uma variável e exibidos na operação de extrato;
    - **Extrato**: Deve exibir todos os depósitos e saques realizados, além do saldo atual na conta.
- Os valores devem ser exibidos no formato monetário (R$ XXX,XX).

## Etapa 2
- Separação do código em funções;
- Implementação de usuários e contas:
    - **Usuários**: Possuem nome, CPF (único para cada usuário), data de nascimento e endereço. Usuários podem ter mais de uma conta;
    - **Contas**: Possuem número de agência, número de conta e CPF do proprietário.

## Etapa 3
- Armazenar dados de clientes e contas bancárias em objetos;
- Implementar POO no sistema baseado no modelo de classe UML apresentado:


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Conta}}}$

<table>
<tr>
    <th>Atributos</th>
    <th></th>
    <th>Métodos</th>
</tr>
<td>

| **Atributo** | **Tipo** |
| --- | --- |
| saldo | float (privado) |
| numero | int (privado) |
| agencia | str (privado) |
| cliente | Cliente (privado) |
| historico | Historico (privado) |
</td>
<td></td>
<td>

| **Método** | **Parâmetros** | **Retorno** |
| --- | --- | --- |
| saldo | - | float |
| nova_conta | cliente: *Cliente*; numero: *int* | Conta |
| sacar | valor: *float* | bool |
| depositar | valor: *float* | bool |
</td>
</table>

<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Conta\underbar{\space\space}corrente}}}$

Classe filha da classe **Conta**.

| **Atributo** | **Tipo** |
| --- | --- |
| limite | float (privado) |
| limite_saques | int (privado) |


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Historico}}}$

| **Método** | **Parâmetros** | **Retorno** |
| --- | --- | --- |
| adicionar_transacao | transacao: *Transacao* | - |


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Transacao (interface)}}}$

| **Método** | **Parâmetros** | **Retorno** |
| --- | --- | --- |
| registrar | conta: *Conta* | - |


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classes: Deposito e Saque}}}$

As duas classes fazem uso da interface Transacao.

| **Atributo** | **Tipo** |
| --- | --- |
| valor | int (privado) |


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Cliente}}}$

<table>
<tr>
    <th>Atributos</th>
    <th></th>
    <th>Métodos</th>
</tr>
<td>

| **Atributo** | **Tipo** |
| --- | --- |
| endereco | str (privado) |
| contas | list (privado) |

</td>
<td></td>
<td>

| **Método** | **Parâmetros** | **Retorno** |
| --- | --- | --- |
| realizar_transacao | conta: *Conta*; transacao: *Transacao* | - |
| adicionar_conta | conta: *Conta* | - |

</td>
</table>


<br>
<br>

$\large{\textsf{\textcolor{powderblue}{Classe: Pessoa\underbar{\space\space}fisica}}}$

Classe filha da classe **Cliente**

| **Atributo** | **Tipo** |
| --- | --- |
| cpf | str (privado)|
| nome | str (privado)|
| data_nascimento | date (privado)|
