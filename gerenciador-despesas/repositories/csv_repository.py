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

            escritor.writerow({
                "descricao": movimentacao.descricao,
                "tipo": movimentacao.tipo,
                "valor": str(movimentacao.valor)
            })

    def listar(self) -> list[Movimentacao]:
        movimentacoes = []

        with open(
            self.caminho,
            "r",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                valor_sinal = Decimal(linha["valor"].replace(",", "."))
                
                movimentacao = Movimentacao(
                    descricao = linha["descricao"],
                    tipo = linha["tipo"],
                    valor = valor_sinal
                    )

                movimentacoes.append(movimentacao)
        return movimentacoes
