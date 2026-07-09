from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.rag import cargar_base_vectorial, buscar_contexto


def obtener_fragmentos_relevantes(pregunta: str, cantidad: int = 4) -> list[dict]:
    resultados = buscar_contexto(pregunta, k=cantidad)

    fragmentos = []

    for doc in resultados:
        fragmentos.append(
            {
                "contenido": doc.page_content,
                "fuente": doc.metadata.get("source", "Fuente desconocida"),
                "ruta": doc.metadata.get("ruta", ""),
            }
        )

    return fragmentos


def crear_cadena_rag():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_template(
        """
Eres un asistente especializado en documentación técnica de iTop.

Responde la pregunta usando únicamente el contexto entregado.
Si la respuesta no está en el contexto, responde:
"No encontré esa información en la documentación disponible."

Sé claro, breve y técnico.

Contexto:
{context}

Pregunta:
{input}
"""
    )

    vectorstore = cargar_base_vectorial()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain


def responder_pregunta(pregunta: str) -> dict:
    chain = crear_cadena_rag()

    resultado = chain.invoke({"input": pregunta})

    fuentes = []

    for doc in resultado.get("context", []):
        fuente = doc.metadata.get("source", "Fuente desconocida")
        if fuente not in fuentes:
            fuentes.append(fuente)

    return {
        "respuesta": resultado["answer"],
        "fuentes": fuentes,
    }