import pytest
from decimal import Decimal
from entity.movimentacao import Movimentacao

def test_criar_receita_valida():
    receita = Movimentacao(
        "Salário",
        "receita",
        Decimal("3500")
    )

    assert receita.descricao == "Salário"
    assert receita.eh_receita() is True
    assert receita.calcular_valor_assinado() == Decimal("3500")

def test_criar_despesa_valida():
    despesa = Movimentacao(
        "Mercado",
        "despesa",
        Decimal("250")
    )

    assert despesa.descricao == "Mercado"
    assert despesa.eh_receita() is False
    assert despesa.calcular_valor_assinado() == Decimal("-250")

def test_nao_permitir_descricao_vazia():
    with pytest.raises(ValueError):
        Movimentacao("", "despesa", Decimal("100"))

def test_nao_permitir_tipo_invalido():
    with pytest.raises(ValueError):
        Movimentacao("salário", "inválido", Decimal("100"))

def test_nao_permitir_valor_negativo():
    with pytest.raises(ValueError, match="Valor precisa ser valores numéricos, positivos e maiores que 0"):
        Movimentacao("Salário", "receita", Decimal("-100"))

def test_nao_permitir_valor_nan():
    with pytest.raises(ValueError):
        Movimentacao("salário", "despesa", Decimal("NaN"))

def test_calcular_valor_nao_altera_self_valor():
        despesa = Movimentacao("salário", "despesa", Decimal("100"))

        resultado = despesa.calcular_valor_assinado()

        assert resultado == Decimal("-100")
        assert despesa.valor == Decimal("100")