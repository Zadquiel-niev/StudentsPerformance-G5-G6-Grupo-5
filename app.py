import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Rendimiento de los estudiantes",
                   page_icon=":student:",
                   layout="wide"
)

df = pd.read_csv('https://raw.githubusercontent.com/Rickfer14/StudentsPerformance-G5-G6-Grupo-5/refs/heads/main/Rendimiento%20de%20los%20estudiantes%20de%205to%20y%206to%20grado.csv')

# ---- SIDEBAR
st.sidebar.header("Filtros")
preparacion = st.sidebar.multiselect(
    "Preparación previa",
    options=df['Preparación'].unique(),
    default=sorted(df['Preparación'].unique())
    )
notas = st.sidebar.multiselect(
    "Nota",
    options=df['Nota'].unique(),
    default=sorted(df['Nota'].unique())
    )
nivel_edu = st.sidebar.multiselect(
    "Nivel educativo de los padres",
    options=df['Nivel educativo de los padres'].unique(),
    default=sorted(df['Nivel educativo de los padres'].unique())
    )
almuerzo = st.sidebar.multiselect(
    "Almuerzo",
    options=df['Almuerzo'].unique(),
    default=sorted(df['Almuerzo'].unique())
    )

df_selection = df[df['Preparación'].isin(preparacion) & df['Nota'].isin(notas) & df['Nivel educativo de los padres'].isin(nivel_edu) & df['Almuerzo'].isin(almuerzo)]

# ---- Colores
azul1 = 'rgba(0, 104, 201, 1)'
azul2 = 'rgba(131, 201, 255, 1)'

# ---- Grafico 1
parental_df = df_selection['Nivel educativo de los padres'].value_counts().reset_index()
parental_df.columns = ['Nivel Educativo', 'conteo']
parental_df.sort_values('conteo', ascending=True, inplace=True)

fig1 = px.bar(parental_df, x='Nivel Educativo', y= 'conteo')
fig1.update_layout(
    xaxis_title="", 
    yaxis_title="",
    height=400,
    margin=dict(l=0, r=0, t=0, b=0),
    )
fig1.update_traces(
    marker=dict(color=azul2),
    text=parental_df[ 'conteo'], 
    textposition='outside' 
)

# ---- Grafico 2
notas_df = df_selection['Nota'].value_counts().reset_index()
notas_df.columns = ['Nota', 'conteo']
notas_df.sort_values('Nota', inplace=True)

fig2 = px.bar(notas_df, x='Nota', y= 'conteo')
fig2.update_layout(
    xaxis_title="", 
    yaxis_title="",
    height=380,
    margin=dict(l=0, r=0, t=0, b=0)
    )
fig2.update_traces(
    marker=dict(color='RebeccaPurple'),
    text=notas_df[ 'conteo'], 
    textposition='outside' 
)

# ---- Grafico 3

fig5 = px.histogram(df_selection, y="Nota", color="Preparación",
    category_orders={"Nota": ['A', 'B', 'C', 'D', 'F']}, 
    barnorm='percent',
    title="Distribución de Notas por Preparación previa")
fig5.update_layout(
    legend_title_text='Curso de Preparación',
    legend=dict(
        traceorder='reversed'
    ),
    xaxis=dict(
        title='Porcentaje'),
    xaxis_ticksuffix="%"
)

# ---- Tabla 1
fig3 = go.Figure(data=go.Table(
    columnwidth=10,
    header=dict(values=["Nota", "Porcentaje"],
                align='center',
                line_width=2,
                height=35,
                font=dict(color='white', size=20)),
    cells=dict(values=[notas_df['Nota'], (notas_df['conteo'] / len(df) * 100).round(1).astype(str) + '%'],
               align='center',
               line_width=2,
               height=30,
               font=dict(color='white', size=18))
))

fig3.update_layout(
    autosize=False,
    width=300,
    height=200,
    margin=dict(l=0, r=0, t=0, b=0)
    )

# ---- Tabla 2
fig4 = go.Figure(data=go.Table(
    columnwidth=10,
    header=dict(values=["Nivel Educativo", "Porcentaje"],
                align='center',
                line_width=2,
                height=35,
                font=dict(color='white', size=20)),
    cells=dict(values=[parental_df['Nivel Educativo'], (parental_df['conteo'] / len(df) * 100).round(1).astype(str) + '%'],
               align='center',
               line_width=2,
               height=30,
               font=dict(color='white', size=18))
))

fig4.update_layout(
    autosize=False,
    width=400,
    height=300,
    margin=dict(l=0, r=0, t=0, b=0)
    )

#---- PAGINA PRINCIPAL ----
st.title(":male-student: Rendimiento de los estudiantes")
st.markdown("##")

#---- NOTAS ESTUDIANTES ----

nota_prom = int(df_selection['Promedio'].mean())

left_column1, middle_column1, right_column1 = st.columns([2, 1.5, 2.5])
with left_column1:
    st.subheader("Nota promedio")
    st.subheader(str(nota_prom) + "/100")
with middle_column1:
    st.subheader("Notas")
    st.plotly_chart(fig3,use_container_width=False)
with right_column1:
    st.plotly_chart(fig2)

with st.container():
    st.markdown("---") 
    st.subheader("Nivel educativo de los padres")
    left_column2, middle_column2, right_column2 = st.columns([2, 1.5, 2.5])
    #with left_column2:

    with middle_column2:
        st.plotly_chart(fig4,use_container_width=False)
    with right_column2:
        st.plotly_chart(fig1)

with st.container():
    st.markdown("---") 
    st.subheader("Preparación previa")
    left_column3, middle_column3, right_column3 = st.columns([1.5, 2.5, 2.5])
    #with left_column3:
    with middle_column3:
        st.plotly_chart(fig5)
    #with right_column3:
