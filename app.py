import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_destilacion.csv")

df = cargar_datos()

st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")
st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Elige el porcentaje de etanol en la mezcla inicial para comenzar.")

porcentaje = st.slider("Selecciona % de etanol en mezcla", 0, 100, step=2)

file_ = open("alcoho.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()
st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="400">', unsafe_allow_html=True)

accion = st.radio("¿Qué deseas hacer?", ("Continuar", "Finalizar"))

if 'mediciones' not in st.session_state:
    st.session_state.mediciones = []

fila = df[df['Porc. Etanol (%)'] == porcentaje].iloc[0]

if accion == "Continuar":
    st.success(f"Índice de refracción: **{fila['Índice de Refracción']}**")
    st.session_state.mediciones.append((porcentaje, fila['Índice de Refracción']))

elif accion == "Finalizar":
    st.subheader("📈 Gráfica de Calibración")
    mediciones_df = pd.DataFrame(st.session_state.mediciones, columns=["% Etanol", "Índice de Refracción"])

    fig, ax = plt.subplots()
    ax.plot(mediciones_df["% Etanol"], mediciones_df["Índice de Refracción"], 'o-', color='blue')
    ax.set_xlabel("% Etanol")
    ax.set_ylabel("Índice de Refracción")
    ax.set_title("Curva de Calibración")
    st.pyplot(fig)

    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    b64_img = base64.b64encode(buffer.read()).decode()
    st.download_button("📥 Descargar imagen", data=buffer, file_name="grafica_calibracion.png", mime="image/png")

    if st.button("🔥 Destilar"):
        file_ = open("destila.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="400">', unsafe_allow_html=True)

        st.subheader("🔬 Resultados de Destilación")
        resultado = df[df["Porc. Etanol (%)"].isin(mediciones_df["% Etanol"])][["Porc. Etanol (%)", "Temperatura (°C)", "Xₑₜₒₕ (líquido)", "Xₑₜₒₕ (vapor)"]]
        resultado = resultado.rename(columns={
            "Porc. Etanol (%)": "% Etanol",
            "Temperatura (°C)": "T° Ebullición (°C)"
        })

        st.dataframe(resultado, use_container_width=True)

        csv = resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar tabla CSV", data=csv, file_name="resultados_destilacion.csv", mime="text/csv")