# ⚖️ Pokémon Balance Dashboard

Este projeto é um **dashboard interativo em Streamlit** para análise de balanceamento dos tipos de Pokémon, utilizando dados armazenados em um banco SQLite.  
O objetivo é explorar diferentes formas de calcular o **Base Stat Total (BST)** e entender como cada método altera a percepção de força entre os tipos.

---

## 🚀 Funcionalidades

- **Filtro de Lendários e Míticos**  
  Permite incluir ou excluir Pokémon lendários e míticos da análise.

- **Método A – Duplicar**  
  Cada Pokémon contribui com seu BST inteiro em todos os tipos que possui.  
  ➝ Favorece tipos comuns como secundários (ex.: Poison).

- **Método B – Dividir**  
  O BST é dividido igualmente entre os tipos do Pokémon.  
  ➝ Destaca tipos com Pokémon naturalmente fortes (ex.: Dragon, Steel).

- **Tipo Principal**  
  Considera apenas o primeiro tipo listado para cada Pokémon.  
  ➝ Mostra a força dos tipos primários (ex.: Grass dispara na frente).

- **Validação dos Dados**  
  - Quantidade de Pokémon únicos por tipo  
  - Comparação entre os métodos (Duplicar vs Dividir)  
  - Gráfico de slope chart mostrando mudanças de ranking entre os métodos

- **KPIs principais**  
  - Total de Pokémon únicos  
  - Média geral de BST por método

---

## 📊 Visualizações

- Gráficos de barras com linha de referência da média geral  
- Boxplots mostrando a distribuição do BST por tipo  
- Top 5 tipos mais fortes em cada método  
- Slope chart para comparar mudanças de ranking entre Método A e Método B

---

## 🛠️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)  
- [Streamlit](https://streamlit.io/)  
- [Plotly Express](https://plotly.com/python/plotly-express/)  
- [SQLite](https://www.sqlite.org/)  
- [Pandas](https://pandas.pydata.org/)

---
Você pode conferir o funcionamento do dashboard no seguinte link: [Dashboard_Pokemon_Balance](https://dados-com-pokemons-dashboard-analise-de-zyrv.onrender.com)
