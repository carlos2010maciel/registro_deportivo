# main.py
import sys
from src import registro
from src.gui import iniciar_gui


def menu_consola():
    print("\n¿Cómo deseas ejecutar el programa?")
    print("1. Interfaz gráfica")
    print("2. Consola")
    opcion = input("Selecciona una opción (1/2): ")

    if opcion == "1":
        iniciar_gui()
    elif opcion == "2":
        registro.menu_principal()
    else:
        print("Opción inválida.")


if __name__ == "__main__":
    menu_consola()