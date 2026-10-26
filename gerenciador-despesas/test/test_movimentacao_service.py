
from decimal import Decimal

from entity.movimentacao import Movimentacao
from services.movimentacao_service import MovimentacaoService


class FakeRepository:
    def __init__(self, movimentacoes: list[Movimentacao]):
        self.movimentacoes = movimentacoes

    def listar(self) -> list[Movimentacao]:
        return self.movimentacoes

    def salvar(self, mov: Movimentacao)-> None:
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

    assert servico.calcular_saldo() == Decimal("3130")
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

    assert len(fake.listar()) == 1