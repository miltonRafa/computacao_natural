# Importa bibliotecas necessárias
import random
import math
from sympy import true

valor_min = 0
valor_max = 1000000
# Define o valor de teta para mutação
teta = (valor_max - valor_min) * 0.05
# Define o tamanho da população
tamanho_populacao = 100
# Gera a população inicial com valores aleatórios
populacao_inicial = [random.randint(valor_min, valor_max) for _ in range(tamanho_populacao)]
# Probabilidade de mutação
pm = 0.8
# Probabilidade de crossover 
pc = 0.8

# Exibe a população inicial
print(populacao_inicial)

def calcula_fitness(populacao_inicial):
    # Calcula o fitness de cada indivíduo da população
    fitness_populacao_inicial = []
    for individuo in populacao_inicial:
        # f(x) = x * sin(x)
        fitness = individuo * math.sin(individuo)
        fitness_populacao_inicial.append(fitness) 
    return fitness_populacao_inicial

def individuos_fitness_print(populacao_inicial):
    # Calcula e imprime o fitness de cada indivíduo
    fitness_populacao_inicial = []
    for individuo in populacao_inicial:
        # f(x) = x * sin(x)
        fitness = individuo * math.sin(individuo)
        fitness_populacao_inicial.append(fitness) 
        print(f"Indivíduo: {individuo} -> Fitness: {fitness:.4f}")

# Comparando pares consecutivos de fitness
def selecao_pais(fitness_populacao_inicial, populacao_inicial):
    # Listas para armazenar os pais selecionados
    pai_1 = []
    pai_2 = []
    # Seleciona pares de pais usando torneio entre 4 indivíduos aleatórios
    for i in range(len(fitness_populacao_inicial)):
        # Sorteia 4 indivíduos diferentes (índices)
        n1 = random.randint(0, len(populacao_inicial)-1)
        n2 = random.randint(0, len(populacao_inicial)-1)
        n3 = random.randint(0, len(populacao_inicial)-1)
        n4 = random.randint(0, len(populacao_inicial)-1)
        # Garante que os 4 indivíduos sorteados são diferentes
        while populacao_inicial[n1] == populacao_inicial[n2] or \
            populacao_inicial[n1] == populacao_inicial[n3] or \
            populacao_inicial[n1] == populacao_inicial[n4] or \
            populacao_inicial[n2] == populacao_inicial[n3] or \
            populacao_inicial[n2] == populacao_inicial[n4] or \
            populacao_inicial[n3] == populacao_inicial[n4]:
            n1 = random.randint(0, len(populacao_inicial)-1)
            n2 = random.randint(0, len(populacao_inicial)-1)
            n3 = random.randint(0, len(populacao_inicial)-1)
            n4 = random.randint(0, len(populacao_inicial)-1)
        # Calcula o fitness dos 4 sorteados
        fit_1 = fitness_populacao_inicial[n1]
        fit_2 = fitness_populacao_inicial[n2]
        fit_3 = fitness_populacao_inicial[n3]
        fit_4 = fitness_populacao_inicial[n4]
        # Seleciona o melhor entre n1 e n2 para pai_1
        if fit_1 > fit_2:
            pai_1.append(populacao_inicial[n1])
        else:
            pai_1.append(populacao_inicial[n2])
        # Seleciona o melhor entre n3 e n4 para pai_2
        if fit_3 > fit_4:
            pai_2.append(populacao_inicial[n3])
        else:
            pai_2.append(populacao_inicial[n4])
    return pai_1, pai_2    

def top_2_indices(populacao_final):
    # Retorna os índices dos 2 indivíduos com maior fitness
    fit_pop = calcula_fitness(populacao_final)
    melhores_indices = sorted(range(len(fit_pop)), key=lambda i: fit_pop[i], reverse=True)[:2]
    return melhores_indices

def top_2_fit(populacao_final):
    # Retorna os 2 maiores valores de fitness
    fit_pop_final = calcula_fitness(populacao_final)
    return sorted(fit_pop_final, reverse=True)[:2]

def crossover(pai_1, pai_2, populacao_inicial):
    # Realiza o crossover preservando os 2 melhores indivíduos
    melhores_indices = top_2_indices(populacao_inicial)

    # Cria uma cópia da população para modificar
    populacao_final = populacao_inicial.copy()
    
    for i in range(len(populacao_final)):
        if i not in melhores_indices:
            valor = random.random()
            if valor < pc :
                alfa = random.random()
                filho = (alfa * pai_1[i]) + ((1 - alfa) * pai_2[i])
                populacao_final[i] = filho
            else:
                fit_pai1 = calcula_fitness(pai_1)
                fit_pai2 = calcula_fitness(pai_2)
                # Copia o indivíduo do pai com maior fitness
                if fit_pai1[i] > fit_pai2[i]:
                    populacao_final[i] = pai_1[i]
                else:
                    populacao_final[i] = pai_2[i]
            top_2_individuos = [populacao_final[i] for i in melhores_indices]
            # Aplica mutação
            populacao_final[i] = mutacao(populacao_final, i)
    return populacao_final, top_2_individuos

# Aplica mutação com probabilidade pm
def mutacao(populacao_final, i):
    if random.random() < pm:
        # Aplica uma pequena perturbação no indivíduo
        populacao_final[i] += random.uniform(-teta, teta)
        populacao_final[i] = max(valor_min, min(valor_max, populacao_final[i])) # retorna o valor máximo entre 0 e 100 garantindo que população não seja maior que valor_max
    return populacao_final[i]

def top_1(populacao_inicial):
    # Executa o loop evolutivo até o top 2 não mudar mais
    top_2_fit1 = top_2_fit(populacao_inicial)
    top_2_fit2 = [0]
    cont = 0
    fit_pop_inicial = calcula_fitness(populacao_inicial)
    while cont < 5:
        top_2_fit2 = top_2_fit1.copy()
        [pai_1, pai_2] = selecao_pais(fit_pop_inicial, populacao_inicial)
        populacao_final, top_2_individuos = crossover(pai_1, pai_2, populacao_inicial)
        top_2_fit1 = top_2_fit(populacao_final)
        populacao_inicial = populacao_final
        fit_pop_inicial = calcula_fitness(populacao_inicial)
        #print("\ntop 2 fitness: ", top_2_fit1)
        #print("top 2 fitness anterior: ", top_2_fit2)
        #print("top 2 indivíduos: ", top_2_individuos)
        #print("\n")
        if top_2_fit1 == top_2_fit2:
            # Guarda os 2 melhores indivíduos finais
            top_individuo = max(top_2_individuos)
            cont += 1
    return max(fit_pop_inicial), top_individuo, populacao_final

for i in range(10):
    contador = 0
    n_runs = 100
    for i in range(n_runs):
        # gera nova população aleatória para este experimento
        populacao_inicial_run = [random.randint(valor_min, valor_max) for _ in range(tamanho_populacao)]
        # Executa o algoritmo genético com a população desta iteração
        top_fitness, top_individuo, populacao_final = top_1(populacao_inicial_run)
        if top_fitness >= 960000.0:
            contador += 1
        # opção: mostrar progresso a cada 10 runs
        #if (i+1) % 10 == 0:
            #print(f"Completed {i+1}/{n_runs} runs")

    print(f"Conforme parâmetros atuais: {contador}/{n_runs} runs ({contador/n_runs*100:.1f}%) atingiram fitness >= 960000.0")

#top_fitness, top_individuo, populacao_final = top_1(populacao_inicial)
#print("\nMelhor indivíduo:", top_individuo)
#print("\nMelhor fitness:", top_fitness)
#print("\n")

#individuos_fitness_print(populacao_final)
