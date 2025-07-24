from cola_prioridad import MaxHeap, MinHeap

print("Prueba con MinHeap:")
cola = MinHeap()
cola.insertar(2, "Revisión rutina")
cola.insertar(1, "Emergencia")
cola.insertar(3, "Consulta leve")

while not cola.esta_vacia():
    print(cola.extraer())
