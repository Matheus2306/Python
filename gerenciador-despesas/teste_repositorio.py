from pathlib import Path
from decimal import Decimal

from entity.movimentacao import Movimentacao
from repositories.csv_repository import CsvRepository

repositorio = CsvRepository(Path("Movimentacoes.csv"))

receita = Movimentacao("Salário", "receita", Decimal("3500"))
despesa = Movimentacao("Mercado", "despesa", Decimal("250"))

try:
    repositorio.salvar(receita)
    repositorio.salvar(despesa)
except Exception as e:
    print(e)

print("Movimentações salvas!")