def validar_nota(nota):
    """
    Valida se nota esta em [0, 10].

    Args:
        nota: Nota a validar

    Returns:
        bool: True se valida
    """
    return 0 <= nota <= 10

def calcular_media(notas):
    """
    Calcula media de uma lista.

    Args:
        notas: Lista de notas

    Returns:
        float: Media das validas

    Raises:
        ValueError: Se vazia
    """
    if not notas:
        raise ValueError("Lista de notas vazia")

    notas_validas = [n for n in notas if validar_nota(n)]

    if not notas_validas:
        raise ValueError("Nenhuma nota valida")

    return sum(notas_validas) / len(notas_validas)


def obter_situacao(media):
    """
    Determina situacao do aluno.
    """
    if not validar_nota(media):
        raise ValueError("Media invalida")

    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperacao"
    else:
        return "Reprovado"


def calcular_estatisticas(notas):
    """
    Calcula estatisticas.
    """
    notas_validas = [n for n in notas if validar_nota(n)]

    if not notas_validas:
        raise ValueError("Nenhuma nota valida")

    media = calcular_media(notas_validas)

    estatisticas = {
        "media": media,
        "maior": max(notas_validas),
        "menor": min(notas_validas),
        "aprovados": 0,
        "recuperacao": 0,
        "reprovados": 0
    }

    for nota in notas_validas:
        situacao = obter_situacao(nota)
        if situacao == "Aprovado":
            estatisticas["aprovados"] += 1
        elif situacao == "Recuperacao":
            estatisticas["recuperacao"] += 1
        else:
            estatisticas["reprovados"] += 1

    return estatisticas


def normalizar_notas(notas, nota_maxima=10):
    """
    Normaliza para escala 0-10.
    """
    if nota_maxima <= 0:
        raise ValueError("nota_maxima deve ser maior que zero")

    return [(nota / nota_maxima) * 10 for nota in notas]