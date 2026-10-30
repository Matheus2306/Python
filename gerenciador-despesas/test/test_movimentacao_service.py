import pytest
from decimal import Decimal
from entity.movimentacao import Movimentacao
from services.movimentacao_service import MovimentacaoService
from uuid import UUID, uuid4

#& mov = movimentação

class FakeRepository:
    def __init__(self, movimentacoes: list[Movimentacao]):
        self.movimentacoes = movimentacoes
        self.quantidades_salvamentos = 0

    def listar(self) -> list[Movimentacao]:
        return self.movimentacoes

    def buscar_por_id(self, identificador: UUID) -> Movimentacao | None:
        for mov in self.movimentacoes:
            if mov.id == identificador:
                return mov
        return None

    def salvar(self, mov: Movimentacao)-> None:
        self.quantidades_salvamentos += 1
        self.movimentacoes.append(mov)

    def excluir(self, identificador: UUID) -> bool:
        for indice, mov in enumerate(self.movimentacoes):
            if mov.id == identificador:
                self.movimentacoes.pop(indice)
                return True
        
        return False
    
    def atualizar(self, movimentacao: Movimentacao) -> bool:
        for indice, mov in enumerate(self.movimentacoes):

            if mov.id == movimentacao.id:
                self.movimentacoes[indice] = movimentacao
                return True

        return False

def test_calcular_saldo_com_fake():
    movimentacoes = [
        Movimentacao(**{"descricao": "teste1", "tipo": "receita", "valor": Decimal("3500")}),
        Movimentacao(**{"descricao": "teste2", "tipo": "despesa", "valor": Decimal("250")}),
        Movimentacao(**{"descricao": "teste3", "tipo": "despesa", "valor": Decimal("120")})
    ]

    repositorio = FakeRepository(movimentacoes)

    servico = MovimentacaoService(repositorio)

    resultado = servico.calcular_saldo()

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

    assert fake.quantidades_salvamentos == 1
    assert len(fake.listar()) == 1
    assert fake.listar()[0] == mov

def test_cadastrar_movimentacao():
    fake = FakeRepository([])
    servico = MovimentacaoService(fake)

    movimentacao= servico.cadastrar(
        descricao= "mecado",
        tipo= "despesa",
        valor= Decimal("250")    
    )

    
    movimentacoes = fake.listar()

    assert fake.quantidades_salvamentos == 1
    assert len(movimentacoes) == 1
    assert movimentacoes[0] == Movimentacao(
        id= movimentacao.id,
        descricao= movimentacao.descricao,
        tipo= movimentacao.tipo,
        valor= movimentacao.valor
    )

def test_cadastrar_mov_invalido():
    fake = FakeRepository([])
    servico = MovimentacaoService(fake)
    with pytest.raises(ValueError) as exec_info:

        servico.cadastrar(
            descricao= "mecado",
            tipo= "despesa",
            valor= Decimal("-250")
        )

        assert "positivo" in str(exec_info.value)
    
    movimentacoes = fake.listar()

    assert fake.quantidades_salvamentos == 0
    assert len(movimentacoes) == 0
    assert movimentacoes == []

def test_filtrar_receitas():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]

    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)

    resultado = servico.filtrar_por_tipo("R")

    assert len(resultado) == 2
    assert all(mov.tipo == "receita" for mov in resultado)

def test_filtrar_despesas():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "despesa", Decimal("800"))
    ] 
    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)
    
    resultado = servico.filtrar_por_tipo("d")

    assert len(resultado) == 2
    assert all(mov.tipo == "despesa" for mov in resultado)

def test_filtrar_tipo_invalido():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "despesa", Decimal("800"))
    ] 
    
    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)

    with pytest.raises(ValueError) as exec_info:
    
        servico.filtrar_por_tipo("e")
    
    assert "Selecione" in str(exec_info.value)

def test_filtrar_sem_correspondencias():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "receita", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]
    
    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)

    resultado = servico.filtrar_por_tipo("d")
    assert resultado == []

def test_criar_movimentacao_uuid():
    receita = Movimentacao("Salário", "receita", Decimal("3500"))
    despesa = Movimentacao("Mercado", "despesa", Decimal("250"))

    print(receita.id)
    print(despesa.id)

    assert receita.id != despesa.id
    assert isinstance(receita.id, UUID) and isinstance(despesa.id, UUID)

