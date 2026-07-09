from dotenv import load_dotenv
from src.chat import obtener_fragmentos_relevantes

load_dotenv()


def main():
    pregunta = input("Escribe tu pregunta: ")

    fragmentos = obtener_fragmentos_relevantes(pregunta)

    print("\nFragmentos encontrados:")
    print("-" * 60)

    for i, fragmento in enumerate(fragmentos, start=1):
        print(f"Resultado {i}")
        print(f"Fuente: {fragmento['fuente']}")
        print(fragmento["contenido"][:700])
        print("-" * 60)


if __name__ == "__main__":
    main()