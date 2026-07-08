from pathlib import Path
from docx import Document


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


def cargar_documentos(carpeta_docs: str = "docs") -> list[dict]:
    ruta_docs = Path(carpeta_docs)
    documentos = []

    if not ruta_docs.exists():
        raise FileNotFoundError(f"No existe la carpeta: {carpeta_docs}")

    for archivo in ruta_docs.iterdir():
        if archivo.name.lower() == "readme.md":
            continue

        if archivo.suffix.lower() == ".docx":
            contenido = leer_docx(archivo)
        elif archivo.suffix.lower() == ".md":
            contenido = leer_md(archivo)
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