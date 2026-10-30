from dataclasses import dataclass, field
from decimal import Decimal
from uuid import uuid4, UUID

@dataclass
class Movimentacao:
    descricao:str
    tipo:str
    valor:Decimal
    id:UUID = field(default_factory= uuid4)

    #& __post_init__ após rodar  o __init__ passa pelo post init que realiza validações de dados, etc...
    #& raise usada para lançar exceção, que o código por fora usa do try/except para capturar a exceção lançada
    #& ValueError é um tipo de excessão usada para mostrar um valor inadequado para operação
    #& a seta "->"  representa que o método irá retornar um valor x (str, Decimal, int, bool, classes, etc...)

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise ValueError("O identificador deve ser um UUID válido.")

        if not isinstance(self.descricao, str) or not self.descricao.strip():
            raise ValueError("Descrição não pode ser vazia e deve ser textos.")

        self.descricao = self.descricao.strip()

        if self.tipo not in ("receita", "despesa"):
            raise ValueError("Tipo precisa ser receita ou despesas.")

        if not isinstance(self.valor, Decimal) or not self.valor.is_finite() or self.valor <= 0:
            raise ValueError("Valor precisa ser valores numéricos, positivos e maiores que 0")
        
    #* Retorna o valor de acordo com o tipo da movimentação
    def calcular_valor_assinado(self) -> Decimal:
        if self.tipo == "despesa":
            return -self.valor

        return self.valor

    #* Retorna o objeto referenciado é uma receita ou não
    def eh_receita(self) -> bool:
        if self.tipo == "receita":
            return True
        return False

    #* Exibe um resumo em string
    def exibir_resumo(self) -> str:
        return f"{self.descricao} | {self.tipo} | R$ {self.valor:.2f}"