from pathlib import Path
from repositories.csv_repository import CsvRepository
from services.movimentacao_service import MovimentacaoService
from decimal import Decimal, InvalidOperation
from utils import menu_terminal, limpa_terminal

caminho_csv = Path("Movimentacoes.csv")

repositorio = CsvRepository(caminho_csv)
servico = MovimentacaoService(repositorio)

def cadastrar_movimentacao_terminal():
    print("=== CADASTRAR MOVIMENTAÇÃO ===")

    descricao = input("Descrição: ").strip()
    tipo = input("Tipo (receita/despesa): ").strip().lower()

    try:
        valor = Decimal(input("Valor: ").replace(",", "."))
    except InvalidOperation:
        print("Valor numérico inválido.")
        return

    try:
        servico.cadastrar(
            descricao= descricao,
            tipo= tipo,
            valor= valor
        )

        print("Movimentação cadastrada com sucesso!")

    except ValueError as erro:
        print(f"Erro de validação: {erro}")

def listar_movimentacoes_terminal():
    movimentacoes = servico.listar_movimentacoes()

    if not movimentacoes:
        print("Nenhuma movimentação cadastrada.")
        return

    print("=== EXTRATO FINANCEIRO ===")

    for indice, movimentacao in enumerate(movimentacoes, start=1):
        print(f"{indice} - {movimentacao.exibir_resumo()}")

def consultar_saldo():
    print(f"Saldo: R${servico.calcular_saldo():.2f}")

def filtrar_por_opcao():
    tipo = input("Filtrar por tipo (receita = r/despesa = d)").strip()
    
    try:
        filtrados = servico.filtrar_por_tipo(tipo= tipo)
    except Exception as e:
        print(e)
        return

    print("=== EXTRATO FINANCEIRO ===")
    
    for indice, filtrado in enumerate(filtrados, start=1):
        print(f"{indice} - {filtrado.exibir_resumo()}")

def executar():
    limpa_terminal()
        
    menu_financeiro = {
        "1": ("Cadastrar movimentação", cadastrar_movimentacao_terminal),
        "2": ("Consultar saldo", consultar_saldo),
        "3": ("Imprimir Extrato", listar_movimentacoes_terminal),
        "4": ("Filtrar transações", filtrar_por_opcao),
        "0": ("Sair", None)  # None indica que a opção encerra o loop
    }

    menu_terminal("gerenciador financeiro", menu_financeiro)
       
    return

if __name__ == "__main__":
    limpa_terminal()
    executar()