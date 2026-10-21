from decimal import Decimal, InvalidOperation
import os
import csv

#& comentários pessoais
#& para descobrir o tipo de uma variável devemos usa "type(<nome da variável>)"
#& :.2f -> formata valores decimais para duas casas decimais
#& enumerate() -> permite consultar o objeto específico e o indice dele. Dentro dos parentes é inserido a lista de objetos no caso aqui as movimentações e também usar o start para o index começar com um valor específico exemplo 1

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
movimentacoes = [
        {
            "descricao": "teste", 
            "tipo":"receita", 
            "valor": 200
        },
        {
            "descricao": "teste1", 
            "tipo":"despesa", 
            "valor": 322
        },
        {
            "descricao": "teste", 
            "tipo":"receita", 
            "valor": 92.23
        },
        {
            "descricao": "teste", 
            "tipo":"despesa", 
            "valor": 44
        },
        {
            "descricao": "teste", 
            "tipo":"receita", 
            "valor": 9950
        },
        {
            "descricao": "teste", 
            "tipo":"despesa", 
            "valor": 800.33
        },
    ]

#* Função para criar e inserir dados em um arquivo CSV
#^ Método open abre um aquivo parâmetros (caminho do arquivo | modo de uso "w" = Write habilita o modo de escrita do .csv, "r" = read lê o .csv e mosta os dados, "a" = apprend insere os dados no arquivo | newline="" evita de ser inserida uma linha vazia | encoding é o tipo codificação do dado)
#^ Writeheader() usa os parâmetros propostos anteriormente por uma váriavel decrita como escritor
#^ para escrever uma linha do CSV usa o .writerow(dado) que recebe o objeto
def criar_csv():
    with open("Movimentacoes.csv", "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["descricao", "tipo", "valor"]
        )
        escritor.writeheader()

