class ColaPrioridadBase:
    def __init__(self):
        self.heap = []

    def esta_vacia(self):
        return len(self.heap) == 0

    def ver_siguiente(self):
        return self.heap[0] if not self.esta_vacia() else None

    def _intercambiar(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

class MinHeap(ColaPrioridadBase):
    def insertar(self, prioridad, dato):
        self.heap.append((prioridad, dato))
        self._subir(len(self.heap) - 1)

    def extraer(self):
        if self.esta_vacia():
            return None
        self._intercambiar(0, len(self.heap) - 1)
        min_val = self.heap.pop()
        self._bajar(0)
        return min_val

    def _subir(self, index):
        while index > 0:
            padre = (index - 1) // 2
            if self.heap[index][0] < self.heap[padre][0]:
                self._intercambiar(index, padre)
                index = padre
            else:
                break

    def _bajar(self, index):
        n = len(self.heap)
        while True:
            izquierdo = 2 * index + 1
            derecho = 2 * index + 2
            menor = index

            if izquierdo < n and self.heap[izquierdo][0] < self.heap[menor][0]:
                menor = izquierdo
            if derecho < n and self.heap[derecho][0] < self.heap[menor][0]:
                menor = derecho
            if menor == index:
                break
            self._intercambiar(index, menor)
            index = menor

class MaxHeap(ColaPrioridadBase):
    def insertar(self, prioridad, dato):
        self.heap.append((prioridad, dato))
        self._subir(len(self.heap) - 1)

    def extraer(self):
        if self.esta_vacia():
            return None
        self._intercambiar(0, len(self.heap) - 1)
        max_val = self.heap.pop()
        self._bajar(0)
        return max_val

    def _subir(self, index):
        while index > 0:
            padre = (index - 1) // 2
            if self.heap[index][0] > self.heap[padre][0]:
                self._intercambiar(index, padre)
                index = padre
            else:
                break

    def _bajar(self, index):
        n = len(self.heap)
        while True:
            izquierdo = 2 * index + 1
            derecho = 2 * index + 2
            mayor = index

            if izquierdo < n and self.heap[izquierdo][0] > self.heap[mayor][0]:
                mayor = izquierdo
            if derecho < n and self.heap[derecho][0] > self.heap[mayor][0]:
                mayor = derecho
            if mayor == index:
                break
            self._intercambiar(index, mayor)
            index = mayor
