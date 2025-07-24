import heapq

class ElementoPrioridad:
    def __init__(self, prioridad, dato):
        self.prioridad = prioridad
        self.dato = dato

    def __repr__(self):
        return f"({self.prioridad}, {self.dato})"

# ------------------------------------------
# Clase base (opcional si se quiere extender más)
# ------------------------------------------

class ColaPrioridad:
    def insertar(self, prioridad, dato):
        raise NotImplementedError

    def extraer(self):
        raise NotImplementedError

    def ver_siguiente(self):
        raise NotImplementedError

    def esta_vacia(self):
        raise NotImplementedError

# ------------------------------------------
# MinHeap: menor prioridad = más urgente
# ------------------------------------------

class MinHeap(ColaPrioridad):
    def __init__(self):
        self.heap = []

    def insertar(self, prioridad, dato):
        heapq.heappush(self.heap, (prioridad, dato))

    def extraer(self):
        if self.esta_vacia():
            return None
        return heapq.heappop(self.heap)

    def ver_siguiente(self):
        if self.esta_vacia():
            return None
        return self.heap[0]

    def esta_vacia(self):
        return len(self.heap) == 0

# ------------------------------------------
# MaxHeap: mayor prioridad = más urgente
# ------------------------------------------

class MaxHeap(ColaPrioridad):
    def __init__(self):
        self.heap = []

    def insertar(self, prioridad, dato):
        # Usamos -prioridad para simular MaxHeap con heapq
        heapq.heappush(self.heap, (-prioridad, dato))

    def extraer(self):
        if self.esta_vacia():
            return None
        prioridad, dato = heapq.heappop(self.heap)
        return (-prioridad, dato)

    def ver_siguiente(self):
        if self.esta_vacia():
            return None
        prioridad, dato = self.heap[0]
        return (-prioridad, dato)

    def esta_vacia(self):
        return len(self.heap) == 0
