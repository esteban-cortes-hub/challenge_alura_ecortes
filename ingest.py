from dotenv import load_dotenv
from src.loader import cargar_documentos
from src.rag import (
    convertir_a_documentos_langchain,
    dividir_documentos,
    crear_base_vectorial,
)

load_dotenv()
def main():
    documentos = cargar_documentos("docs")

    if not documentos:
        print("No se encontraron documentos .docx o .md en la carpeta docs.")
        return

    print(f"Documentos encontrados: {len(documentos)}")

    documentos_langchain = convertir_a_documentos_langchain(documentos)
    chunks = dividir_documentos(documentos_langchain)

    print(f"Chunks generados: {len(chunks)}")

    crear_base_vectorial(chunks)

    print("Base vectorial creada correctamente en data/chroma")


if __name__ == "__main__":
    main()