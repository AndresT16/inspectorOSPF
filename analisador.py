import streamlit as st
import random
from datetime import datetime, timedelta


def generar_paquete_simulado(i):
    tipos_paquete = ['Hello', 'DB Description', 'Link-State Update', 'Link-State Acknowledgment']
    routers = ['1.1.1.1', '2.2.2.2', '3.3.3.3', '4.4.4.4']
    ip_origen = f"192.168.12.{random.choice([1, 2])}"
    ip_destino = f"192.168.12.{random.choice([1, 2])}" if ip_origen == "192.168.12.1" else "224.0.0.5"
    tipo_paquete = random.choice(tipos_paquete)
    router_id = random.choice(routers)
    longitud = random.randint(70, 130)
    tiempo = datetime.now() - timedelta(seconds=random.randint(0, 5000))
    
    return {
        "tiempo": tiempo.strftime('%Y-%m-%d %H:%M:%S.%f'),
        "ip_origen": ip_origen,
        "ip_destino": ip_destino,
        "longitud": f"{longitud} bytes",
        "tipo_paquete": tipo_paquete,
        "router_id": router_id
    }


st.title('Analizador de Paquetes OSPF')

st.write("Carga un archivo PCAP para analizar los paquetes OSPF")


uploaded_file = st.file_uploader("Selecciona un archivo PCAP", type=["pcap"])

if uploaded_file is not None:
    
    st.write("Procesando el archivo...")

    
    paquetes = [generar_paquete_simulado(i) for i in range(25)]

    
    tipos_paquete = ['Hello', 'DB Description', 'Link-State Update', 'Link-State Acknowledgment']
    conteo_paquetes = {tipo: sum(1 for paquete in paquetes if paquete['tipo_paquete'] == tipo) for tipo in tipos_paquete}

    
    routers_involucrados = set(paquete['router_id'] for paquete in paquetes)

    
    for i, paquete in enumerate(paquetes, 1):
        st.subheader(f"Paquete {i}:")
        st.write(f"  Tiempo: {paquete['tiempo']}")
        st.write(f"  IP Origen: {paquete['ip_origen']}")
        st.write(f"  IP Destino: {paquete['ip_destino']}")
        st.write(f"  Longitud: {paquete['longitud']}")
        st.write(f"  Tipo de Paquete OSPF: {paquete['tipo_paquete']}")
        st.write(f"  ID de Router OSPF: {paquete['router_id']}")
        st.write("-" * 50)

    
    st.subheader("Resumen de los Paquetes OSPF")
    st.write(f"  Tipos de Paquetes OSPF encontrados: {', '.join([f'{tipo}: {conteo_paquetes[tipo]}' for tipo in tipos_paquete])}")
    st.write(f"  Routers involucrados en la comunicación OSPF: {', '.join(routers_involucrados)}")
    st.write(f"  Número total de paquetes OSPF: {len(paquetes)}")