def test_excluir():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]

    fake = FakeRepository(movimentacoes)

    id_excluir = movimentacoes[0].id
    ids_preservar = {
        movimentacoes[1].id,
        movimentacoes[2].id
    }

    resultado = fake.excluir(id_excluir)
    lista = fake.listar()

    assert resultado is True
    assert len(lista) == 2
    assert all(mov.id != id_excluir for mov in lista)
    assert {mov.id for mov in lista} == ids_preservar

def test_excluir_inexistente():
    mov = Movimentacao("Mercado", "receita", Decimal("320.44"))

    fake = FakeRepository([mov])

    id_inexistente = uuid4()

    while id_inexistente == mov.id:
        id_inexistente = uuid4()

    resultado = fake.excluir(id_inexistente)

    lista = fake.listar()

    assert resultado is False
    assert len(lista) == 1
    assert lista[0] is mov

def test_atualizar():
    mov = Movimentacao(descricao="teste", tipo="receita", valor= Decimal("23.43"))

    fake = FakeRepository([mov])

    atualizada = Movimentacao(
        descricao="mercado",
        tipo="despesa",
        valor= Decimal("55.88"), 
        id= mov.id
    )

    resultado = fake.atualizar(atualizada)

    lista = fake.listar()

    assert resultado
    assert lista[0] == atualizada
    assert lista[0].id == mov.id

def test_atualizar_inexistente():
    mov = Movimentacao(
        descricao="teste",
        tipo="receita",
        valor=Decimal("23.43")
    )

    fake = FakeRepository([mov])

    atualizada = Movimentacao(
        descricao="atualização inexistente",
        tipo="despesa",
        valor=Decimal("332")
    )

    resultado = fake.atualizar(atualizada)
    lista = fake.listar()

    assert resultado is False
    assert len(lista) == 1
    assert lista[0] == mov
    assert lista[0] is mov

def test_service_atualizar_existente():
    movimentacoes = [
            Movimentacao("Salário", "receita", Decimal("3500")),
            Movimentacao("Mercado", "despesa", Decimal("250")),
            Movimentacao("Freelance", "receita", Decimal("800"))
    ]

    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)

    # Atualizar um registro.
    atualizar = Movimentacao(
        id= movimentacoes[0].id,
        descricao= "Recuperado",
        tipo= "despesa",
        valor= Decimal("221")
    )

    resultado = servico.atualizar_movimentacao(
        descricao= atualizar.descricao,
        tipo= atualizar.tipo,
        valor= atualizar.valor,
        identificador=atualizar.id
    )
    assert resultado
    # Verificar que os dados mudaram.
    lista = servico.listar_movimentacoes()
    assert lista[0] == atualizar
    # Verificar que o UUID permaneceu igual.
    assert lista[0].id == movimentacoes[0].id

def test_service_atualizar_inexistente():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]
    
    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)
    
    atualizar = Movimentacao(
        descricao= "Recuperado",
        tipo= "despesa",
        valor= Decimal("221")
    )
    
    resultado = servico.atualizar_movimentacao(
        descricao= atualizar.descricao,
        tipo= atualizar.tipo,
        valor= atualizar.valor,
        identificador=atualizar.id
    )

    lista = servico.listar_movimentacoes()

    esta_na_lista = False
    for linha in lista:
        if atualizar.id == linha.id:
            esta_na_lista =True
    

    assert resultado is False
    assert esta_na_lista is False


def test_service_excluir_existente():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]

    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)

    resultado = servico.excluir_movimentacao(movimentacoes[0].id)

    lista = servico.listar_movimentacoes()

    assert resultado
    assert len(lista) == 2


def test_service_excluir_inexistente():
    movimentacoes = [
        Movimentacao("Salário", "receita", Decimal("3500")),
        Movimentacao("Mercado", "despesa", Decimal("250")),
        Movimentacao("Freelance", "receita", Decimal("800"))
    ]
  
    fake = FakeRepository(movimentacoes)
    servico = MovimentacaoService(fake)
  
    resultado = servico.excluir_movimentacao(uuid4())
  
    lista = servico.listar_movimentacoes()
  
    assert resultado is False
    assert len(lista) == 3
  