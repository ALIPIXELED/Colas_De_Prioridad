# Simulador de Colas de Prioridad en Python

Este proyecto contiene varias aplicaciones que muestran el uso de colas de prioridad (heaps) en diferentes contextos, usando Python y PyQt6 para interfaces graficas.

## Estructura del proyecto

- **cola_prioridad.py**: Implementacion de las clases base de colas de prioridad, MinHeap y MaxHeap.
- **app1_medico.py**: Aplicacion de gestion de pacientes en un hospital usando una cola de prioridad para atender segun urgencia.
- **app2_sistema.py**: Simulador del encendido y apagado de una computadora, donde cada tarea del sistema tiene una prioridad y se ejecuta en orden usando una cola de prioridad.
- **app3_eventos.py**: (Si existe) Aplicacion para gestion de eventos o tareas usando colas de prioridad.
- **pruebas.py**: Archivo para pruebas de las estructuras de datos.

## Descripcion de cada aplicacion

### 1. app1_medico.py
Simula la gestion de pacientes en un hospital:
- Cada paciente tiene un nombre y una enfermedad.
- Cada enfermedad tiene una prioridad (1 es mas urgente, 10 es menos urgente).
- Los pacientes se atienden segun la prioridad de su enfermedad.
- Interfaz grafica amigable para agregar y atender pacientes.

### 2. app2_sistema.py
Simula el proceso de encendido y apagado de una computadora:
- Cada tarea del sistema (como BIOS, kernel, login, etc) tiene una prioridad.
- Se pueden agregar o eliminar tareas, pero las tareas principales no deben faltar ni cambiar para poder encender/apagar.
- El encendido ejecuta las tareas en orden de prioridad (MinHeap).
- El apagado cierra las tareas en orden inverso (MaxHeap).
- Barra de progreso y mensajes para mostrar el avance.
- Interfaz grafica tipo consola retro.

### 3. app3_eventos.py
(Si existe) Gestiona eventos o tareas usando colas de prioridad.

### 4. pruebas.py
Permite probar las funciones de las colas de prioridad sin interfaz grafica.

## Requisitos
- Python 3.10 o superior
- PyQt6

Puedes instalar PyQt6 con:
```
pip install PyQt6
```

## Como ejecutar cada app

1. Abre una terminal en la carpeta `colas_prioridad`.
2. Ejecuta la app que quieras, por ejemplo:
```
python app1_medico.py
```
O para el simulador de sistema:
```
python app2_sistema.py
```

## Notas
- El archivo `cola_prioridad.py` contiene toda la logica de los heaps.
- El archivo `__pycache__/` es solo cache de Python y no es necesario subirlo.
- Puedes modificar o agregar enfermedades/tareas segun lo que quieras probar.

---

Hecho por: El Cuartel General
