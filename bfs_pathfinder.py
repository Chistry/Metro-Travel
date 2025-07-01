class BFSPathfinder:
    
    def __init__(self, grafo: dict[str, list[tuple[str, float]]]):
        self.grafo = grafo
        self.visitados: set[str] = set()
        self.padres: dict[str, str | None] = {}
        self.costos: dict[str, float] = {}
    
    def encontrar_ruta_menos_escalas(self, origen: str, destino: str) -> tuple[float, int, list[str]]:
        # Verificar que origen y destino existen en el grafo
        if origen not in self.grafo:
            return float('inf'), 0, []
        if destino not in self.grafo:
            return float('inf'), 0, []
        
        # Inicializar estructuras de datos
        self.visitados.clear()
        self.padres.clear()
        self.costos.clear()
        
        # Cola para BFS: almacena tuplas (nodo_actual, costo_acumulado)
        # Usamos una lista normal como cola
        cola: list[tuple[str, float]] = [(origen, 0)]
        
        # Marcar origen como visitado
        self.visitados.add(origen)
        self.padres[origen] = None
        self.costos[origen] = 0
        
        # Variable para almacenar si encontramos el destino
        destino_encontrado = False
        
        # Algoritmo BFS principal
        while cola and not destino_encontrado:
            # Extraer el primer elemento de la cola (FIFO)
            # Nota: pop(0) es O(n), menos eficiente que deque.popleft() que es O(1)
            nodo_actual, costo_actual = cola.pop(0)
            
            # Explorar todos los vecinos del nodo actual
            for vecino, precio_vuelo in self.grafo.get(nodo_actual, []):
                # Si no hemos visitado este vecino
                if vecino not in self.visitados:
                    # Marcarlo como visitado
                    self.visitados.add(vecino)
                    
                    # Guardar el padre para reconstruir la ruta
                    self.padres[vecino] = nodo_actual
                    
                    # Calcular y guardar el costo acumulado
                    nuevo_costo = costo_actual + precio_vuelo
                    self.costos[vecino] = nuevo_costo
                    
                    # Si llegamos al destino, terminar
                    if vecino == destino:
                        destino_encontrado = True
                        break
                    
                    # Agregar vecino a la cola para explorar sus conexiones
                    cola.append((vecino, nuevo_costo))
        
        # Si no encontramos el destino, no hay ruta
        if destino not in self.visitados:
            return float('inf'), 0, []
        
        # Reconstruir la ruta desde destino hasta origen
        ruta = self._reconstruir_ruta(origen, destino)
        
        # Calcular número de escalas (número de vuelos - 1)
        # Ejemplo: CCS -> AUA -> SBH = 2 vuelos, 1 escala
        num_escalas = len(ruta) - 2 if len(ruta) > 1 else 0
        
        # Obtener costo total
        costo_total = self.costos[destino]
        
        return costo_total, num_escalas, ruta
    
    def _reconstruir_ruta(self, origen: str, destino: str) -> list[str]:
        ruta = []
        nodo_actual = destino
        
        # Recorrer desde destino hasta origen usando los padres
        while nodo_actual is not None:
            ruta.append(nodo_actual)
            nodo_actual = self.padres.get(nodo_actual)
        
        # Invertir la ruta para que vaya de origen a destino
        ruta.reverse()
        
        return ruta
    
    def obtener_estadisticas_ruta(self, ruta: list[str]) -> dict[str, any]:
        if len(ruta) < 2:
            return {
                'valida': False,
                'mensaje': 'Ruta inválida'
            }
        
        # Calcular costo por segmento
        costos_segmentos = []
        for i in range(len(ruta) - 1):
            origen_seg = ruta[i]
            destino_seg = ruta[i + 1]
            
            # Buscar el precio del segmento
            for dest, precio in self.grafo.get(origen_seg, []):
                if dest == destino_seg:
                    costos_segmentos.append({
                        'origen': origen_seg,
                        'destino': destino_seg,
                        'precio': precio
                    })
                    break
        
        return {
            'valida': True,
            'num_vuelos': len(ruta) - 1,
            'num_escalas': max(0, len(ruta) - 2),
            'costo_total': sum(seg['precio'] for seg in costos_segmentos),
            'costo_promedio': sum(seg['precio'] for seg in costos_segmentos) / len(costos_segmentos) if costos_segmentos else 0,
            'segmentos': costos_segmentos
        }


def encontrar_ruta_menos_escalas_bfs(grafo: dict[str, list[tuple[str, float]]], 
                                    origen: str, 
                                    destino: str) -> tuple[float, int, list[str]]:
    bfs_finder = BFSPathfinder(grafo)
    return bfs_finder.encontrar_ruta_menos_escalas(origen, destino) 