import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64

st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")

# Cargar base de datos desde Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel("BINARIA.xlsx")
    return df

df = cargar_datos()

st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Simulador interactivo para la destilación de mezclas etanol-agua usando datos reales de índice de refracción y fracciones molares.")

# Paso 1: Selección de concentración
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

if 'etapas' not in st.session_state:
    st.session_state.etapas = []

if st.button("Iniciar medición"):
    file_ = open("alcoho.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="mezcla" style="width: 300px;">',
        unsafe_allow_html=True,
    )
    st.session_state.etapas.append(porc_inicial)

# Mostrar datos medidos
if st.session_state.etapas:
    if st.button("Continuar medición"):
        mediciones = df[df["Porcentaje"] == porc_inicial]
        if not mediciones.empty:
            st.success("Índice de refracción encontrado:")
            st.write(mediciones[["Indice_Refraccion"]])
        else:
            st.error("Datos no encontrados para ese porcentaje.")
    if st.button("Finalizar"):
        st.subheader("📈 Gráfica de Calibración")
        fig, ax = plt.subplots()
        ax.plot(df["Porcentaje"], df["Indice_Refraccion"], marker="o")
        ax.set_xlabel("Porcentaje de Etanol (%)")
        ax.set_ylabel("Índice de Refracción")
        ax.set_title("Curva de Calibración")
        st.pyplot(fig)

        if st.button("Destilar"):
            file_ = open("destila.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
                unsafe_allow_html=True,
            )

            tabla = df[df["Porcentaje"].isin(st.session_state.etapas)]
            tabla = tabla[["Porcentaje", "Temperatura", "Xetoh_liquido", "Xetoh_vapor"]]
            st.write("🔬 Resultados de Destilación")
            st.dataframe(tabla.reset_index(drop=True))
