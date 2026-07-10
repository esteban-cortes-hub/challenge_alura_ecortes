from pathlib import Path

from docx import Document
from pypdf import PdfReader


def leer_docx(ruta_archivo: Path) -> str:
    documento = Document(ruta_archivo)
    parrafos = []

    for parrafo in documento.paragraphs:
        texto = parrafo.text.strip()

        if texto:
            parrafos.append(texto)

    return "\n".join(parrafos)


def leer_md(ruta_archivo: Path) -> str:
    return ruta_archivo.read_text(encoding="utf-8")


def leer_pdf(ruta_archivo: Path) -> str:
    lector = PdfReader(ruta_archivo)
    paginas = []

    for numero_pagina, pagina in enumerate(lector.pages, start=1):
        texto = pagina.extract_text()

        if texto and texto.strip():
            paginas.append(
                f"[Página {numero_pagina}]\n{texto.strip()}"
            )

    return "\n\n".join(paginas)


def cargar_documentos(carpeta_docs: str = "docs") -> list[dict]:
    ruta_docs = Path(carpeta_docs)
    documentos = []

    if not ruta_docs.exists():
        raise FileNotFoundError(f"No existe la carpeta: {carpeta_docs}")

    for archivo in ruta_docs.iterdir():
        if archivo.name.lower() == "readme.md":
            continue

        extension = archivo.suffix.lower()

        if extension == ".docx":
            contenido = leer_docx(archivo)
        elif extension == ".md":
            contenido = leer_md(archivo)
        elif extension == ".pdf":
            contenido = leer_pdf(archivo)
        else:
            continue

        if contenido.strip():
            documentos.append(
                {
                    "nombre_archivo": archivo.name,
                    "ruta": str(archivo),
                    "contenido": contenido,
                    "cantidad_caracteres": len(contenido),
                }
            )

    return documentos