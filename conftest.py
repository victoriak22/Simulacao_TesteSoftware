import pytest

@pytest.fixture
def destinos_validos():
    """Lista dos três destinos aceitos pelo sistema"""
    return ["mesma_regiao", "outra_regiao", "internacional"]


@pytest.fixture
def valor_normal():
    """Valor de pedido que NÃO aciona frete grátis (≤ R$ 200)"""
    return 100.0


@pytest.fixture
def valor_gratis():
    """Valor de pedido que aciona frete grátis (> R$ 200)"""
    return 250.0