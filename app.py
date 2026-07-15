from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.chat import responder_pregunta


load_dotenv()

RUTA_CHROMA = Path("data/chroma")


st.set_page_config(
    page_title="Asistente iTop",
    page_icon="🤖",
    layout="centered",
)


def limpiar_conversacion() -> None:
    """Elimina el historial almacenado en la sesión de Streamlit."""
    st.session_state.mensajes = []


def mostrar_barra_lateral() -> None:
    """Construye la información lateral de la aplicación."""
    with st.sidebar:
        st.header("🤖 Proyecto")

        st.write(
            "Asistente de inteligencia artificial para consultar "
            "documentación técnica de iTop."
        )

        st.divider()

        st.subheader("Tecnologías")

        st.markdown(
            """
- Python
- LangChain
- Gemini
- ChromaDB
- Streamlit
"""
        )

        st.divider()

        st.subheader("Formatos soportados")

        st.markdown(
            """
- DOCX
- Markdown
- PDF
"""
        )

        st.divider()

        if st.button(
            "🗑️ Nueva conversación",
            use_container_width=True,
        ):
            limpiar_conversacion()
            st.rerun()


def mostrar_presentacion() -> None:
    """Muestra el título y las instrucciones principales."""
    st.title("🤖 Asistente IA para documentación iTop")

    st.write(
        "Consulta documentación técnica utilizando lenguaje natural. "
        "Las respuestas se generan a partir de la información almacenada "
        "en la base documental."
    )

    with st.expander("💡 Ejemplos de preguntas"):
        st.markdown(
            """
- ¿Cuál es el endpoint para enviar licencias?
- ¿Cómo se autentica la integración?
- ¿Qué campos requiere la API?
- ¿Cómo se crea un objeto en iTop?
- ¿Qué componentes forman parte de la arquitectura?
"""
        )

    st.info(
        "El asistente responde únicamente utilizando la documentación "
        "disponible. Si no encuentra información suficiente, lo indicará."
    )


def mostrar_historial() -> None:
    """Muestra los mensajes almacenados en la sesión."""
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["rol"]):
            st.markdown(mensaje["contenido"])


def construir_respuesta_con_fuentes(
    respuesta: str,
    fuentes: list[str],
) -> str:
    """Construye el texto que será almacenado en el historial."""
    contenido = respuesta

    if fuentes:
        contenido += "\n\n### 📚 Fuentes consultadas\n"

        for fuente in fuentes:
            contenido += f"- `{fuente}`\n"

    return contenido


def procesar_pregunta(pregunta: str) -> None:
    """Procesa una pregunta y muestra la respuesta del agente."""
    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": pregunta,
        }
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Buscando en la documentación..."):
                resultado = responder_pregunta(pregunta)

            respuesta = resultado.get(
                "respuesta",
                "No fue posible generar una respuesta.",
            )
            fuentes = resultado.get("fuentes", [])

            st.markdown(respuesta)

            if fuentes:
                st.markdown("### 📚 Fuentes consultadas")

                for fuente in fuentes:
                    st.markdown(f"- `{fuente}`")

            contenido_historial = construir_respuesta_con_fuentes(
                respuesta,
                fuentes,
            )

        except Exception:
            contenido_historial = (
                "⚠️ No fue posible procesar la consulta.\n\n"
                "Verifica que:\n\n"
                "- La API Key de Gemini sea válida.\n"
                "- Exista conexión a Internet.\n"
                "- La base vectorial haya sido creada correctamente."
            )

            st.error(contenido_historial)

    st.session_state.mensajes.append(
        {
            "rol": "assistant",
            "contenido": contenido_historial,
        }
    )


def main() -> None:
    """Punto de entrada de la aplicación Streamlit."""
    mostrar_barra_lateral()
    mostrar_presentacion()

    if not RUTA_CHROMA.exists():
        st.error(
            "No se encontró la base vectorial. "
            "Ejecuta primero el siguiente comando:"
        )

        st.code("python ingest.py", language="powershell")
        st.stop()

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    mostrar_historial()

    pregunta = st.chat_input(
        "Escribe tu pregunta sobre iTop..."
    )

    if pregunta and pregunta.strip():
        procesar_pregunta(pregunta.strip())


if __name__ == "__main__":
    main()