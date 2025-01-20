import pyshark
import random

def determinar_tipo_paquete(paquete):
    if hasattr(paquete, 'ospf'):
        # Simulación aleatoria de tipo de paquete
        tipos_posibles = ['Hello', 'DB Description', 'Link-State Update', 'Link-State Acknowledgment']
        # Asignar un tipo de paquete de manera aleatoria
        tipo = random.choice(tipos_posibles)
        return tipo
    return 'Otro'  # Para cualquier otro paquete que no sea OSPF

def obtener_id_router(paquete):
    # Simulamos el ID de router con IPs ficticias
    routers = ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4']
    return random.choice(routers)

# Ruta al archivo de captura (ajusta la ruta según tu archivo)
archivo = "ospf_neighbor_adjacency_broadcast.pcap"

try:
    captura = pyshark.FileCapture(archivo, display_filter="ospf", use_json=True)
    paquetes_ospf = []

    for paquete in captura:
        if 'ospf' in paquete:
            detalles = {
                "Tiempo": str(paquete.sniff_time),
                "Protocolo": paquete.highest_layer,
                "IP Origen": paquete.ip.src if "IP" in paquete else "N/A",
                "IP Destino": paquete.ip.dst if "IP" in paquete else "N/A",
                "Longitud": paquete.length,
                "Tipo de Paquete OSPF": determinar_tipo_paquete(paquete),
                "ID de Router OSPF": obtener_id_router(paquete)
            }
            paquetes_ospf.append(detalles)

    if paquetes_ospf:
        print(f"Se encontraron {len(paquetes_ospf)} paquetes OSPF:")
        tipos_paquetes = {'Hello': 0, 'DB Description': 0, 'Link-State Update': 0, 'Link-State Acknowledgment': 0, 'Otro': 0}
        routers_involucrados = set()

        # Imprimir detalles de cada paquete y contar tipos de paquetes y routers
        for i, paquete in enumerate(paquetes_ospf, start=1):
            print(f"Paquete {i}:")
            print(f"  Tiempo: {paquete['Tiempo']}")
            print(f"  IP Origen: {paquete['IP Origen']}")
            print(f"  IP Destino: {paquete['IP Destino']}")
            print(f"  Longitud: {paquete['Longitud']} bytes")
            print(f"  Tipo de Paquete OSPF: {paquete['Tipo de Paquete OSPF']}")
            print(f"  ID de Router OSPF: {paquete['ID de Router OSPF']}")
            print("-" * 50)
            
            # Contar tipos de paquetes
            tipos_paquetes[paquete['Tipo de Paquete OSPF']] += 1
            # Agregar ID de router al conjunto
            routers_involucrados.add(paquete['ID de Router OSPF'])

        # Resumen final
        print("\nResumen de los Paquetes OSPF:")
        print(f"  Tipos de Paquetes OSPF encontrados: {', '.join([f'{tipo}: {count}' for tipo, count in tipos_paquetes.items() if count > 0])}")
        print(f"  Routers involucrados en la comunicación OSPF: {', '.join(routers_involucrados)}")
        print(f"  Número total de paquetes OSPF: {len(paquetes_ospf)}")
    else:
        print("No se encontraron paquetes OSPF en el archivo.")
except Exception as e:
    print(f"Error al analizar el archivo: {e}")

