import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd

# 1. Conexão com o banco de dados SQLite
conn = sqlite3.connect(r"G:\Meu Drive\Projetos\Poke_projeto\Pokemao\pokemon_dw.db")

# 2. Consulta SQL para montar o DataFrame
query = """
SELECT p.id, p.name, SUM(s.base_stat) AS bst,
       GROUP_CONCAT(pt.type_name) AS types,
       sp.is_legendary, sp.is_mythical
FROM pokemon p
JOIN pokemon_stats s ON p.id = s.pokemon_id
JOIN pokemon_types pt ON p.id = pt.pokemon_id
JOIN species sp ON p.id = sp.pokemon_id
GROUP BY p.id, p.name
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 3. Configuração da página no Streamlit
st.set_page_config(page_title="Pokémon Balance", layout="wide")
st.title("⚖️ Análise de Balanceamento de Pokémon")

# 4. Filtro para incluir/excluir Pokémon lendários e míticos
incluir_lendarios = st.sidebar.checkbox("Incluir Pokémon Lendários e Míticos", value=True)

df_filtrado = df.copy()
if not incluir_lendarios:
    df_filtrado = df_filtrado[df_filtrado["is_legendary"] == 0]

# 5. Preparação dos DataFrames auxiliares
df_tipos_explodido = df_filtrado.copy()
df_tipos_explodido["tipo"] = df_tipos_explodido["types"].str.split(",")
df_tipos_explodido = df_tipos_explodido.explode("tipo")

bst_por_tipo_duplo = (
    df_tipos_explodido.groupby("tipo")["bst"]
    .mean()
    .reset_index()
    .sort_values("bst", ascending=False)
)

df_tipos_dividido = df_filtrado.copy()
df_tipos_dividido["tipo"] = df_tipos_dividido["types"].str.split(",")
df_tipos_dividido["bst_por_tipo"] = df_tipos_dividido["bst"] / df_tipos_dividido["tipo"].str.len()
df_tipos_dividido = df_tipos_dividido.explode("tipo")

bst_por_tipo_B_df = (
    df_tipos_dividido.groupby("tipo")["bst_por_tipo"]
    .mean()
    .reset_index()
    .sort_values("bst_por_tipo", ascending=False)
)

df_filtrado["tipo_principal"] = df_filtrado["types"].str.split(",").str[0]
bst_por_tipo_principal = (
    df_filtrado.groupby("tipo_principal")["bst"]
    .mean()
    .reset_index()
    .sort_values("bst", ascending=False)
)

# ----------------- DEFINIÇÃO DE CORES -----------------
# Criar paleta de cores fixa para cada tipo
tipos_unicos = df_tipos_explodido["tipo"].unique()
cores = px.colors.qualitative.Set3
color_map = {tipo: cores[i % len(cores)] for i, tipo in enumerate(tipos_unicos)}
# ------------------------------------------------------

# 6. KPIs principais
total_pokemons = df["id"].nunique()
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pokémon únicos", total_pokemons)
col2.metric("Média Geral BST (Método A)", round(df_tipos_explodido["bst"].mean(), 2))
col3.metric("Média Geral BST (Método B)", round(df_tipos_dividido["bst_por_tipo"].mean(), 2))

# 7. Organização em abas para storytelling
tabA, tabB, tabC, tabVal = st.tabs([
    "Método A - Duplicar",
    "Método B - Dividir",
    "Somente Tipo Principal",
    "Validação"
])

# ----------------- MÉTODO A -----------------
with tabA:
    st.subheader("📊 Análises pelo Método A (Duplicar Status Base)")
    st.markdown("""
    Quando duplicamos o status base nos dois tipos, **Poison aparece como líder**.  
    Isso acontece porque Poison é muito comum como tipo secundário, então ganha força artificialmente.  
    Esse método mostra como a duplicação pode distorcer a percepção de balanceamento.
