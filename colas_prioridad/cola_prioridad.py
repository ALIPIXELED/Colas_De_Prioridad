#Esta clase define la estructura basica de una cola de prioridad.
class ColaPrioridadBase:
    #constructor, crea una lista vacia para el heap
    def __init__(self):
        self.heap = []

    #devuelve True si la cola esta vacia
    def esta_vacia(self):
        return len(self.heap) == 0

    #muestra el primer elemento sin sacarlo
    def ver_siguiente(self):
        return self.heap[0] if not self.esta_vacia() else None

    #intercambia dos elementos del heap
    def _intercambiar(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

#implementa un heap minimo
class MinHeap(ColaPrioridadBase):
    #inserta un elemento con prioridad
    def insertar(self, prioridad, dato):
        self.heap.append((prioridad, dato))
        self._subir(len(self.heap) - 1)

    #saca el elemento con menor prioridad
    def extraer(self):
        if self.esta_vacia():
            return None
        self._intercambiar(0, len(self.heap) - 1)
        min_val = self.heap.pop()
        self._bajar(0)
        return min_val

    #sube el elemento hasta su lugar correcto
    def _subir(self, index):
        while index > 0:
            padre = (index - 1) // 2
            if self.heap[index][0] < self.heap[padre][0]:
                self._intercambiar(index, padre)
                index = padre
            else:
                break

    #baja el elemento hasta su lugar correcto
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

#implementa un heap maximo
class MaxHeap(ColaPrioridadBase):
    #inserta un elemento con prioridad
    def insertar(self, prioridad, dato):
        self.heap.append((prioridad, dato))
        self._subir(len(self.heap) - 1)

    #saca el elemento con mayor prioridad
    def extraer(self):
        if self.esta_vacia():
            return None
        self._intercambiar(0, len(self.heap) - 1)
        max_val = self.heap.pop()
        self._bajar(0)
        return max_val

    #sube el elemento hasta su lugar correcto
    def _subir(self, index):
        while index > 0:
            padre = (index - 1) // 2
            if self.heap[index][0] > self.heap[padre][0]:
                self._intercambiar(index, padre)
                index = padre
            else:
                break

    #baja el elemento hasta su lugar correcto
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
