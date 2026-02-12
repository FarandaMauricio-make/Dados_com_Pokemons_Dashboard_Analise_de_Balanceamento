# ⚖️ Pokémon Balance Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple)
![SQLite](https://img.shields.io/badge/Database-SQLite3-green)

> **Dashboard de Inteligência de Dados** focado em resolver um viés estatístico comum em jogos: como avaliar a força de um Tipo (Ex: Fogo) quando muitos Pokémon possuem dois tipos? O projeto compara metodologias de agregação para revelar o verdadeiro "Rei do Meta".

## 📋 Sobre o Projeto

Este painel utiliza o Data Warehouse (`pokemon_dw.db`) para analisar o **BST (Base Stat Total)** dos Pokémon.

O diferencial deste projeto é a **honestidade estatística**. A maioria das análises apenas duplica os dados de Pokémon com tipo duplo (contando um Charizard inteiramente para Fogo e inteiramente para Voador). Este dashboard propõe uma abordagem alternativa ("Split Weight") para corrigir distorções causadas por tipos que aparecem frequentemente como secundários (como Veneno/Poison).

---

## 🧠 Metodologia Analítica

O dashboard confronta três visões distintas sobre os dados:

### 1. Método A: Duplicação (Viés de Frequência)
* **Lógica:** Se um Pokémon é *Fogo/Voador* com 500 BST, ele conta 500 para a média de Fogo e 500 para Voador.
* **Resultado:** Favorece tipos que são comuns como "coadjuvantes" (secundários), inflando artificialmente a média de tipos como **Poison**.

### 2. Método B: Divisão Proporcional (Poder Real)
* **Lógica:** O BST é dividido. O mesmo Pokémon conta 250 para Fogo e 250 para Voador.
* **Resultado:** Revela a "densidade de poder". Tipos raros mas fortes, como **Dragon** e **Steel**, assumem a liderança.

### 3. Tipo Principal (Foco no Design)
* **Lógica:** Ignora o tipo secundário.
* **Resultado:** Mostra como os designers do jogo equilibram os Pokémon baseados em sua identidade primária (Ex: **Grass** sobe no ranking devido aos iniciais).

---

## 🚀 Funcionalidades

* **Slope Chart (Gráfico de Inclinação):** Uma visualização avançada que conecta o Ranking A ao Ranking B, mostrando visualmente quais tipos "caem" ou "sobem" dependendo da metodologia usada.
* **Filtro de Lendários:** Checkbox na sidebar para incluir ou excluir Pokémon Lendários/Míticos, permitindo analisar apenas o cenário competitivo padrão.
* **Paleta de Cores Consistente:** Mapeamento de cores fixo para garantir que o tipo "Fogo" tenha a mesma cor em todos os gráficos e abas.
* **Validação de Dados:** Uma aba dedicada para transparência, mostrando tabelas brutas e contagens.

---

## 🛠️ Tecnologias Utilizadas

* **[Streamlit](https://streamlit.io/):** Front-end e controle de abas.
* **[Plotly Express](https://plotly.com/python/):** Gráficos interativos (Boxplot, Bar Chart, Slope Chart).
* **[Pandas](https://pandas.pydata.org/):** Manipulação de dados (`explode`, `groupby`, `merge`).
* **[SQLite3](https://www.sqlite.org/):** Fonte de dados relacional.

---

## 📦 Como Rodar o Projeto

### Pré-requisitos
⚠️ **Importante:** Você precisa ter o arquivo `pokemon_dw.db` na raiz do projeto (gerado pelo script de ETL).

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/pokemon-balance.git](https://github.com/SEU-USUARIO/pokemon-balance.git)
    cd pokemon-balance
    ```

2.  **Instale as dependências:**
    ```bash
    pip install streamlit pandas plotly
    ```

3.  **Execute o Dashboard:**
    ```bash
    streamlit run Pokemon_Balance.py
    ```

---

## 📂 Estrutura de Arquivos

## 📊 Principais Insights

Ao navegar pelas abas, os dados contam a seguinte história:

1.  **A Ilusão do Veneno:** No *Método A*, Poison parece muito forte. No *Método B*, ele cai drasticamente. Isso prova que Poison é usado pelos designers do jogo como um "tipo de preenchimento" secundário para muitos Pokémon.
2.  **A Supremacia dos Dragões:** Independente do método, Dragões mantêm médias altíssimas, confirmando seu status de "Boss Monsters" no design do jogo.
3.  **O Equilíbrio do Aço:** Steel é o tipo defensivo definitivo, competindo topo a topo com Dragão quando removemos a duplicidade de dados.

---

## 🤝 Contribuição

Sugestões para análise de Gerações (Gen 1 vs Gen 9)?

1.  Faça um Fork.
2.  Crie sua Feature Branch.
3.  Commit e Push.
4.  Abra um Pull Request.

---

**Balanced, as all things should be.** ⚖️

Você pode conferir o funcionamento do dashboard no seguinte link: [Análise de Balanceamento dos Pokémon](https://dados-com-pokemons-dashboard-analise-de-zyrv.onrender.com)