def inserir_dados(dado):
    with open("Movimentacoes.csv", "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(dado)

        


#* Função de cadastro das movimentações
#^ Usam palavras reservadas:
#^ Input: realisa a entrada de dados do usuário por padrão recebe string
#^ Decimal: transforma os números escritos pelo input em valor decimal podendo ser calculado posteriormente
#^ Caso algum erro envia uma exceção de valor inválido usando o invalid operation
#^ .append em movimentações realiza a adição na lista as movimentações criadas.
def cadastrar_movimentacao():
    descricao = input('Descrição: ').strip()

    if not descricao:
        print("Descrição não pode ser vazia")
        return
    
    tipo = input('Tipo (receita/despesa): ').strip().lower()

    if tipo not in ("receita", "despesa"):
        print("tipo inválido")
        return

    try:
        valor = Decimal(input("Valor: ").replace(",", "."))
    except InvalidOperation:
        print("Valor inválido.")
        return

    if not valor.is_finite() or valor <= 0:
        print("valor deve ser positivo e finito.")
        return

    try:
        inserir_dados({
            "descricao": descricao,
            "tipo": tipo,
            "valor": valor
        })
    except:
        print("Não foi possivel salvar dados")
    print("Movimentação cadastrada!")


#* Imprime o extrato das movimentações de transações passando pela lista completamente
def imprimir_extrato():
    if not movimentacoes:
        print("Nenhuma movimentação cadastrada")
        return

    print("=== LISTA DE MOVIMENTAÇÕES ===")
    with open("Movimentacoes.csv", "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo)
        for linha in enumerate(leitor, start = 1):
            sinal = '+' if linha["tipo"] == "receita" else "-"
            print(f"{indice} | {movimentacao["tipo"]} | {sinal}{movimentacao["valor"]:.2f}")
            print("____________________________________________________________")



#* Calcula o saldo passando pela lista de cadastro
#^ Usa o tipo da movimentação para realizar o calculo "receita": soma; "despesa": subtrai;
def calcular_saldo():
    saldo = Decimal("0")
    for movimentacao in movimentacoes:
        if movimentacao["tipo"] == "receita":
            saldo += movimentacao["valor"]
        else:
            saldo -= movimentacao["valor"]
    return saldo


#* Conta a quantidade de movimentações foram realizadas
#^ Métodos de lenght que conta o total de movimentações realizadas
#^ Outro loop para contar a quantidade de cada pelo tipo
def contar_movimentacoes():
    total_receita = 0
    total_movimentacoes = len(movimentacoes)
    for movimentacao in movimentacoes:
        if movimentacao["tipo"] == "receita":
            total_receita += 1
    print("=== ESTATÍSTICAS ===")
    print(f"Total de movimentações: {total_movimentacoes}")
    print(f"Receitas cadastradas: {total_receita}")
    print(f"Despesas cadastradas: {total_movimentacoes - total_receita}")


#* Função que filtra as movimentações pelo tipo Receita / despesa
#^ OS.system está servindo para limpar o terminal 
def filtrar_movimentacoes():
    limpa_terminal()
    
    while True:
        print("=== FILTRAR MOVIMENTAÇÕES ===")
        print("Qual tipo deseja consultar?")
        print("1 - Receitas")
        print("2 - Despesas")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            filtro_por_opcao("1")
            
        elif opcao == "2":
            filtro_por_opcao("2")

        elif opcao == "0":
            return
        else:
            print("Escolha uma opção válida")

        input("precione enter para continuar...")
        limpa_terminal()


#* realiza o filtro pela a opção selecionada 1 = receita, 2
def filtro_por_opcao(opcao):

    if opcao not in ("1", "2"):
        print("Opção não pode ser vazia")
        return

    if not movimentacoes:
        print("Sem movimentações")
        return

    tipo_selecionado = "receita" if opcao == "1" else "despesa"
    filtrados = []
    for movimentacao in movimentacoes:
        if movimentacao["tipo"] == tipo_selecionado:
            filtrados.append(movimentacao)

    if not filtrados:
        print("Nenhuma movimentação desse tipo encontrada.")
        return


    print(f"=== {tipo_selecionado.upper()} ===")
    for movimentacao in filtrados:
        print(f"Descrição: {movimentacao['descricao']}")
        print(f"Valor: R$ {movimentacao['valor']:.2f}")
        print("--------------------------")


#* Função de exclusão de objetos do array
#^ Mostra uma lista de várias movimentações e o usuário insere um indice de um dos objetos
#^ Valida se o número digitado é menor que 0 e por fim valida se o o indice é válido
#^ Usa do .pop() para retirar a movimentação e exibe qual movimentação foi removida.
def excluir_movimentacao():
    while True:
        limpa_terminal()
        print("=== EXCLUIR MOVIMENTAÇÃO ===")
        imprimir_extrato()
        try:
            input_usuario = int(input("Digite o número da movimentação ou digite 0 para voltar: "))
        except ValueError:
            print("Digite um valor válido")
            input("Precione enter para seguir...")
            continue

        if input_usuario == 0:
            return

        if input_usuario < 0:
            print("Digite um número positivo")
            input("Precione enter para seguir...")
            continue
        if  input_usuario > len(movimentacoes):
            print("movimentação inexistente")
            continue

        removido = movimentacoes.pop(input_usuario - 1 )
        limpa_terminal()
        print(f"Movimentação {removido["descricao"]} excluída com sucesso!")
        input("Precione enter para seguir...")
      

#* Função de execução aqui usa de intermédio as demais funções produzidas anteriormente
#^ While true: loop para escolha das opções e realizar as demais opções
#^ De acordo com a opção solicitada pelo input realiza algum tipo de operação
def executar():
    while True:
        print("\n === GERENCIADOR FINANCEIRO ===")
        print("1 - Cadastrar movimentação")
        print("2 - Consultar saldo")
        print("3 - Imprimir extrato das movimentações")
        print("4 - Contar movimentações")
        print("5 - Filtrar por tipo")
        print("6 - Excluir Movimentações")
        print("0 - Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_movimentacao()
        elif opcao == "2":
            print(f"Saldo: R$ {calcular_saldo():.2f}")
        elif opcao == "3":
            imprimir_extrato()
        elif opcao == "4":
            contar_movimentacoes()
        elif opcao == "5":
            filtrar_movimentacoes()
        elif opcao == "6":
            excluir_movimentacao()
        elif opcao == "0":
            limpa_terminal()
            break

        else:
            print("Opção inválida.")

        input("\npressione enter para seguir...")
        limpa_terminal()
        

def limpa_terminal():
    os.system(('cls' if os.name == 'nt' else 'clear'))
    

if __name__ == "__main__":
    limpa_terminal()
    criar_csv()
    executar()