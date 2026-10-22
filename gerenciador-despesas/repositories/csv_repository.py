
import csv
from pathlib import Path

from entity.movimentacao import Movimentacao
from decimal import Decimal


class CsvRepository:
    def __init__(self, caminho: Path):
        self.caminho = caminho

        if not self.caminho.exists():
            self.criar_arquivo()

    def criar_arquivo(self):
        with open(
            self.caminho,
            "w",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=["descricao", "tipo", "valor"]
            )

            escritor.writeheader()
    
    def salvar(self, movimentacao: Movimentacao) -> None:
        with open(
            self.caminho,
            "a",
            newline="",
            encoding="utf-8"
        ) as arquivo:

            escritor = csv.DictWriter(
                arquivo,
                fieldnames=["descricao", "tipo", "valor"]
            )
            escritor.writerow(movimentacao)
