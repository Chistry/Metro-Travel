import heapq

# Construye una representación de grafo a partir de las tarifas
def construir_grafo(tarifas, aeropuertos_permitidos):
    grafo = {aeropuerto: [] for aeropuerto in aeropuertos_permitidos}
    for origen, destino, precio in tarifas:
        if origen in aeropuertos_permitidos and destino in aeropuertos_permitidos:
            grafo[origen].append((destino, precio))
            grafo[destino].append((origen, precio))
    return grafo

def encontrar_ruta_mas_barata(grafo, origen, destino):
    cola_prioridad = [(0, 0, origen, [origen])]
    distancias = {nodo: (float('inf'), float('inf')) for nodo in grafo}
    distancias[origen] = (0, 0)
    
    while cola_prioridad:
        costo_actual, escalas_actuales, nodo_actual, ruta_actual = heapq.heappop(cola_prioridad)
        
        if (costo_actual, escalas_actuales) > distancias[nodo_actual]:
            continue
        
        if nodo_actual == destino:
            return costo_actual, escalas_actuales, ruta_actual
            
        for vecino, precio_vuelo in grafo.get(nodo_actual, []):
            nuevo_costo = costo_actual + precio_vuelo
            nuevas_escalas = escalas_actuales + 1
            
            if (nuevo_costo, nuevas_escalas) < distancias[vecino]:
                distancias[vecino] = (nuevo_costo, nuevas_escalas)
                nueva_ruta = ruta_actual + [vecino]
                heapq.heappush(cola_prioridad, (nuevo_costo, nuevas_escalas, vecino, nueva_ruta))
                
    return float('inf'), 0, []