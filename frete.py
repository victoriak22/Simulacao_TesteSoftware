"""Sistema de Cálculo de Frete"""


def calcular_frete(peso: float, destino: str, valor_pedido: float) -> float:
    """
    Calcula o frete com base no peso, destino e valor do pedido.

    Parâmetros:
        peso         : peso em kg — deve ser > 0 e <= 20
        destino      : 'mesma_regiao', 'outra_regiao' ou 'internacional'
        valor_pedido : valor total do pedido em R$

    Retorna 0.0 se valor_pedido > R$ 200,00. Lança ValueError para entradas inválidas.
    """
    if peso <= 0:
        raise ValueError(f"Peso inválido: {peso}. O peso deve ser maior que zero.")
    if peso > 20:
        raise ValueError(f"Peso inválido: {peso}. Não aceitamos pacotes acima de 20 kg.")

    destinos_validos = {"mesma_regiao", "outra_regiao", "internacional"}
    if destino not in destinos_validos:
        raise ValueError(f"Destino inválido: '{destino}'. Use: {sorted(destinos_validos)}.")

    if valor_pedido > 200.0:
        return 0.0

    if peso <= 1:
        base = 10.00
    elif peso <= 5:
        base = 15.00
    else:
        base = 25.00

    if destino == "mesma_regiao":
        frete = base
    elif destino == "outra_regiao":
        frete = base * 1.50
    else:
        frete = base * 2.00

    return round(frete, 2)