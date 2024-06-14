<h1>Projeto de Algoritmo Genético para o Problema do Caixeiro Viajante (TSP)</h1>

  <div>
    <h2>Visão Geral
    <h3>Este projeto utiliza um Algoritmo Genético para resolver o Problema do Caixeiro Viajante (TSP) com dados recolhidos em sala de aula referentes a pontos de interesse da cidade de Muriaé (MG) para a realização do trabalho, 
      visando encontrar a rota mais curta que visita todas as localidades uma vez e retorna à origem.</h3>
  </div>

  <h2>Estrutura do Projeto</h2>
  <ul>
    <li>CSV Rotas - Base de Dados.csv: Matriz de distâncias entre localidades.</li>
    <li>main.py: Script principal do algoritmo genético.</li>
    <li>logs/: Diretório contendo os logs de cada geração.</li>
  </ul>

  <h2>Estrutura dos Logs</h2>
  <ul>
    <li>logs/{timestamp}-geracao/: Diretório principal de cada geração.
      <ul>
        <li>filhos/: Logs dos filhos gerados.</li>
        <li>mutacoes/: Logs das mutações aplicadas.</li>
        <li>pais/: Logs dos pais selecionados.</li>
        <li>populacoes/: Logs da população de cada geração.</li>
        <li>melhores-individuos/: Logs dos melhores indivíduos de todas as gerações.</li>
      </ul>
    </li>
  </ul>

  <h2>Etapas do Algoritmo</h2>
  <ol>
    <li>Inicialização da População: Gera uma população inicial de rotas aleatórias.</li>
    <li>Cálculo de Fitness: Calcula a distância total de cada rota.</li>
    <li>Seleção de Pais: Seleciona pares de pais usando torneio.</li>
    <li>Crossover: Gera filhos a partir dos pais selecionados.</li>
    <li>Mutação: Aplica mutações aos filhos.</li>
    <li>Substituição: Substitui indivíduos na população usando elitismo.</li>
    <li>Log das Gerações: Salva logs das populações, pais, filhos, mutações e melhores indivíduos.</li>
    <li>Iteração: Repete as etapas 3 a 7 por um número definido de gerações.</li>
    <li>Resultado: Identifica e salva o melhor indivíduo de todas as gerações.</li>
  </ol>

  <h2>Como executar</h2>
  <h3>1. Instale as dependencias com o comando no terminal (É necessario ter python instalado)</h3>

      pip install pandas matplotlib 

  <h3>2. Execute o Script com python</h3>

      python main.py
