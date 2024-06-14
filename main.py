import pandas as pd
import random
import os
import time
import matplotlib.pyplot as plt
data = pd.read_csv("./CSV Rotas - Base de Dados.csv")
data.head()

#Criando os diretorios de logs
def criar_diretorios(caminho):
    os.makedirs(caminho, exist_ok=True)
    


timestamp_atual = time.time()
criar_diretorios('logs')
criar_diretorios(f"logs/{timestamp_atual}-geracao")
criar_diretorios(f"logs/{timestamp_atual}-geracao/filhos")
criar_diretorios(f"logs/{timestamp_atual}-geracao/mutacoes")
criar_diretorios(f"logs/{timestamp_atual}-geracao/pais")
criar_diretorios(f"logs/{timestamp_atual}-geracao/populacoes")
criar_diretorios(f"logs/{timestamp_atual}-geracao/melhores-individuos")


def calcular_fitness(rota):
    distancia_total = 0.0
    for i in range(len(rota) - 1):
        origem = rota[i]
        destino = rota[i + 1]
        distancia_total += data.loc[origem, destino]    
    return round(distancia_total, 3)


def selecao_por_torneio(populacao, tamanho_torneio):
    nova_populacao = []
    torneio = random.sample(populacao, tamanho_torneio)
    torneio.sort(key=lambda x: calcular_fitness(x))
    melhor_individuo = torneio[0]
    nova_populacao.append(melhor_individuo)
    return nova_populacao


#Pegando as localidades e setando a coluna 0 como index
localidades = data.columns[1:].tolist()


data.set_index(data.columns[0], inplace=True)


novo_df = pd.DataFrame(columns=data.columns)
for localidade in localidades:
    if localidade in data.index:
        novo_df = pd.concat([novo_df, data.loc[[localidade]]], axis=0)
novo_df.head()


def save_log(file_name,individuos):
        with open(f"./logs/{timestamp_atual}-geracao/{file_name}.txt","w") as file:
            for i in individuos:
                fitnessCALC = calcular_fitness(i)
                file.write(str(fitnessCALC) + " "+', '.join(i) + '\n')

def individuo_ja_existe(pais, individuo):
    return individuo in pais

def selecao_pais(data, qtd_pais = 2, tamanho_torneio = 5):
    pais = []
    for i in range(qtd_pais):
        novo_individo = selecao_por_torneio(data, tamanho_torneio)
        while individuo_ja_existe(pais, novo_individo):
            novo_individo = selecao_por_torneio(data, tamanho_torneio)
        pais.extend(novo_individo)
    return pais

def crossover_ordem(pai1, pai2):
    tamanho = len(pai1)
    filho1, filho2 = [None]*tamanho, [None]*tamanho

    # 'Faminas' deve ser o primeiro e o último ponto
    filho1[0], filho1[-1] = 'Faminas', 'Faminas'
    filho2[0], filho2[-1] = 'Faminas', 'Faminas'

    # Escolher dois pontos de crossover entre 1 e tamanho-2
    ponto1, ponto2 = sorted(random.sample(range(1, tamanho-1), 2))
    # Copiar segmento de pai1 para filho1 e de pai2 para filho2
    filho1[ponto1:ponto2] = pai1[ponto1:ponto2]
    filho2[ponto1:ponto2] = pai2[ponto1:ponto2]
    def preencher_filho(filho, pai):
        for elemento in pai:
            if elemento in filho:
                continue  # Se o elemento já existe em lista2, passa para o próximo elemento
            # Procura a primeira posição None em lista2
            for i in range(len(filho)):
                if filho[i] is None:
                    filho[i] = elemento
                    break  # Atribui o elemento e sai do loop
        if(None in filho):
            for elemento in pai:
                if elemento not in filho:
                    index_none = filho.index(None)
                    filho[index_none] = elemento

    # Preencher os filhos com os genes dos outros pais
    preencher_filho(filho1, pai2)
    preencher_filho(filho2, pai1)
    if None in filho1 or None in filho2:
        # Se algum filho contém None, chamar crossover_ordem novamente para gerar novos filhos
        return crossover_ordem(pai1, pai2)
    else:
        return filho1, filho2


def mutacao(filho, taxa_mutacao=0.1):
    # Verifica se a mutação ocorrerá com base na taxa de mutação
    if random.random() < taxa_mutacao:
        # Escolhe dois índices aleatórios entre 2 e 18
        indice1 = random.randint(2, 18)
        indice2 = random.randint(2, 18)
        
        # Garante que os índices sejam diferentes
        while indice1 == indice2:
            indice2 = random.randint(2, 18)
        
        # Troca os genes nos índices selecionados
        filho[indice1], filho[indice2] = filho[indice2], filho[indice1]
    
    return filho

def substituicao_eletista(p,f):
    fitness_populacao = [(individuo, calcular_fitness(individuo)) for individuo in p]
    # Ordena a população com base no fitness (do maior para o menor)
    fitness_populacao.sort(key=lambda x: x[1], reverse=True)
    num_melhores = 25
    melhores_individuos = [individuo for individuo, fitness in fitness_populacao[:num_melhores]]
    # Seleciona os 25 piores indivíduos
    piores_individuos = [individuo for individuo, fitness in fitness_populacao[num_melhores:]]

    for filho in f:
        indice_substituir = random.choice(range(len(piores_individuos)))
        piores_individuos[indice_substituir] = filho
    # Combina os melhores indivíduos com os piores indivíduos (alguns substituídos pelos filhos)
    nova_populacao = melhores_individuos + piores_individuos
    return nova_populacao

def melhor_individo_populacao(populacao):
    fitness_populacao = [(individuo, calcular_fitness(individuo)) for individuo in populacao]
    fitness_populacao.sort(key=lambda x: x[1], reverse=True)
    return fitness_populacao[-1]

#Criando o grade While responsavel por gerar as populacoes

#Iniciando a populacao
tamanho_populacao = 50
populacao = []

localidades = [loc for loc in localidades if loc != 'Faminas']  
populacao = []

for _ in range(tamanho_populacao):
    rota = ['Faminas'] + random.sample(localidades, len(localidades)) + ['Faminas']
    populacao.append(rota)

save_log('populacoes/0-populacao',populacao)
melhor_individuo = [None,1000]
melhores_individuos = []
geracoes = 0 
while melhor_individuo[-1] > 23.5: 
    #Pegando os pais para o cruzamento
    pais = []
    pais = selecao_pais(populacao)
    save_log(f"pais/{geracoes}-geracao",pais)
    #Gerando os filhos apartir dos pais
    filhos = []
    for i in range(0, len(pais), 2):  # iterar com passo 2
        filho1, filho2 = crossover_ordem(pais[i], pais[i+1])
        filhos.append(filho1)
        filhos.append(filho2)
    save_log(f"filhos/{geracoes}-geracao",filhos)

    #Aplicando a mutacao nos filhos
    for i, filho in enumerate(filhos):
        filhos[i] = mutacao(filho)
    save_log(f"mutacoes/{geracoes}-mutacao",filhos)

    #Incluindo os filhos na populacao de forma elitista 
    populacao = substituicao_eletista(populacao,filhos)
    save_log(f"populacoes/{geracoes+1}-populacao",populacao)
    melhores_individuos.append(melhor_individo_populacao(populacao))
    melhor_individuo_geracao = melhor_individo_populacao(populacao)
    if( melhor_individuo_geracao[-1] < melhor_individuo[-1]):
        melhor_individuo = melhor_individuo_geracao
    
    print(f"Geracao: {geracoes} - Menor Rota: {melhor_individuo[-1]}")
    geracoes = geracoes + 1

"""     
def encontrar_melhor_de_todas_geracoes(individuos):
    individuos_ordenados = sorted(individuos, key=lambda x: x[1])
    return individuos_ordenados[0]

melhor_individuo = encontrar_melhor_de_todas_geracoes(melhores_individuos) """

# Imprime o melhor indivíduo
print("Melhor Rota:", melhor_individuo)

with open(f"./logs/{timestamp_atual}-geracao/melhores-individuos/melhores.txt","w") as file:
    for element in melhores_individuos:
        file.write(f"{i} \n")
        file.write(f"\n\n-------Melhor individuo-------\n\n {element} \n")


# Extrair os scores para plotagem
scores = [individuo[1] for individuo in melhores_individuos]
plt.plot(scores)
plt.title('Evolução dos Melhores Indivíduos')
plt.xlabel('Geração')
plt.ylabel('Score')
plt.show()
