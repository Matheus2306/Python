from decimal import Decimal, InvalidOperation


#~-------------------------------------------
#~_____________Conceitos usados______________
#~
#~ Def ---- declara uma função 
#~ List ---- armazena uma coleção ordenada (váriavel de movimentações)
#~ Dict ---- Armazena pares chave / valor
#~ Decimal ---- Representa números decimais com precisão adequada para valores monetários
#~ Try/except ---- captura exceções
#~ While true ---- executa um loop até ser interrompido com "break"
#~ Return ---- retorna um resultado ou encerra uma função
#~
#~------------------------------------------- 

#? Variável global de armazenamento em lista das movimentações.
movimentacoes = []

#* Função de cadastro das movimentações
#^ Usam palavras reservadas:
#^ Input: realisa a entrada de dados do usuário por padrão recebe string
#^ Decimal: transforma os números escritos pelo input em valor decimal podendo ser calculado posteriormente
#^ Caso algum erro envia uma exceção de valor inválido usando o invalid operation
#^ .append em movimentações realiza a adição na lista as movimentações criadas.
def cadastrarMovimentacao():
    descricao = input('Descrição: ').strip()
    tipo = input('Tipo (receita/despesa): ').strip().lower()

    if descricao == "" or descricao == " ":
        print("Descrição não pode ser vazia")
        return

    if tipo not in ("receita", "despesa"):
        print("tipo inválido")
        return

    try:
        valor = Decimal(input("Valor: ").replace(",", "."))
    except InvalidOperation:
        print("Valor inválido.")

    if valor <= 0:
        print("valor deve ser positivo")
        return

    movimentacoes.append({
        "descricao": descricao,
        "tipo": tipo,
        "valor": valor
    })

    print("Movimentação cadastrada!")

#*Imprime o extrato das movimentações de transações passando pela lista completamente
def imprimirExtrato():
    for movimentacao in movimentacoes:
        print(f"\nDescrição da movimentação: {movimentacao["descricao"]}")
        print(f"Tipo: {movimentacao["tipo"]}")
        print(f"valor: R$ {'+' if movimentacao["tipo"] == "receita" else "-"}{movimentacao["valor"]:.2f}")

#* Calcula o saldo passando pela lista de cadastro
#^ Usa o tipo da movimentação para realizar o calculo "receita": soma; "despesa": subtrai;
def calcularSaldo():
    saldo = Decimal("0")
    for movimentacao in movimentacoes:
        if movimentacao["tipo"] == "receita":
            saldo += movimentacao["valor"]
        else:
            saldo -= movimentacao["valor"]
    return saldo

#* Função de execução aqui usa de intermédio as demais funções produzidas anteriormente
#^ While true: loop para escolha das opções e realizar as demais opções
#^ De acordo com a opção solicitada pelo input realiza algum tipo de operação
def executar():
    while True:
        print("\n === GERENCIADOR FINANCEIRO ===")
        print("1 - Cadastrar movimentação")
        print("2 - Consultar saldo")
        print("3 - Imprimir extrato das movimentações")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrarMovimentacao()
        elif opcao == "2":
            print(f"Saldo: R$ {calcularSaldo():.2f}")
        elif opcao == "3":
            imprimirExtrato()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    executar()