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
    ":open_book: Preparación previa",
    options=df['Preparación'].unique(),
    default=sorted(df['Preparación'].unique())
    )
notas = st.sidebar.multiselect(
    ":pencil: Nota",
    options=df['Nota'].unique(),
    default=sorted(df['Nota'].unique())
    )
nivel_edu = st.sidebar.multiselect(
    ":mortar_board: Nivel educativo de los padres",
    options=df['Nivel educativo de los padres'].unique(),
    default=sorted(df['Nivel educativo de los padres'].unique())
    )
almuerzo = st.sidebar.multiselect(
    ":bowl_with_spoon: Almuerzo",
    options=df['Almuerzo'].unique(),
    default=sorted(df['Almuerzo'].unique())
    )

df_selection = df[df['Preparación'].isin(preparacion) & df['Nota'].isin(notas) & df['Nivel educativo de los padres'].isin(nivel_edu) & df['Almuerzo'].isin(almuerzo)]

# ---- Calculos

nota_prom = int(df_selection['Promedio'].mean(0))

diccionario = {'Completada':1, 'Ninguna':0}     # Preparación a binario para tasas de conversión
binario = df['Preparación'].map(diccionario)
df_selection['Preparación_bin'] = binario

# ---- Colores
azul1 = 'rgba(0, 104, 201, 1)'
azul2 = 'rgba(131, 201, 255, 1)'

# ---- Grafico 1
notas_df = df_selection['Nota'].value_counts().reset_index()
notas_df.columns = ['Nota', 'conteo']
notas_df.sort_values('Nota', inplace=True)

fig1 = px.bar(notas_df, x='Nota', y= 'conteo')
fig1.update_layout(
    xaxis_title="", 
    yaxis_title="",
    height=380,
    margin=dict(l=0, r=0, t=0, b=0)
    )
fig1.update_traces(
    marker=dict(color=azul2),
    text=notas_df[ 'conteo'], 
    textposition='outside' 
)

# ---- Grafico 2
fig2 = px.histogram(df_selection, y="Nota", color="Preparación",
    category_orders={"Nota": ['A', 'B', 'C', 'D', 'F']}, 
    barnorm='percent',
    height=300
)
fig2.update_layout(
    legend_title_text='Curso de Preparación',
    legend=dict(
        orientation="h",
        y=1.2,
        xanchor="center",
        x=0.5,
        title=''
    ),
    xaxis=dict(
        title='Porcentaje'),
    xaxis_ticksuffix="%",
    yaxis_title='',
    margin=dict(l=0, r=0, t=0, b=0)
)

# ---- Grafico 3
grupo = df_selection.groupby('Nivel educativo de los padres')['Preparación_bin'].mean().mul(100).rename('tasa_conv1').reset_index()
orden_categorias = ['Algun estudio de secundaria', 'Escuela secundaria', 'Algun estudio universitario', 'Título de asociado', 'Licenciatura', 'Título de maestría']

fig3 = px.bar(
    grupo,
    x='Nivel educativo de los padres',
    y='tasa_conv1',
    text='tasa_conv1',
    category_orders={"Nivel educativo de los padres": orden_categorias},
    height=400
)
fig3.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
fig3.update_layout(
    xaxis_title='',
    yaxis_title='Tasa de conversión (%)',
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0)
)

# ---- Grafico 4
tc = df_selection.groupby(['Nivel educativo de los padres', 'Almuerzo'])['Preparación_bin'].mean().mul(100).rename('tasa_conv2').reset_index()

fig4 = px.scatter(
    tc,
    x='tasa_conv2',
    y='Nivel educativo de los padres',
    color='Almuerzo',
    title='',
    labels={'tasa_conv2': 'Tasa de conversión (%)', 'Nivel_educativo': ''},
    range_x=[0, 100],
    category_orders={"Nivel educativo de los padres": orden_categorias},
    height=350
    )
fig4.update_layout(
        legend=dict(
        orientation="h",
        y=1.15,
        xanchor="center",
        x=0.5,
        title=''),
        margin=dict(l=0, r=0, t=50, b=0)
    )
# ---- Grafico 5

