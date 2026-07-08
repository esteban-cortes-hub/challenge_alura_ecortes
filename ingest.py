from src.loader import cargar_documentos


def main():
    documentos = cargar_documentos("docs")

    if not documentos:
        print("No se encontraron documentos .docx o .md en la carpeta docs.")
        return

    print(f"Documentos encontrados: {len(documentos)}")
    print("-" * 60)

    for doc in documentos:
        print(f"Archivo: {doc['nombre_archivo']}")
        print(f"Caracteres: {doc['cantidad_caracteres']}")
        print(f"Vista previa: {doc['contenido'][:300]}...")
        print("-" * 60)


if __name__ == "__main__":
    main()