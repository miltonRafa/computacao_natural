# Computação Natural — algoritmo em `algoritmo_genetico.py`

Resumo
------
Este repositório contém uma implementação simples de um algoritmo genético em Python (arquivo `algoritmo_genetico.py`). O objetivo do código é otimizar a função f(x) = x * sin(x) em um domínio inteiro [valor_min, valor_max] usando uma população de indivíduos representados por valores numéricos reais/inteiros.

Descrição do algoritmo
----------------------
- Inicialização: gera uma população inicial de tamanho `tamanho_populacao` com valores aleatórios entre `valor_min` e `valor_max`.
- Fitness: calculado por f(x) = x * sin(x).
- Seleção: torneio entre 4 indivíduos (participantes sorteados aleatoriamente) para escolher cada par de pais.
- Crossover: combinação aritmética (filho = alfa*pai1 + (1-alfa)*pai2) aplicada com probabilidade `pc`.
- Mutação: mutação aditiva (±teta) aplicada com probabilidade `pm`.
- Elite: os 2 melhores indivíduos são preservados entre gerações.

Como o experimento é realizado
------------------------------
O script executa 10 blocos (loop externo), cada bloco realiza `n_runs` (100) experimentos. Para cada run:
- Gera-se uma nova população inicial aleatória.
- Executa-se o algoritmo (função `top_1`) que roda o processo evolutivo e retorna o melhor `top_fitness` e `top_individuo` para aquela run.
- Um contador acumula quantas runs, dentre as `n_runs`, atigiram um fitness mínimo desejado (no código atual, `>= 960000.0`).
Ao final de cada bloco são impressas as estatísticas: quantas runs atingiram o limiar e a porcentagem correspondente.

Como rodar
----------
Recomendado: usar um ambiente virtual Python.

1. Criar e ativar venv (Linux/macOS):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt # opcional, ver abaixo
```

2. Instalar dependências mínimas (opcional):

```bash
pip install sympy
```

3. Rodar o script:

```bash
python algoritmo_genetico.py
```

Parâmetros importantes (no arquivo `algoritmo_genetico.py`)
----------------------------------------------
- `valor_min`, `valor_max`: domínio dos indivíduos.
- `tamanho_populacao`: número de indivíduos por população.
- `teta`: magnitude da mutação (atualmente definido como 5% do intervalo).
- `pm`: probabilidade de mutação.
- `pc`: probabilidade de crossover.
- `n_runs`: número de runs por bloco (cada run cria uma nova população inicial).
- Limiar de fitness: atualmente usado `>= 960000.0` para contar runs bem-sucedidas.

Interpretação dos resultados
---------------------------
O script imprime, por bloco de `n_runs`, quantas runs atingiram o limiar desejado. Isso mede a efetividade do algoritmo sob a configuração atual de parâmetros (probabilidades, tamanho de população, magnitude de mutação). Ao variar cada parâmetro e repetir os experimentos, você pode estimar sensibilidade e robustez:

- Aumentar `tamanho_populacao` tende a melhorar cobertura do espaço e estabilidade, porém custa mais tempo.
- `pm` muito alto -> excesso de ruído; muito baixo -> pouca exploração.
- `pc` controla exploração por recombinação — ajustar conforme o problema.
- `teta` define passo da mutação; para busca fina, reduzi-lo progressivamente pode ajudar.

