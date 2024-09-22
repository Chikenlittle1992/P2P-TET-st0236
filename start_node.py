import node
from dht import DHT
import random
import time
import threading

def menu(node_address, dht):
    while True:
        print("\n--- Menú ---")
        print("1. Conectar a otro nodo")
        print("2. Subir archivo")
        print("3. Buscar archivo")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            target_node_address = input("Ingresa la dirección del nodo al que deseas conectar (localhost:puerto): ")
            try:
                node.connect_to_node(node_address, target_node_address)
            except Exception as e:
                print(f"No se pudo conectar a {target_node_address}: {e}")
        
        elif opcion == "2":
            filename = input("Ingresa el nombre del archivo que deseas subir: ")
            dht.add_file(filename, node_address)
            print(f"Archivo '{filename}' subido al nodo {node_address}.")
        
        elif opcion == "3":
            filename = input("Ingresa el nombre del archivo que deseas buscar: ")
            target_node_address = input("Ingresa la dirección del nodo donde iniciar la búsqueda (localhost:puerto): ")
            try:
                nodes_with_file = node.find_file(filename, target_node_address)
                if nodes_with_file:
                    print(f"El archivo '{filename}' está disponible en los siguientes nodos: {nodes_with_file}")
                else:
                    print(f"El archivo '{filename}' no fue encontrado en la red.")
            except Exception as e:
                print(f"Error buscando el archivo '{filename}': {e}")
        
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

