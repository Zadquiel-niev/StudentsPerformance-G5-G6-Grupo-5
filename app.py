import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Rendimiento de los estudiantes",
                   page_icon=":student:",
                   layout="wide"
)



df = pd.read_csv('StudentsPerformance G5-G6 - StudentsPerformance G5-G6.csv')

df['average'] = round((df['math score'] + df['reading score'] + df['writing score']) / 3)

st.dataframe(df)

# ---- Calculo los porcentajes 

frecuencia = df['parental level of education'].value_counts()
porcentaje = (frecuencia / len(df) * 100)
porcentajes_formateados = porcentaje.round(1).astype(str) + '%'

# ---- Grafico
counts = df["parental level of education"].value_counts().reset_index()
counts.columns = ["parental level of education", "Frecuencia"]
fig = px.bar(counts, x="parental level of education", y="Frecuencia")
fig.update_layout(
    xaxis_title="", 
    yaxis_title="",
    )
fig.update_traces(
    marker=dict(color='RebeccaPurple'),
    text=counts["Frecuencia"],  # añadir el texto encima de las barras
    textposition='outside'  # posición del texto fuera de las barras
)

#---- PAGINA PRINCIPAL ----
st.title(":student: Rendimiento de los estudiantes")
st.markdown("##")

#---- NOTAS ESTUDIANTES ----

nota_prom = int(df['average'].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Nota promedio:")
    st.subheader(str(nota_prom) + "/100")
with middle_column:
    st.subheader("Nivel académico de los padres:")
    st.table(porcentajes_formateados.reset_index().rename(columns={'index': "Nivel educativo",'Nivel educativo': 'Porcentaje'}))
    st.markdown("##")

with right_column:
    st.plotly_chart(fig)