fig5 = px.box(
    df_selection,
    x='Nivel educativo de los padres',
    y='Promedio',
    color='Preparación',
    title='',
    labels={'Promedio': 'Nota', 'Nivel educativo de los padres': ''},
    category_orders={"Nivel educativo de los padres": orden_categorias}
)
fig5.update_layout(
        legend=dict(
        orientation="h",
        y=1.1,
        xanchor="center",
        x=0.5,
        title=''),
        margin=dict(l=0, r=0, t=0, b=0)
    )
# ---- Tabla 1
data = {
    'A': ['APROBADO', '100% - 90%'],
    'B': ['APROBADO', '89% - 80%'],
    'C': ['APROBADO', '79% - 70%'],
    'D': ['APROBADO', '69% - 60%'],
    'F': ['SUSPENDIDO', '59% - 0%']
}
data_notas = pd.DataFrame(data)

fig11 = go.Figure(data=go.Table(
    columnwidth=10,
    header=dict(values=list(data_notas.columns),
                align='center',
                line_width=2,
                height=35,
                font=dict(color='white', size=20)),
    cells=dict(values=data_notas.T.values,
               align='center',
               line_width=2,
               height=30,
               font=dict(color='white', size=18))
))

fig11.update_layout(
    autosize=False,
    width=400,
    height=100,
    margin=dict(l=0, r=0, t=0, b=0)
    )


#---- PAGINA PRINCIPAL ----
st.title(":male-student: Rendimiento de los estudiantes")
st.markdown("##")

# ---- Distintas tabs
tab1, tab2 = st.tabs(["Dashboard", "Base de datos"])

# ---- Tab 1 ----
with tab1:

    # ---- Notas ----
    
    left_column1, middle_column1, right_column1 = st.columns([2.5, 0.5, 3])
    with left_column1:
        st.metric(label="Nota promedio", value=nota_prom, delta=(nota_prom - int(df['Promedio'].mean(0))))
        st.markdown("---") 
        
        st.markdown("### Análisis de examenes 1000 estudiantes de G5 y G6"
        "\nUtilizaremos la nota promedio de cada estudiante obtenida en sus examenes de:"
        "\n - Lectura"
        "\n - Escritura"
        "\n - Matemática")
        
    with right_column1:
        st.plotly_chart(fig11)
        st.markdown("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Distribución de la notas promedio de los estudiantes")
        st.plotly_chart(fig1)
    
    # ---- Preparación ----
    
    with st.container():
        st.markdown("---") 
        st.subheader("Preparación previa de los estudiantes")
        left_column2, middle_column2, right_column2 = st.columns([1.5, 1.3, 1.7], gap='large')
        with left_column2:
            st.markdown("---")
            st.markdown("Los datos muestran que los estudiantes que participaron en el curso de preparación obtuvieron resultados significativamente mejores en los exámenes.")
            st.markdown("---")
            st.markdown("El nivel educativo de los padres también influye en la preparación de los estudiantes. "
            "\n\nAquellos con padres que tienen un título universitario o superior tienden a tener mejores resultados.")
        with middle_column2:
            st.markdown("---") 
            st.markdown('&emsp;&emsp;Distribución de notas por preparación previa')
            st.plotly_chart(fig2)
        with right_column2:
            st.markdown("---") 
            st.write("Tasa de estudiantes que se preparan para el examen\nsegún el nivel educativo de los padres")
            st.plotly_chart(fig3)

    # ---- Preparación y Almuerzo

    with st.container():
        st.markdown("---") 
        st.subheader("Impacto de la Preparación y el Almuerzo")
        left_column3, middle_column3, right_column3 = st.columns([1.2, 1.8, 1.9], gap='medium')
        with left_column3:
            st.markdown("---")
            st.markdown("Se observan las concentraciones de estudiantes que completaron la preparación y los que no según el nivel educativo de los padres, por su nota promedio.")
            st.markdown("---")
            st.markdown("Además observamos el impacto de los tipos de almuerzo en la preparación previa según el nivel educativo de los padres.")
        with middle_column3:
            st.markdown("---") 
            st.write("Notas segun el Nivel educativo de los padres y su Preparación")
            st.plotly_chart(fig5)
        with right_column3:
            st.markdown("---") 
            st.write("Tasa de conversión para Nivel educativo de los padres y Almuerzo")
            st.plotly_chart(fig4)

# ---- Tab 2 ----
with tab2:
    st.dataframe(df_selection)