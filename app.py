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
    )
fig2.update_traces(
    marker=dict(color='RebeccaPurple'),
    text=notas_df[ 'conteo'], 
    textposition='outside' 
)

# ---- Tabla
fig3 = go.Figure()

fig3.update_layout()


#---- PAGINA PRINCIPAL ----
st.title(":male-student: Rendimiento de los estudiantes")
st.markdown("##")

#---- NOTAS ESTUDIANTES ----

nota_prom = int(df['average'].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Nota promedio")
    st.subheader(str(nota_prom) + "/100")
with middle_column:
    st.subheader("Notas")
    st.table(notas_df)
    st.markdown("##")

with right_column:
    st.plotly_chart(fig2)

st.markdown("---")


