from typing import Protocol
from entity.movimentacao import Movimentacao
from uuid import UUID

class MovimentacaoRepository(Protocol):
    def listar(self) -> list[Movimentacao]:
        ...

    def salvar(self, movimentacao: Movimentacao) -> None:
        ...

    def buscar_por_id(self, identificador: UUID) -> Movimentacao | None:
        ...

    def excluir(self, identificador:UUID) -> bool:
        ...
    
    def atualizar(self, movimentacao: Movimentacao) -> bool:
        ...