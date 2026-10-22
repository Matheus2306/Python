import os
import csv
import pandas as pd

def limpa_terminal():
    os.system(('cls' if os.name == 'nt' else 'clear'))

#* Função para criar e inserir dados em um arquivo CSV
#^ Método open abre um aquivo parâmetros (caminho do arquivo | modo de uso "w" = Write habilita o modo de escrita do .csv, "r" = read lê o .csv e mosta os dados, "a" = apprend insere os dados no arquivo | newline="" evita de ser inserida uma linha vazia | encoding é o tipo codificação do dado)
#^ Writeheader() usa os parâmetros propostos anteriormente por uma váriavel decrita como escritor
#^ para escrever uma linha do CSV usa o .writerow(dado) que recebe o objeto
def criar_csv(caminho_csv):
    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["descricao", "tipo", "valor"]
        )
        escritor.writeheader()

def inserir_dados(caminho_csv, dado):
    with open(caminho_csv, "a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=["descricao", "tipo", "valor"]
        )
        escritor.writerow(dado)

def carregar_movimentacoes(caminho_csv):
    return pd.read_csv(caminho_csv, dtype={
            "descricao": str,
            "tipo": str,
            "valor": str
        },
        keep_default_na=False
        )


#* Função coringa para criar e gerenciar menus de terminal de forma dinâmica. 
#*    :param titulo: Título principal do menu.
#*    :param opcoes: Dicionário onde a chave é a opção (ex: '1') e o valor é 
#*                   uma tupla no formato: (Descrição da Opção, Função a ser executada).
#*    :param msg_input: Texto exibido no input do usuário.
def menu_terminal(titulo: str, opcoes: dict, msg_input: str = "Escolha: "):
    while True:
        print(f"\n === {titulo.upper()} ===")
        
        #! Exibe as opções dinamicamente com base no dicionário
        for chave, dados in opcoes.items():
            descricao = dados[0]
            print(f"{chave} - {descricao}")
            
        opcao = input(f"\n{msg_input} ").strip()
        
        if opcao in opcoes:
            dados = opcoes[opcao]
            funcao = dados[1]
            
            #! Se a função for None, consideramos que é o comando de saída
            if funcao is None:
                return
                
            print() #! Linha em branco para separar a execução
            #! Verifica se há um 3º elemento (solicitação de parâmetro)
            if len(dados) > 2 and dados[2] is not None:
                param = dados[2]
                
                #! Executa a função passando o parâmetro (que pode ser None)
                funcao(param)
            else:
                #! Executa a função sem parâmetros
                funcao()

                
            input("\nprecione enter para continuar...")
            limpa_terminal()
        else:
            print("\n[!] Opção inválida. Tente novamente.")
