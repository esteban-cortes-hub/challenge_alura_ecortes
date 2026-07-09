from src.rag import buscar_contexto


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