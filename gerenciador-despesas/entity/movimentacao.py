from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Movimentacao:
    descricao:str
    tipo:str
    valor:Decimal

    #& __post_init__ após rodar  o __init__ passa pelo post init que realiza validações de dados, etc...
    #& raise usada para lançar exceção, que o código por fora usa do try/except para capturar a exceção lançada
    #& ValueError é um tipo de excessão usada para mostrar um valor inadequado para operação
    #& a seta "->"  representa que o método irá retornar um valor x (str, Decimal, int, bool, classes, etc...)

    def __post_init__(self):
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
        

try:
    receita = Movimentacao("passo", "receita", Decimal("3255"))
    despesa = Movimentacao("Mercado", "despesa", Decimal("250.00"))

    print(receita.exibir_resumo())
except Exception as e:
    print(e)