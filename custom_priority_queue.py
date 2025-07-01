class CustomPriorityQueue:
    def __init__(self):
        # la cola se representará como una lista de tuplas (costo, escalas, nodo, ruta)
        self._queue = []

    
    # Añade un elemento a la cola, el elemento debe ser una tupla donde el primer elemento es el costo y el segundo son las escalas (para desempatar por escalas)
    def push(self, item):
        
        self._queue.append(item)
        self._queue.sort() # Ordena por el primer elemento (costo), luego por el segundo (escalas)

    def pop(self):
        if not self._queue:
            return None
        # como mantenemos la lista ordenada, el elemento de menor costo está siempre al principio
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def __len__(self):
        return len(self._queue)