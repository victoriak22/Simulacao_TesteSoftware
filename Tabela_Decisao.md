# Tabela de Decisão e Classes de Equivalência — Sistema de Cálculo de Frete

---

## Classes de Equivalência

As classes particionam o domínio de cada parâmetro em grupos cujos membros
são tratados de forma idêntica pelo sistema — testar um representante equivale
a testar todos os demais dentro do mesmo grupo.

### Parâmetro: `peso`

| ID    | Classe               | Intervalo           | Tipo     | Representante | Resultado esperado   |
|-------|----------------------|---------------------|:--------:|:-------------:|----------------------|
| CE-P1 | Peso faixa 1         | 0 < peso ≤ 1 kg     | Válida   | 0,5 kg        | Tarifa base R$ 10,00 |
| CE-P2 | Peso faixa 2         | 1 kg < peso ≤ 5 kg  | Válida   | 3,0 kg        | Tarifa base R$ 15,00 |
| CE-P3 | Peso faixa 3         | 5 kg < peso ≤ 20 kg | Válida   | 10,0 kg       | Tarifa base R$ 25,00 |
| CE-P4 | Peso zero / negativo | peso ≤ 0            | Inválida | 0 / −1        | `ValueError`         |
| CE-P5 | Peso acima do limite | peso > 20 kg        | Inválida | 21,0 kg       | `ValueError`         |

### Parâmetro: `destino`

| ID    | Classe               | Valor(es)             | Tipo     | Representante     | Resultado esperado  |
|-------|----------------------|-----------------------|:--------:|:-----------------:|---------------------|
| CE-D1 | Mesma região         | `"mesma_regiao"`      | Válida   | `"mesma_regiao"`  | Multiplicador × 1,0 |
| CE-D2 | Outra região         | `"outra_regiao"`      | Válida   | `"outra_regiao"`  | Multiplicador × 1,5 |
| CE-D3 | Internacional        | `"internacional"`     | Válida   | `"internacional"` | Multiplicador × 2,0 |
| CE-D4 | Destino desconhecido | qualquer outro string | Inválida | `"exterior"`      | `ValueError`        |

### Parâmetro: `valor_pedido`

| ID    | Classe        | Intervalo         | Tipo   | Representante | Resultado esperado          |
|-------|---------------|-------------------|:------:|:-------------:|-----------------------------|
| CE-V1 | Pedido normal | valor ≤ R$ 200,00 | Válida | R$ 100,00     | Frete calculado normalmente |
| CE-V2 | Frete grátis  | valor > R$ 200,00 | Válida | R$ 250,00     | Frete = R$ 0,00             |

---

## Tabela de Decisão

### Condições

| #  | Condição                                                  |
|----|-----------------------------------------------------------|
| C1 | **Peso** — faixa em que o pacote se enquadra             |
| C2 | **Destino** — abrangência geográfica da entrega          |
| C3 | **Valor do pedido** — se supera o limiar de frete grátis |

### Regras

| Condição / Ação             | R1           | R2           | R3            | R4           | R5           | R6 (grátis)  |
|-----------------------------|:------------:|:------------:|:-------------:|:------------:|:------------:|:------------:|
| **C1 – Peso**               | ≤ 1 kg       | ≤ 1 kg       | ≤ 1 kg        | 1 – 5 kg     | 5 – 20 kg    | qualquer     |
| **C2 – Destino**            | Mesma região | Outra região | Internacional | Mesma região | Outra região | qualquer     |
| **C3 – Valor do pedido**    | ≤ R$ 200     | ≤ R$ 200     | ≤ R$ 200      | ≤ R$ 200     | ≤ R$ 200     | **> R$ 200** |
| **→ Tarifa base**           | R$ 10,00     | R$ 10,00     | R$ 10,00      | R$ 15,00     | R$ 25,00     | —            |
| **→ Multiplicador destino** | × 1,0        | × 1,5        | × 2,0         | × 1,0        | × 1,5        | —            |
| **→ Frete final**           | **R$ 10,00** | **R$ 15,00** | **R$ 20,00**  | **R$ 15,00** | **R$ 37,50** | **R$ 0,00**  |
| **→ Caso de teste**         | `R1`         | `R2`         | `R3`          | `R4`         | `R5`         | `R6`         |

