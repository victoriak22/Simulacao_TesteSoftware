import pytest

from src.notas import validar_nota, calcular_estatisticas, calcular_media, obter_situacao, normalizar_notas

class TestValidarNota:
    def test_nota_valida_inteira (self) :
        assert validar_nota (0) == True
    def test_nota_valida_inteira (self) :
        assert validar_nota (5) == True
    def test_nota_valida_inteira (self) :
        assert validar_nota (10) == True
    def test_nota_invalida_negativa (self) :
        assert validar_nota (-1) == False
    def test_nota_invalida_acima (self) :
        assert validar_nota (11) == False

class TestCalcularMedia:
    def test_media_simples(self):
        assert calcular_media([5, 5, 5]) == 5.0

    def test_media_com_decimais(self):
        assert calcular_media([7.5, 8.5]) == 8.0

    def test_media_com_notas_invalidas(self):
        assert calcular_media([5, -1, 10]) == 7.5

    def test_media_lista_vazia(self):
        with pytest.raises(ValueError):
            calcular_media([])

    def test_media_sem_notas_validas(self):
        with pytest.raises(ValueError):
            calcular_media([-1, 20])

class TestObterSituacao:
    def test_aprovado(self):
        assert obter_situacao(7.0) == "Aprovado"

    def test_aprovado_acima(self):
        assert obter_situacao(9.5) == "Aprovado"

    def test_recuperacao_limite(self):
        assert obter_situacao(5.0) == "Recuperacao"

    def test_reprovado(self):
        assert obter_situacao(4.9) == "Reprovado"

    def test_media_invalida(self):
        with pytest.raises(ValueError):
            obter_situacao(11)


class TestCalcularEstatisticas:
    def test_estatisticas_basicas(self):
        notas = [3, 5, 7, 9]
        resultado = calcular_estatisticas(notas)

        assert resultado["media"] == 6.0
        assert resultado["maior"] == 9
        assert resultado["menor"] == 3

    def test_contagem_situacoes(self):
        notas = [4, 5, 6, 7, 8]
        resultado = calcular_estatisticas(notas)

        assert resultado["aprovados"] == 2
        assert resultado["recuperacao"] == 2
        assert resultado["reprovados"] == 1

    def test_com_notas_invalidas(self):
        notas = [5, 7, -1, 20]
        resultado = calcular_estatisticas(notas)

        assert resultado["media"] == 6.0

    def test_apenas_uma_nota(self):
        resultado = calcular_estatisticas([8])

        assert resultado["media"] == 8
        assert resultado["maior"] == 8
        assert resultado["menor"] == 8

    def test_sem_notas_validas(self):
        with pytest.raises(ValueError):
            calcular_estatisticas([-1, 20])


class TestNormalizarNotas:
    def test_normalizacao_basica(self):
        assert normalizar_notas([10, 20], 20) == [5.0, 10.0]

    def test_normalizacao_com_escala_10(self):
        assert normalizar_notas([5, 10]) == [5.0, 10.0]

    def test_lista_vazia(self):
        assert normalizar_notas([]) == []

    def test_notas_decimais(self):
        resultado = normalizar_notas([2.5, 5.0], 5.0)
        assert resultado == [5.0, 10.0]

    def test_nota_maxima_invalida(self):
        with pytest.raises(ValueError):
            normalizar_notas([5, 10], 0)