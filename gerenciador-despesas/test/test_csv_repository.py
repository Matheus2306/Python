from pathlib import Path
from decimal import Decimal
from entity.movimentacao import Movimentacao
from repositories.csv_repository import CsvRepository
from uuid import UUID, uuid4

#& tmp_path / "movimentacoes.csv" -> fornece um diretório temporário isolado para o teste 

def test_salvar_movimentacao(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"

    repositorio = CsvRepository(caminho)

    movimentacao = Movimentacao(
        descricao= "Salário",
        tipo= "receita",
        valor= Decimal("3500.00")
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

def test_preservar_uuid_apos_salvar_e_listar(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    movimentacao = Movimentacao(
        descricao="Mercado",
        tipo="despesa",
        valor=Decimal("250")
    )

    id_original = movimentacao.id
    repositorio.salvar(movimentacao)

    recuperadas = repositorio.listar()

    assert len(recuperadas) == 1
    assert recuperadas[0].id == id_original
    assert isinstance(recuperadas[0].id, UUID)

def test_criar_duas_mov_id_diferente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    movs = [
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Mercado", "despesa", Decimal("250"))
    ]

    for dados in movs:
        repositorio.salvar(movimentacao= dados)

    movimentacoes = repositorio.listar()

    assert len(movimentacoes) == 2
    assert movimentacoes[0].id != movimentacoes[1].id
    assert movimentacoes[0].id == movs[0].id
    assert movimentacoes[1].id == movs[1].id


def test_buscar_pelo_id(tmp_path: Path):
    caminho= tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    movs = [
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Mercado01", "despesa", Decimal("250"))
    ]
    
    for dados in movs:
        repositorio.salvar(movimentacao= dados)

    resultado = repositorio.buscar_por_id(movs[0].id)

    assert resultado == movs[0]
    assert isinstance(resultado, Movimentacao)

def test_buscar_por_id_inexistente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    mov = Movimentacao("Mercado01", "despesa", Decimal("250"))

    repositorio.salvar(mov) 

    uuid = uuid4()

    resultado = repositorio.buscar_por_id(uuid)

    assert resultado is None

def test_excluir_movimentacao_csv(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    movs = [
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Mercado01", "despesa", Decimal("250")),
        Movimentacao("Mercado02", "despesa", Decimal("250"))
    ]

    for mov in movs:
        repositorio.salvar(mov)

    resultado = repositorio.excluir(movs[1].id)

    movimentacoes = repositorio.listar()

    presente_lista = False
    for mov in movimentacoes:
        if mov.id == movs[1].id:
            presente_lista = True
            break

    esperadas = [movs[0], movs[2]]

    assert movimentacoes == esperadas
    assert resultado
    assert len(movimentacoes) == 2
    assert not presente_lista

def test_unico_registro_excluir(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)

    mov = Movimentacao("despesa", "despesa", Decimal("43"))

    repositorio.salvar(mov)

    resultado = repositorio.excluir(mov.id)
    lista = repositorio.listar()

    assert resultado
    assert lista == []

def test_id_inexistente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)
    
    mov = Movimentacao("despesa", "despesa", Decimal("43"))
    
    repositorio.salvar(mov)

    id_inexistente = uuid4()
    
    resultado = repositorio.excluir(id_inexistente)
    lista = repositorio.listar()

    assert not resultado
    assert len(lista) == 1

def test_atualizar_existente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)
    
    movs = [
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Mercado01", "despesa", Decimal("250")),
        Movimentacao("Mercado02", "despesa", Decimal("250"))
    ]

    for mov in movs:
        repositorio.salvar(mov)

    atualizar = Movimentacao(
        descricao= "teste",
        tipo="receita",
        valor= Decimal("55.90"),
        id= movs[0].id
    )

    resultado = repositorio.atualizar(atualizar)

    lista = repositorio.listar()

    assert resultado
    assert len(lista) == 3
    assert lista[0].id == movs[0].id
    assert lista[0] == atualizar
    assert lista[1] == movs[1]
    assert lista[2] == movs[2]

def test_atualizar_inexistente(tmp_path: Path):
    caminho = tmp_path / "movimentacoes.csv"
    repositorio = CsvRepository(caminho)
    
    movs = [
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Mercado01", "despesa", Decimal("250")),
        Movimentacao("Mercado02", "despesa", Decimal("250"))
    ]

    for mov in movs:
        repositorio.salvar(mov)

    atualizar = Movimentacao(
        descricao= "teste",
        tipo="receita",
        valor= Decimal("55.90")
    )

    resultado = repositorio.atualizar(atualizar)

    lista = repositorio.listar()
    
    assert resultado is False
    assert lista == movs