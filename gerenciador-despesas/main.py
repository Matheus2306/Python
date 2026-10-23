from decimal import Decimal, InvalidOperation
from pathlib import Path
from utils import carregar_movimentacoes, criar_csv, limpa_terminal, inserir_dados,menu_terminal

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
#~ .at[] do pandas altera um valor exxistente por indice, ou seja [indice, "nome da coluna"] = valor para alterar  
#~
#~------------------------------------------- 

#? Variável global de armazenamento em lista das movimentações.
caminho_csv = Path("movimentacoes.csv")



#* Função de cadastro das movimentações
#^ Usam palavras reservadas:
#^ Input: realisa a entrada de dados do usuário por padrão recebe string
#^ Decimal: transforma os números escritos pelo input em valor decimal podendo ser calculado posteriormente
#^ Caso algum erro envia uma exceção de valor inválido usando o invalid operation
#^ .append em movimentações realiza a adição na lista as movimentações criadas. (método usando dos arrays)
#^ Agora usa de inserir dados para enviar para o arquivo .csv
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
        inserir_dados(caminho_csv= caminho_csv, dado = {
            "descricao": descricao,
            "tipo": tipo,
            "valor": valor
        })
        print("Movimentação cadastrada!")
    except Exception as e:
        print(f"Não foi possivel salvar dados: {e}")


#* Imprime o extrato das movimentações de transações passando pela lista completamente
def imprimir_extrato(titulo = "LISTA DE MOVIMENTAÇÕES"):
    tabela = carregar_movimentacoes(caminho_csv= caminho_csv)
    if tabela.empty:
        print("Nenhuma movimentação cadastrada")
        return
    
    print(f"=== {titulo} ===")
    print("Indice | Descrição | Tipo | Valor")
    for movimentacao in tabela.itertuples(index=True, name="movimentacao"):
        print(f"{movimentacao.Index + 1} | {movimentacao.descricao} | {movimentacao.tipo} | {movimentacao.valor}")
        print("_______________________________")

#* Calcula o saldo passando pela lista de cadastro
#^ Usa o tipo da movimentação para realizar o calculo "receita": soma; "despesa": subtrai;
def consultar_saldo():
    saldo = Decimal("0")
    tabela = carregar_movimentacoes(caminho_csv= caminho_csv)

    #! .interrows() retorna o index e o dado como uma tupla por isso usa-se o "_" que usa o para referênciar o index
    for movimentacao in tabela.itertuples(index=True, name="Movimentacoes"):
        valor = Decimal(movimentacao.valor)

        if movimentacao.tipo == "receita":
            saldo += valor
        else:
            saldo -= valor
    return saldo


#* Função de editar movimentação intermediaria onde acontece a seleção da linha para editar e imprime para o usuário qual será o campo para editar. 
def editar_movimentacao():
    while True:
        limpa_terminal( )
        tabela = carregar_movimentacoes(caminho_csv= caminho_csv)
        if tabela.empty:
            print("nenhuma movimentação cadastrada")

        imprimir_extrato("EDITAR MOVIMENTAÇÃO")
        print("Digite 0 para cancelar...")
        try:
            opcao = int(input("Escolha: "))
        except ValueError as e:
            print("Informe um valor válido")
            input("Pressione Enter para continuar...")
            continue

        if opcao == 0:
            return
        
        if opcao < 1 or opcao > len(tabela):
            print("Movimentação inexistente.")
            return

        indice_real = opcao - 1
        movimentacao_selecionada = tabela.iloc[indice_real]["descricao"]
        print(f"Movimentação selecionada: {movimentacao_selecionada}")

        #! Lambda cria uma função que executará somente quando for chamada.
        menu_selecao = {
            "1": ("Alterar descrição", lambda: editar_dado("descricao", indice_real, tabela)),
            "2": ("Alterar tipo", lambda: editar_dado("tipo", indice_real, tabela)),
            "3": ("Alterar valor", lambda: editar_dado("valor", indice_real, tabela)),
            "0": ("Cancelar / Voltar", None)  
        }
        
        menu_terminal(f"Editando: {movimentacao_selecionada}", menu_selecao)

