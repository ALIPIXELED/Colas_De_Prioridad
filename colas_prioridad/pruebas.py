from cola_prioridad import MaxHeap, MinHeap

cola = MaxHeap()
cola.insertar(5, "Paciente leve")
cola.insertar(10, "Emergencia")
cola.insertar(7, "Urgencia media")

while not cola.esta_vacia():
    print("Atendiendo:", cola.extraer())
