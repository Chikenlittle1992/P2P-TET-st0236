import node
from dht import DHT
import random
import time
import threading

def menu(node_address, dht):
    while True:
        print("\n--- Menú ---")
        print("1. Subir archivo")
        print("2. Buscar archivo")
        print("3. Ver vecinos actuales")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            filename = input("Ingresa el nombre del archivo que deseas subir: ")
            dht.add_file(filename, node_address)
            print(f"Archivo '{filename}' subido al nodo {node_address}.")
        
        elif opcion == "2":
            filename = input("Ingresa el nombre del archivo que deseas buscar: ")
            try:
                # Obtener vecinos automáticamente y buscar en ellos
                neighbors = node.get_neighbors(node_address)
                for neighbor in neighbors:
                    nodes_with_file = node.find_file(filename, neighbor)
                    if nodes_with_file:
                        print(f"El archivo '{filename}' está disponible en los siguientes nodos: {nodes_with_file}")
                        break
                else:
                    print(f"El archivo '{filename}' no fue encontrado en la red.")
            except Exception as e:
                print(f"Error buscando el archivo '{filename}': {e}")
        
        elif opcion == "3":
            try:
                neighbors = node.get_neighbors(node_address)
                print(f"Vecinos actuales del nodo {node_address}: {neighbors}")
            except Exception as e:
                print(f"No se pudo obtener la lista de vecinos: {e}")
        
        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    # Dirección del nodo
    node_address = input("Ingresa el puerto (ejemplo: localhost:5001): ")
    dht = DHT()

    # Inicializar nodo
    server = node.serve(node_address, dht)

    # Unirse a la red de nodos (vecinos)
    bootstrap_node = input("Ingresa la dirección del nodo bootstrap (deja vacío si es el primer nodo): ")
    if bootstrap_node:
        node.connect_to_node(node_address, bootstrap_node)
        # Obtener vecinos del nodo bootstrap y actualizar
        neighbors = node.get_neighbors(bootstrap_node)
        node.update_neighbors(node_address, neighbors)

        # Informar a los vecinos del nodo bootstrap sobre el nuevo nodo
        node.update_neighbors(bootstrap_node, [node_address])
    else:
        print("Nodo inicial de la red, sin bootstrap.")

    # Iniciar el menú en un hilo separado para que el nodo siga corriendo
    menu_thread = threading.Thread(target=menu, args=(node_address, dht))
    menu_thread.start()

    # Mantener el nodo activo y esperando solicitudes
    try:
        while True:
            time.sleep(10)  # Mantener el servidor activo
    except KeyboardInterrupt:
        print("Nodo detenido.")
        server.stop(0)
        menu_thread.join()

