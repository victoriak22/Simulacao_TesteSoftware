"""Testes para o Sistema de Cálculo de Frete."""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from frete import calcular_frete

# Fixtures definidas em conftest.py: valor_normal (R$100), valor_gratis (R$250)


# ---------------------------------------------------------------------------
# 1. Classes de Equivalência
# ---------------------------------------------------------------------------

class TestClassesEquivalencia:

    def test_ce_peso_faixa1_mesma_regiao(self, valor_normal):
        """CE-P1 × CE-D1 → R$ 10,00"""
        assert calcular_frete(0.5, "mesma_regiao", valor_normal) == 10.00

    def test_ce_peso_faixa2_outra_regiao(self, valor_normal):
        """CE-P2 × CE-D2 → R$ 22,50"""
        assert calcular_frete(3.0, "outra_regiao", valor_normal) == 22.50

    def test_ce_peso_faixa3_internacional(self, valor_normal):
        """CE-P3 × CE-D3 → R$ 50,00"""
        assert calcular_frete(10.0, "internacional", valor_normal) == 50.00

    def test_ce_frete_gratis(self, valor_gratis):
        """CE-V2: pedido > R$ 200 → frete 0,0"""
        assert calcular_frete(15.0, "internacional", valor_gratis) == 0.0

    def test_ce_destino_invalido(self, valor_normal):
        """CE-D4: destino fora do conjunto válido → ValueError"""
        with pytest.raises(ValueError, match="Destino inválido"):
            calcular_frete(1.0, "exterior", valor_normal)


# ---------------------------------------------------------------------------
# 2. Valores Limite
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("peso, esperado", [
    # Fronteira 1 kg
    (0.999, 10.00),
    (1.000, 10.00),
    (1.001, 15.00),
    # Fronteira 5 kg
    (4.999, 15.00),
    (5.000, 15.00),
    (5.001, 25.00),
    # Fronteira 20 kg
    (19.999, 25.00),
    (20.000, 25.00),
    # 20.001 → inválido, coberto em TestEntradasInvalidas
])
def test_valores_limite(peso, esperado, valor_normal):
    assert calcular_frete(peso, "mesma_regiao", valor_normal) == pytest.approx(esperado, abs=0.01)


# ---------------------------------------------------------------------------
# 3. Tabela de Decisão
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("peso, destino, valor_pedido, esperado", [
    (0.5,  "mesma_regiao",  100.0, 10.00),
    (0.5,  "outra_regiao",  100.0, 15.00),
    (0.5,  "internacional", 100.0, 20.00),
    (3.0,  "mesma_regiao",  100.0, 15.00),
    (10.0, "outra_regiao",  100.0, 37.50),
    (18.0, "internacional", 201.0,  0.00),
], ids=["R1", "R2", "R3", "R4", "R5", "R6"])
def test_tabela_decisao(peso, destino, valor_pedido, esperado):
    assert calcular_frete(peso, destino, valor_pedido) == pytest.approx(esperado, abs=0.01)


# ---------------------------------------------------------------------------
# 4. Entradas Inválidas
# ---------------------------------------------------------------------------

class TestEntradasInvalidas:

    def test_peso_zero(self, valor_normal):
        with pytest.raises(ValueError, match="maior que zero"):
            calcular_frete(0, "mesma_regiao", valor_normal)

    def test_peso_acima_20(self, valor_normal):
        with pytest.raises(ValueError, match="20 kg"):
            calcular_frete(20.001, "mesma_regiao", valor_normal)


# ---------------------------------------------------------------------------
# 5. Property-Based Testing (Hypothesis)
# ---------------------------------------------------------------------------

DESTINOS     = st.sampled_from(["mesma_regiao", "outra_regiao", "internacional"])
PESO_VALIDO  = st.floats(min_value=0.001, max_value=20.0, allow_nan=False, allow_infinity=False)
VALOR_PEDIDO = st.floats(min_value=0.0,   max_value=1000.0, allow_nan=False, allow_infinity=False)


@given(peso=PESO_VALIDO, destino=DESTINOS, valor_pedido=VALOR_PEDIDO)
@settings(max_examples=300)
def test_prop_frete_nunca_negativo(peso, destino, valor_pedido):
    assert calcular_frete(peso, destino, valor_pedido) >= 0.0


@given(peso=PESO_VALIDO, destino=DESTINOS,
       valor_pedido=st.floats(min_value=200.01, max_value=10_000.0,
                              allow_nan=False, allow_infinity=False))
@settings(max_examples=200)
def test_prop_pedido_acima_200_frete_gratis(peso, destino, valor_pedido):
    assert calcular_frete(peso, destino, valor_pedido) == 0.0


@given(peso=PESO_VALIDO, valor_pedido=VALOR_PEDIDO)
@settings(max_examples=300)
def test_prop_ordenacao_por_destino(peso, valor_pedido):
    """frete internacional ≥ outra_regiao ≥ mesma_regiao para qualquer peso e valor."""
    frete_mesma = calcular_frete(peso, "mesma_regiao",  valor_pedido)
    frete_outra = calcular_frete(peso, "outra_regiao",  valor_pedido)
    frete_intl  = calcular_frete(peso, "internacional", valor_pedido)
    assert frete_outra >= frete_mesma
    assert frete_intl  >= frete_outra