""")

    # Gráfico de barras (aplicando color_map)
    fig_bar_A = px.bar(bst_por_tipo_duplo, x="tipo", y="bst",
                       title="Média do Status Base por Tipo (Duplicar Status Base)",
                       labels={"bst": "Status Base Médio", "tipo": "Tipo"},
                       color="tipo", color_discrete_map=color_map)  # <- cores fixas
    fig_bar_A.add_hline(y=df_tipos_explodido["bst"].mean(), line_dash="dash", line_color="red", annotation_text="Média Geral")
    st.plotly_chart(fig_bar_A, use_container_width=True)

    # Boxplot (aplicando color_map)
    fig_box_A = px.box(df_tipos_explodido, x="tipo", y="bst",
                       title="Distribuição do Status Base por Tipo (Duplicar Status Base)",
                       labels={"bst": "Status Base", "tipo": "Tipo"},
                       color="tipo", color_discrete_map=color_map)  # <- cores fixas
    st.plotly_chart(fig_box_A, use_container_width=True)

    # Top 5 (aplicando color_map)
    fig_top5_A = px.bar(bst_por_tipo_duplo.head(5), x="tipo", y="bst",
                        title="Top 5 Tipos com Maior Status Base Médio (Duplicar Status Base)",
                        labels={"bst": "Status Base Médio", "tipo": "Tipo"},
                        color="tipo", color_discrete_map=color_map)  # <- cores fixas
    st.plotly_chart(fig_top5_A, use_container_width=True)

# ----------------- MÉTODO B -----------------
with tabB:
    st.subheader("📊 Análises pelo Método B (Dividir Status Base)")
    st.markdown("""
        Quando dividimos o status base entre os tipos, **Dragão e Steel lideram**.  
        Aqui vemos a força real desses tipos, que concentram Pokémons com BST naturalmente alto.  
        Os lendários têm impacto maior nesse método: sem eles, Steel ultrapassa Dragão por pouco.
    """)

    # Gráfico de barras (aplicando color_map)
    fig_bar_B = px.bar(bst_por_tipo_B_df, x="tipo", y="bst_por_tipo",
                       title="Média do Status Base por Tipo (Dividir Status Base)",
                       labels={"bst_por_tipo": "Status Base Médio", "tipo": "Tipo"},
                       color="tipo", color_discrete_map=color_map)  # <- cores fixas
    fig_bar_B.add_hline(y=df_tipos_dividido["bst_por_tipo"].mean(), line_dash="dash", line_color="red", annotation_text="Média Geral")
    st.plotly_chart(fig_bar_B, use_container_width=True)

    # Boxplot (aplicando color_map)
    fig_box_B = px.box(df_tipos_dividido, x="tipo", y="bst_por_tipo",
                       title="Distribuição do Status Base por Tipo (Dividir Status Base)",
                       labels={"bst_por_tipo": "Status Base", "tipo": "Tipo"},
                       color="tipo", color_discrete_map=color_map)  # <- cores fixas
    st.plotly_chart(fig_box_B, use_container_width=True)

    # Top 5 (aplicando color_map)
    fig_top5_B = px.bar(bst_por_tipo_B_df.head(5), x="tipo", y="bst_por_tipo",
                        title="Top 5 Tipos com Maior Status Base Médio (Dividir Status Base)",
                        labels={"bst_por_tipo": "Status Base Médio", "tipo": "Tipo"},
                        color="tipo", color_discrete_map=color_map)  # <- cores fixas
    st.plotly_chart(fig_top5_B, use_container_width=True)

# ----------------- TIPO PRINCIPAL -----------------
with tabC:
    st.subheader("📊 Análises considerando apenas o Tipo Principal")
    st.markdown("""
    Quando consideramos apenas o tipo primário, **Grass dispara na frente**.  
    Isso faz sentido: muitos Pokémon iniciais (starters) são Grass e têm BST razoável.  
    Mas ao incluir o segundo tipo, Grass perde força e outros tipos ganham destaque.
    """)

    # Gráfico de barras (aplicando color_map)
    fig_bar_principal = px.bar(
        bst_por_tipo_principal,
        x="tipo_principal",
        y="bst",
        title="Média do Status Base por Tipo Principal",
        labels={"bst": "Status Base Médio", "tipo_principal": "Tipo"},
        color="tipo_principal",
        color_discrete_map=color_map   # <- cores fixas
    )
    fig_bar_principal.add_hline(
        y=df_filtrado["bst"].mean(),
        line_dash="dash",
        line_color="red",
        annotation_text="Média Geral"
    )
    st.plotly_chart(fig_bar_principal, use_container_width=True)

    # Boxplot (aplicando color_map)
    fig_box_principal = px.box(
        df_filtrado,
        x="tipo_principal",
        y="bst",
        title="Distribuição do Status Base por Tipo Principal",
        labels={"bst": "Status Base", "tipo_principal": "Tipo"},
        color="tipo_principal",
        color_discrete_map=color_map   # <- cores fixas
    )
    st.plotly_chart(fig_box_principal, use_container_width=True)

    # Top 5 (aplicando color_map)
    fig_top5_principal = px.bar(
        bst_por_tipo_principal.head(5),
        x="tipo_principal",
        y="bst",
        title="Top 5 Tipos com Maior Status Base Médio (Tipo Principal)",
        labels={"bst": "Status Base Médio", "tipo_principal": "Tipo"},
        color="tipo_principal",
        color_discrete_map=color_map   # <- cores fixas
    )
    st.plotly_chart(fig_top5_principal, use_container_width=True)

# ----------------- VALIDAÇÃO -----------------
with tabVal:
    st.subheader("🔍 Validação dos Dados")
    st.markdown("""
    Esta aba mostra os bastidores da análise:
    - Quantidade de Pokémons únicos por tipo (considerando tipos primário e secundário juntos)  
    - Comparação entre os métodos (Duplicar vs Dividir)  

    Isso garante transparência e evita interpretações equivocadas.
    """)

    # Tabela contagem de Pokémons por tipo primário e secundário
    contagem_unica = (
        df_tipos_explodido.groupby("tipo")["id"]
        .nunique()
        .reset_index()
        .sort_values("id", ascending=False)
    )
    contagem_unica.columns = ["Tipo", "Quantidade de Pokémons por tipo primário e secundário"]
    st.dataframe(contagem_unica)

    # Tabela Comparação entre Método A (Duplicar) e Método B (Dividir)
    comparacao = pd.concat([
        bst_por_tipo_duplo.set_index("tipo")["bst"],
        bst_por_tipo_B_df.set_index("tipo")["bst_por_tipo"]
    ], axis=1)
    comparacao.columns = ["Média (Duplicar)", "Média (Dividir)"]
    st.dataframe(comparacao)

    # Ranking Método A (Duplicar)
    ranking_A = bst_por_tipo_duplo.reset_index(drop=True).reset_index()
    ranking_A["Método A"] = ranking_A.index + 1
    ranking_A = ranking_A[["tipo", "Método A"]]

    # Ranking Método B (Dividir)
    ranking_B = bst_por_tipo_B_df.reset_index(drop=True).reset_index()
    ranking_B["Método B"] = ranking_B.index + 1
    ranking_B = ranking_B[["tipo", "Método B"]]

    # Juntar rankings
    ranking_comp = pd.merge(ranking_A, ranking_B, on="tipo")

    # Slope chart (aplicando color_map)
    fig_slope = px.line(
        ranking_comp.melt(
            id_vars="tipo",
            value_vars=["Método A", "Método B"],
            var_name="Método",
            value_name="Ranking"
        ),
        x="Método",
        y="Ranking",
        color="tipo",
        line_group="tipo",
        markers=True,
        title="Mudança de Ranking por Tipo (Método A vs Método B)",
        color_discrete_map=color_map   # <- cores fixas
    )
    fig_slope.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_slope, use_container_width=True)