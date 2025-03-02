import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Rendimiento de los estudiantes",
                   page_icon=":student:",
                   layout="wide"
)

df = pd.read_csv('StudentsPerformance G5-G6 - StudentsPerformance G5-G6.csv')

# ---- Calculo de notas (letras)
df['average'] = round((df['math score'] + df['reading score'] + df['writing score']) / 3)

def nota_a_letra(nota):
    if nota >= 90:
        return "A"
    elif nota >= 80:
        return "B"
    elif nota >= 70:
        return "C"
    elif nota >= 60:
        return "D"
    else:
        return "F"

df['nota'] = df['average'].apply(nota_a_letra)

# ---- SIDEBAR
st.sidebar.header("Filtros")
preparacion = st.sidebar.multiselect(
    "Escoja el nivel de eduación:",
    options=df['test preparation course'].unique(),
    default=df['test preparation course'].unique()
    )
df_selection = df[df['test preparation course'].isin(preparacion)]

# ---- Grafico
parental_df = df_selection['parental level of education'].value_counts().reset_index()
parental_df.columns = ['Nivel Educativo', 'conteo']
parental_df.sort_values('conteo', ascending=True, inplace=True)

fig1 = px.bar(parental_df, x='Nivel Educativo', y= 'conteo')
fig1.update_layout(
    xaxis_title="", 
    yaxis_title="",
    )
fig1.update_traces(
    marker=dict(color='RebeccaPurple'),
    text=parental_df[ 'conteo'], 
    textposition='outside' 
)

# ---- Grafico 2
notas_df = df_selection['nota'].value_counts().reset_index()
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

nota_prom = int(df['average'].mean())

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

