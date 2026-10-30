import csv
from pathlib import Path
from entity.movimentacao import Movimentacao
from decimal import Decimal
from uuid import UUID
import tempfile
import os


class CsvRepository():
    def __init__(self, caminho: Path):
        
        self.caminho = caminho
        self.fildnames = ["id", "descricao", "tipo", "valor"]

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
                fieldnames= self.fildnames
            )

            escritor.writeheader()

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
                    id = UUID(linha["id"]),
                    descricao = linha["descricao"],
                    tipo = linha["tipo"],
                    valor = valor_sinal
                )

                movimentacoes.append(movimentacao)
        return movimentacoes

    def buscar_por_id(self, identificador: UUID) -> Movimentacao | None:
        with open(
            self.caminho,
            "r",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                if UUID(linha["id"]) == identificador:
                    return Movimentacao(
                        id= UUID(linha["id"]),
                        descricao= linha["descricao"],
                        tipo= linha["tipo"],
                        valor= Decimal(linha["valor"])
                    )
            return None
    
    def salvar(self, movimentacao: Movimentacao) -> None:
        with open(
            self.caminho,
            "a",
            newline="",
            encoding="utf-8"
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames= self.fildnames
            )

            escritor.writerow({
                "id": str(movimentacao.id),
                "descricao": str(movimentacao.descricao),
                "tipo": str(movimentacao.tipo),
                "valor": str(movimentacao.valor)
            })
    
    def excluir(self, identificador: UUID) -> bool:
        movimentacoes = self.listar()
        restantes = []

        encontrou = False

        for mov in movimentacoes:
            if mov.id == identificador:
                encontrou = True
            else:
                restantes.append(mov)

        if not encontrou:
            return False

        self._reescrever_arquivo(restantes)
        
        return True

    def atualizar(self, movimentacao: Movimentacao) -> bool:
        movimentacoes = self.listar()

        for indice, mov in enumerate(movimentacoes):
            if mov.id == movimentacao.id:
                movimentacoes[indice] = movimentacao

                self._reescrever_arquivo(movimentacoes)
                return True

        return False

    def _reescrever_arquivo(self, movimentacoes: list[Movimentacao]) -> None:
        caminho_temporario = None
        
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                newline="",
                encoding="utf-8",
                dir=self.caminho.parent,
                suffix=".csv",
                delete=False
            ) as arquivo:
        
                caminho_temporario = Path(arquivo.name)
        
                escritor = csv.DictWriter(
                    arquivo,
                    fieldnames= self.fildnames
                )
        
                escritor.writeheader()
        
                for mov in movimentacoes:
                    escritor.writerow({
                        "id": str(mov.id),
                        "descricao": mov.descricao,
                        "tipo": mov.tipo,
                        "valor": str(mov.valor)
                    })
        
            os.replace(caminho_temporario, self.caminho)
        
        finally:
            if caminho_temporario is not None:
                caminho_temporario.unlink(missing_ok=True)