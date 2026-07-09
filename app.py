from dotenv import load_dotenv
import streamlit as st

from src.chat import responder_pregunta

load_dotenv()

st.set_page_config(
    page_title="Asistente iTop",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Asistente de documentación iTop")
st.write(
    "Haz preguntas sobre la documentación cargada en el proyecto. "
    "El asistente responderá usando la base documental disponible."
)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

pregunta = st.chat_input("Escribe tu pregunta sobre iTop...")

if pregunta:
    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": pregunta,
        }
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en la documentación..."):
            resultado = responder_pregunta(pregunta)

            respuesta = resultado["respuesta"]
            fuentes = resultado["fuentes"]

            st.markdown(respuesta)

            if fuentes:
                st.markdown("**Fuentes:**")
                for fuente in fuentes:
                    st.markdown(f"- `{fuente}`")

            contenido_historial = respuesta

            if fuentes:
                contenido_historial += "\n\n**Fuentes:**\n"
                for fuente in fuentes:
                    contenido_historial += f"- `{fuente}`\n"

    st.session_state.mensajes.append(
        {
            "rol": "assistant",
            "contenido": contenido_historial,
        }
    )