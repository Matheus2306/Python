import pytest
from decimal import Decimal
from entity.movimentacao import Movimentacao
from services.movimentacao_service import MovimentacaoService

#& mov = movimentação

class FakeRepository:
    def __init__(self, movimentacoes: list[Movimentacao]):
        self.movimentacoes = movimentacoes
        self.quantidades_salvamentos = 0

    def listar(self) -> list[Movimentacao]:
        return self.movimentacoes

    def salvar(self, mov: Movimentacao)-> None:
        self.quantidades_salvamentos += 1
        self.movimentacoes.append(mov)


def test_calcular_saldo_com_fake():
    movimentacoes = [
        Movimentacao(**{"descricao": "teste1", "tipo": "receita", "valor": Decimal("3500")}),
        Movimentacao(**{"descricao": "teste2", "tipo": "despesa", "valor": Decimal("250")}),
        Movimentacao(**{"descricao": "teste3", "tipo": "despesa", "valor": Decimal("120")})
    ]

    repositorio = FakeRepository(movimentacoes)

    servico = MovimentacaoService(repositorio)

    resultado = servico.calcular_saldo()

    assert resultado == Decimal("3130")
    assert isinstance(resultado, Decimal)

def test_calcular_saldo_lista_vazia():
    movimentacoes = []
    repositorio = FakeRepository(movimentacoes)
    servico = MovimentacaoService(repositorio)

    assert servico.calcular_saldo() == Decimal("0")

def test_salvar_movimentacao_com_fake():
    fake = FakeRepository([])

    mov = Movimentacao(
        "mecado",
        "despesa",
        Decimal("250")
    )
    fake.salvar(mov)

    assert fake.quantidades_salvamentos == 1
    assert len(fake.listar()) == 1
    assert fake.listar()[0] == mov

def test_cadastrar_movimentacao():
    fake = FakeRepository([])
    servico = MovimentacaoService(fake)

    servico.cadastrar(
        descricao= "mecado",
        tipo= "despesa",
        valor= Decimal("250")    
    )

    
    movimentacoes = fake.listar()

    assert fake.quantidades_salvamentos == 1
    assert len(movimentacoes) == 1
    assert movimentacoes[0] == Movimentacao(
            descricao= "mecado",
            tipo= "despesa",
            valor= Decimal("250")    
        )

def test_cadastrar_mov_invalido():
    fake = FakeRepository([])
    servico = MovimentacaoService(fake)
    with pytest.raises(ValueError) as exec_info:

        servico.cadastrar(
            descricao= "mecado",
            tipo= "despesa",
            valor= Decimal("-250")
        )

        assert "positivo" in str(exec_info.value)
    
    movimentacoes = fake.listar()

    assert fake.quantidades_salvamentos == 0
    assert len(movimentacoes) == 0
    assert movimentacoes == []