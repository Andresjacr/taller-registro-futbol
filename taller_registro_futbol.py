import os

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\nMENÚ DE OPCIONES:")
    print("1. Registrar equipo")
    print("2. Programar partido")
    print("3. Registrar marcador y estadísticas de partido")
    print("4. Ver equipo con más goles a favor")
    print("5. Ver equipo con más goles en contra")
    print("6. Gestionar plantel de un equipo") 
    print("7. Salir")

def registrar_equipo(equipos):
    """Registra un nuevo equipo."""
    nombre = input("Introduce el nombre del nuevo equipo: ").strip()
    if nombre in equipos:
        print("Error: El equipo ya está registrado.")
    elif nombre:
        equipos[nombre] = {"pj": 0, "pg": 0, "pp": 0, "pe": 0, "gf": 0, "gc": 0, "plantel": [], "puntos": 0}
        print(f"¡Equipo '{nombre}' registrado con éxito!")
    else:
        print("Error: El nombre del equipo no puede estar vacío.")

def programar_fecha(equipos, calendario):
    """Programa un nuevo partido."""
    if len(equipos) < 2:
        print("Necesitas al menos dos equipos registrados para programar una fecha.")
        return

    print("Equipos disponibles:", ", ".join(equipos.keys()))
    local = input("Introduce el nombre del equipo local: ").strip()
    visitante = input("Introduce el nombre del equipo visitante: ").strip()

    if local not in equipos or visitante not in equipos:
        print("Error: Uno o ambos equipos no están registrados.")
    elif local == visitante:
        print("Error: Un equipo no puede jugar contra sí mismo.")
    else:
        partido = {"local": local, "visitante": visitante, "marcador_local": None, "marcador_visitante": None, "jugado": False}
        calendario.append(partido)
        print(f"Partido '{local} vs {visitante}' programado.")

