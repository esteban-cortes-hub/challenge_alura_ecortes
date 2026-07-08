from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


CHROMA_PATH = "data/chroma"


def obtener_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
        
    )


def convertir_a_documentos_langchain(documentos: list[dict]) -> list[Document]:
    documentos_langchain = []

    for doc in documentos:
        documentos_langchain.append(
            Document(
                page_content=doc["contenido"],
                metadata={
                    "source": doc["nombre_archivo"],
                    "ruta": doc["ruta"],
                },
            )
        )

    return documentos_langchain


def dividir_documentos(documentos_langchain: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_documents(documentos_langchain)


def crear_base_vectorial(chunks: list[Document]) -> Chroma:
    embeddings = obtener_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )

    return vectorstore


def cargar_base_vectorial() -> Chroma:
    embeddings = obtener_embeddings()

    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
    )


def buscar_contexto(pregunta: str, k: int = 4) -> list[Document]:
    vectorstore = cargar_base_vectorial()
    resultados = vectorstore.similarity_search(pregunta, k=k)
    return resultados