#* Função que edita os dados dinâmicamente por parâmetros
#^ col: coluna a ser editada;
#^ indice: linha que será editada;
#^ df: DataFrame que será editado.
def editar_dado(col, indice, df):
    try:
        novo_dado = input(f"Novo(a) {col}: ").strip()

        if col == "tipo":
            if novo_dado not in ("receita", "despesa"):
                print("tipo inválido")
                return
            if novo_dado ==  df.at[indice, "tipo"]:
                print("O novo tipo não deve ser igual ao anterior")
                return

        if col == "valor":
            try:
                valor = Decimal(novo_dado.replace(",", "."))
            except InvalidOperation:
                print("Valor inválido.")
                return

            if not valor.is_finite() or valor <= 0:
                print("O valor deve ser positivo e finito.")
                return

            novo_dado = str(valor)

        if col == "descricao" and not novo_dado:
            print("A descrição não pode ser vazia.")
            return
        
        df.at[indice, col] = novo_dado
        df.to_csv(caminho_csv, index = False)
        print("Movimentação atualizada com sucesso!")
    except Exception as e:
        print(f"Não foi possivel salvar {e}")


#* Conta a quantidade de movimentações foram realizadas
#^ Métodos de lenght que conta o total de movimentações realizadas
#^ Outro loop para contar a quantidade de cada pelo tipo
def contar_movimentacoes():
    total_receita = 0
    tabela = carregar_movimentacoes(caminho_csv= caminho_csv)
    total_movimentacoes = len(tabela)
    for movimentacao in tabela.itertuples(index=True, name="Movimentacoes"):
        if movimentacao.tipo == "receita":
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
        menu_filtrar = {
            "1": (" - Receitas", filtro_por_opcao, "1"),
            "2": (" - Receitas", filtro_por_opcao, "2"),
            "0": (" - Sair", None)
        }

        menu_terminal("filtrar movimentações", menu_filtrar)
        return



#* realiza o filtro pela a opção selecionada 1 = receita, 2
def filtro_por_opcao(opcao):

    if opcao not in ("1", "2"):
        print("Opção não pode ser vazia")
        return

    tabela = carregar_movimentacoes(caminho_csv= caminho_csv)

    if tabela.empty:
        print("Sem movimentações")
        return

    tipo_selecionado = "receita" if opcao == "1" else "despesa"
    filtrados = tabela[tabela["tipo"] == tipo_selecionado]

    print(f"=== {tipo_selecionado.upper()} ===")
    soma = Decimal("0")
    #! .intertuples() realiza a mesma operação que o .interrows(), porém é mais rápido
    for movimentacao in filtrados.itertuples():
        valor = Decimal(movimentacao.valor)
        print(f"Descrição: {movimentacao.descricao}")
        print(f"Valor: R$ {valor:.2f}")
        print("--------------------------")
        soma += valor
    print(f"Valor total: {soma}")


#* Função de exclusão de objetos do array
#^ Mostra uma lista de várias movimentações e o usuário insere um indice de um dos objetos
#^ Valida se o número digitado é menor que 0 e por fim valida se o o indice é válido
#^ Usa do .drop() para retirar a movimentação e exibe qual movimentação foi removida.
def excluir_movimentacao():
    while True:
        dados = carregar_movimentacoes(caminho_csv= caminho_csv)
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
        if  input_usuario > len(dados):
            print("movimentação inexistente")
            continue


        try:
            #! Tira a linha pelo index
            dados = dados.drop(input_usuario - 1, axis=0)
            #! Reseta os dados
            dados.reset_index(drop = True, inplace = True)
            #! Salva o .csv
            dados.to_csv(caminho_csv, index=False)
            print(f"Movimentação excluída com sucesso!")
        except Exception as e:
            print(f"erro: {e}")

        limpa_terminal()
        input("Precione enter para seguir...")
      

#* Função de execução aqui usa de intermédio as demais funções produzidas anteriormente
#^ While true: loop para escolha das opções e realizar as demais opções
#^ De acordo com a opção solicitada pelo input realiza algum tipo de operação   
def executar():
    while True:
        limpa_terminal()
        
        menu_financeiro = {
            "1": ("Cadastrar movimentação", cadastrar_movimentacao),
            "2": ("Consultar saldo", consultar_saldo),
            "3": ("Imprimir extrato das movimentações", imprimir_extrato),
            "4": ("Contar movimentações", contar_movimentacoes),
            "5": ("Filtrar por tipo", filtrar_movimentacoes),
            "6": ("Editar movimentação", editar_movimentacao),
            "7": ("Excluir Movimentações", excluir_movimentacao),
            "0": ("Sair", None)  # None indica que a opção encerra o loop
        }

        menu_terminal("gerenciador financeiro", menu_financeiro)
       
        return
        

if __name__ == "__main__":
    limpa_terminal()
    if not caminho_csv.exists():
        criar_csv()
    executar()