def registrar_marcador(equipos, calendario):
    """Registra el marcador de un partido y actualiza las estadísticas."""
    partidos_pendientes = [p for p in calendario if not p["jugado"]]
    if not partidos_pendientes:
        print("No hay partidos pendientes de registrar marcador.")
        return

    print("\nPartidos pendientes:")
    for i, partido in enumerate(partidos_pendientes):
        print(f"{i + 1}. {partido['local']} vs {partido['visitante']}")

    try:
        opcion = int(input("Selecciona el número del partido para registrar el marcador: ")) - 1
        if 0 <= opcion < len(partidos_pendientes):
            partido_seleccionado = partidos_pendientes[opcion]

            if partido_seleccionado["jugado"]:
                print("Este partido ya fue registrado.")
                return

            marcador_local = int(input(f"Goles de {partido_seleccionado['local']}: "))
            marcador_visitante = int(input(f"Goles de {partido_seleccionado['visitante']}: "))

            if marcador_local < 0 or marcador_visitante < 0:
                print("Error: Los marcadores no pueden ser negativos.")
                return

            partido_seleccionado["marcador_local"] = marcador_local
            partido_seleccionado["marcador_visitante"] = marcador_visitante
            partido_seleccionado["jugado"] = True

            local = partido_seleccionado["local"]
            visitante = partido_seleccionado["visitante"]

            equipos[local]["pj"] += 1
            equipos[visitante]["pj"] += 1
            equipos[local]["gf"] += marcador_local
            equipos[visitante]["gf"] += marcador_visitante
            equipos[local]["gc"] += marcador_visitante
            equipos[visitante]["gc"] += marcador_local

            if marcador_local > marcador_visitante:
                equipos[local]["pg"] += 1
                equipos[visitante]["pp"] += 1
                equipos[local]["puntos"] += 3
            elif marcador_visitante > marcador_local:
                equipos[visitante]["pg"] += 1
                equipos[local]["pp"] += 1
                equipos[visitante]["puntos"] += 3
            else:
                equipos[local]["pe"] += 1
                equipos[visitante]["pe"] += 1
                equipos[local]["puntos"] += 1
                equipos[visitante]["puntos"] += 1
            
            print("Marcador registrado y estadísticas de equipo actualizadas.")

        else:
            print("Opción no válida.")
    except ValueError:
        print("Error: Debes introducir un número entero para la opción y los marcadores.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def equipo_mas_goles_favor(equipos):
    """Encuentra y muestra el equipo con más goles a favor."""
    if not equipos:
        print("No hay equipos registrados.")
        return
    
    equipo_max_gf = max(equipos, key=lambda e: equipos[e]['gf'])
    print(f"El equipo con más goles a favor es: {equipo_max_gf} con {equipos[equipo_max_gf]['gf']} goles.")

def equipo_mas_goles_contra(equipos):
    """Encuentra y muestra el equipo con más goles en contra."""
    if not equipos:
        print("No hay equipos registrados.")
        return
    
    equipo_max_gc = max(equipos, key=lambda e: equipos[e]['gc'])
    print(f"El equipo con más goles en contra es: {equipo_max_gc} con {equipos[equipo_max_gc]['gc']} goles.")

def gestionar_plantel(equipos):
    """Gestiona el plantel de un equipo: registra jugadores y muestra sus datos (sin estadísticas individuales de juego)."""
    if not equipos:
        print("No hay equipos registrados.")
        return

    print("Equipos disponibles:", ", ".join(equipos.keys()))
    nombre_equipo = input("Introduce el nombre del equipo para gestionar su plantel: ").strip()

    if nombre_equipo in equipos:
        while True:
            print(f"\n--- Gestión del plantel de '{nombre_equipo}' ---")
            print("1. Agregar nuevo jugador")
            print("2. Ver jugadores del plantel")
            print("3. Volver al menú principal")
            opcion_plantel = input("Elige una opción: ").strip()

            if opcion_plantel == '1':
                nombre_jugador = input("Introduce el nombre del nuevo jugador: ").strip()
                if nombre_jugador:
                    jugador_existente = next((j for j in equipos[nombre_equipo]["plantel"] if j["nombre"] == nombre_jugador), None)
                    if jugador_existente:
                        print(f"El jugador '{nombre_jugador}' ya está en el plantel de '{nombre_equipo}'.")
                    else:
                        try:
                            dorsal = int(input(f"Dorsal de {nombre_jugador}: "))
                            posicion = input(f"Posición de {nombre_jugador} (ej. Delantero, Defensa, Portero): ").strip()
                            edad = int(input(f"Edad de {nombre_jugador}: "))

                            equipos[nombre_equipo]["plantel"].append({
                                "nombre": nombre_jugador,
                                "dorsal": dorsal,
                                "posicion": posicion,
                                "edad": edad
                            })
                            print(f"Jugador '{nombre_jugador}' añadido a '{nombre_equipo}'.")
                        except ValueError:
                            print("Error: La dorsal y la edad deben ser números enteros. No se añadió el jugador.")
                else:
                    print("El nombre del jugador no puede estar vacío.")

            elif opcion_plantel == '2':
                if not equipos[nombre_equipo]["plantel"]:
                    print(f"El plantel de '{nombre_equipo}' está vacío.")
                else:
                    print(f"\n--- Jugadores en el plantel de '{nombre_equipo}' ---")
                    for jugador in equipos[nombre_equipo]["plantel"]:
                        print(f"- {jugador['nombre']} (Dorsal: {jugador['dorsal']}, Posición: {jugador['posicion']}, Edad: {jugador['edad']})") 
            
            elif opcion_plantel == '3':
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
            
            input("\nPresiona Enter para continuar...")
    else:
        print("Error: El equipo no está registrado.")


def main():
    """Función principal del programa."""
    equipos = {}
    calendario = []

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == '1':
            registrar_equipo(equipos)
        elif opcion == '2':
            programar_fecha(equipos, calendario)
        elif opcion == '3':
            registrar_marcador(equipos, calendario)
        elif opcion == '4':
            equipo_mas_goles_favor(equipos)
        elif opcion == '5':
            equipo_mas_goles_contra(equipos)
        elif opcion == '6':
            gestionar_plantel(equipos)
        elif opcion == '7':
            print("Saliendo del programa. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()