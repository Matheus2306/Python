from pathlib import Path
from decimal import Decimal
from entity.movimentacao import Movimentacao
from repositories.csv_repository import CsvRepository

#& tmp_path / "movimentacoes.csv" -> fornece um diretório temporário isolado para o teste 

def test_salvar_movimentacao(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"

    repositorio = CsvRepository(caminho)

    movimentacao = Movimentacao(
        "Salário",
        "receita",
        Decimal("3500.00")
    )

    repositorio.salvar(movimentacao)

    movimentacoes = repositorio.listar()

    assert len(movimentacoes) == 1
    assert movimentacoes[0].descricao == "Salário"
    assert movimentacoes[0].valor == Decimal("3500.00")

def test_criar_csv_automaticamente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"

    assert not caminho.exists()

    CsvRepository(caminho)

    assert caminho.exists()

def test_salvar_tres_movimentacoes(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    
    repositorio = CsvRepository(caminho)

    dados = [
        {"descricao": "teste1", "tipo": "receita", "valor": Decimal("1299.02")},
        {"descricao": "teste2", "tipo": "receita", "valor": Decimal("500.00")},
        {"descricao": "teste3", "tipo": "despesa", "valor": Decimal("50.00")}
    ]
    for dados_mov in dados:
        movimentacao = Movimentacao(**dados_mov)
        repositorio.salvar(movimentacao)

    movimentacoes = repositorio.listar()

    assert len(movimentacoes) == 3


def test_listar_repositorio_vazio(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
        
    repositorio = CsvRepository(caminho)
    movimentacoes = repositorio.listar()

    assert movimentacoes == []