import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#Pestaña
st.set_page_config(page_title="Cats Analysis", page_icon="icono.png")

#Info principal
st.title('Análisis de Gatos en el Refugio Austin')
st.markdown("""Yareli Sugey Bravo Morales - S20006784\n
zS20006784@estudiantes.uv.mx""")

#Impotación del dataset
DATA_URL=('cats.csv')

#Para leer el dataset
@st.cache_resource
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data
data = load_data(11000)

#Sidebar
st.sidebar.image("logo.png")

#show just here <-
if st.sidebar.checkbox('Mostrar datos'):
    st.subheader('Datos')
    st.write(data)

query = st.sidebar.text_input("Buscar por tiempo en el refugio: ")
query = query.upper()
if st.sidebar.button('Buscar', key='button1'):
    # Filtra los datos que contienen la consulta ingresada
    results = data[data["time_shelter"].str.upper().str.contains(query)]
    # Muestra los resultados
    st.header('Gatos encontrados:')
    st.table(results)

query = st.sidebar.text_input("Buscar por nombre: ")
query = query.upper()
if st.sidebar.button('Buscar', key='button2'):
    # Filtra los datos que contienen la consulta ingresada
    data['name'] = data['name'].astype(str)
    results = data[data["name"].str.upper().str.contains(query)]
    # Muestra los resultados
    st.header('Gatos con el nombre encontrados:')
    st.table(results)


#Multiselect
st.sidebar.markdown("##")
coat_pattern = st.sidebar.multiselect("Selecciona por el patrón de su pelaje", 
                                      data["coat_pattern"].unique(), default=data["coat_pattern"].unique())
coatFilter = data[data["coat_pattern"].isin(coat_pattern)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS2"):
    st.subheader('Patrón del pelaje')
    st.write(coatFilter)

st.sidebar.markdown("##")
sex_upon_outcome = st.sidebar.multiselect("Selecciona por el estado reproductivo del gato",
                                           data["sex_upon_outcome"].unique(), default=data["sex_upon_outcome"].unique())
statusFilter = data[data["sex_upon_outcome"].isin(sex_upon_outcome)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS3"):
    st.subheader('Estado reproductivo')
    st.write(statusFilter)

st.sidebar.markdown("##")
outcome_type = st.sidebar.multiselect("Selecciona por la situación actual del gato", 
                                      data["outcome_type"].unique(), default=data["outcome_type"].unique())
situationFilter = data[data["outcome_type"].isin(outcome_type)]
if st.sidebar.checkbox('Mostrar datos', key="buttonS4"):
    st.subheader('Situación actual del gato')
    st.write(situationFilter)


# Histogram
fig, ax = plt.subplots()
ax.hist(data['dob_year'], bins=15)
ax.set_xlabel('Año')
ax.set_ylabel('Cantidad de gatos')
ax.set_title('Nacimientos')
plt.style.use('dark_background')
st.sidebar.markdown("##")
if st.sidebar.checkbox('Mostrar histograma', key="buttonHistogram"):
    st.header("Histograma")
    st.pyplot(fig)
    st.markdown(
        'Este histograma muestra los años de nacimiento de los gatos existentes en el refugio')


# Barsgraph
selection = data.query(
    "coat_pattern == @coat_pattern & sex_upon_outcome == @sex_upon_outcome & outcome_type == @outcome_type")
fig = px.bar(selection, x="breed", y=["coat_pattern", "sex_upon_outcome"])
fig.update_xaxes(title='Categorías')
fig.update_yaxes(title='Valores')
if st.sidebar.checkbox('Mostrar gráfica de barras', key="buttonBarsGraph"):
    st.header("Gráfica de barras")
    st.plotly_chart(fig)
    st.markdown(
        'Esta gráfica de barras muestra la cantidad de gatos según su tipo de pelaje y su estado reproductivo')


# Scattergraph
avgPricecars = selection['breed']
fig = px.scatter(selection,
                 x=selection["breed"].index,
                 y=avgPricecars,
                 template="plotly_white")
fig.update_xaxes(title='Gatos')
fig.update_yaxes(title='Razas')
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
if st.sidebar.checkbox('Mostrar gráfica scatter', key="buttonScatterGraph"):
    st.header("Gráfica de dispersión")
    st.plotly_chart(fig)
    st.markdown(
        'Esta gráfica de dispersión muestra las razas de todos los gatos')