> **Prioridade das regras:** a condição de frete grátis (C3 > R$ 200) tem
> precedência sobre todas as demais — o frete retorna `0.0` independentemente
> de peso e destino.

### Casos não cobertos pela tabela (entradas inválidas)

Estas condições lançam `ValueError` antes de qualquer cálculo e, portanto,
não compõem regras na tabela de decisão principal.

| Situação                        | Classe CE | Comportamento esperado                             |
|---------------------------------|-----------|----------------------------------------------------|
| Peso = 0 ou negativo            | CE-P4     | `ValueError: peso deve ser maior que zero`         |
| Peso > 20 kg                    | CE-P5     | `ValueError: não aceitamos pacotes acima de 20 kg` |
| Destino fora do conjunto válido | CE-D4     | `ValueError: destino inválido`                     |

---

## Referência rápida

### Tarifas base por faixa de peso

| Faixa               | Tarifa base | Classe CE |
|---------------------|:-----------:|:---------:|
| 0 < peso ≤ 1 kg     | R$ 10,00    | CE-P1     |
| 1 kg < peso ≤ 5 kg  | R$ 15,00    | CE-P2     |
| 5 kg < peso ≤ 20 kg | R$ 25,00    | CE-P3     |
| peso > 20 kg        | ❌ Inválido  | CE-P5     |

### Multiplicadores de destino

| Destino         | Fator  | Efeito sobre a tarifa base | Classe CE |
|-----------------|:------:|----------------------------|:---------:|
| `mesma_regiao`  | × 1,0  | Sem acréscimo              | CE-D1     |
| `outra_regiao`  | × 1,5  | +50 %                      | CE-D2     |
| `internacional` | × 2,0  | +100 %                     | CE-D3     |

---

## Estratégia de Testes

### Cobertura implementada

| Técnica                  | Casos | Localização no código              |
|--------------------------|:-----:|------------------------------------|
| Classes de equivalência  | 5     | `TestClassesEquivalencia`          |
| Valores limite           | 9     | `test_valores_limite` (parametrize)|
| Tabela de decisão        | 6     | `test_tabela_decisao` (parametrize)|
| Entradas inválidas       | 2     | `TestEntradasInvalidas`            |
| Property-based testing   | 3     | `test_prop_*` (Hypothesis)         |
| **Total**                | **25**|                                    |

### Valores limite por fronteira

| Fronteira | Abaixo  | Exato   | Acima   | Obs.                    |
|-----------|:-------:|:-------:|:-------:|-------------------------|
| 1 kg      | 0,999   | 1,000   | 1,001   | —                       |
| 5 kg      | 4,999   | 5,000   | 5,001   | —                       |
| 20 kg     | 19,999  | 20,000  | 20,001  | 20,001 → `ValueError`   |

### Propriedades verificadas (Hypothesis)

| ID | Propriedade                                                       | Exemplos |
|----|-------------------------------------------------------------------|:--------:|
| P1 | Frete nunca é negativo                                            | 300      |
| P2 | Pedido > R$ 200 sempre retorna `0.0`                              | 200      |
| P3 | `internacional ≥ outra_regiao ≥ mesma_regiao` para qualquer entrada | 300    |

### Fixtures (conftest.py)

| Fixture          | Valor      | Propósito                              |
|------------------|:----------:|----------------------------------------|
| `valor_normal`   | R$ 100,00  | Pedido que não aciona frete grátis     |
| `valor_gratis`   | R$ 250,00  | Pedido que aciona frete grátis         |
| `destinos_validos`| lista     | Conjunto dos três destinos aceitos     |