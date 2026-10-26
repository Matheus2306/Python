from typing import Protocol
from entity.movimentacao import Movimentacao

class MovimentacaoRepository(Protocol):
    def listar(self) -> list[Movimentacao]:
        ...

    def salvar(self, movimentacao: Movimentacao) -> None:
        ...