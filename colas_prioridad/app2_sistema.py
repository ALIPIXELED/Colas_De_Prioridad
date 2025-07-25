import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox, QProgressBar, QHBoxLayout, QInputDialog
from PyQt6.QtCore import Qt, QTimer
from cola_prioridad import MinHeap, MaxHeap

# clase principal del simulador de PC
class SimuladorPC(QWidget):
    def __init__(self):
        super().__init__()
        # titulo y tamano de la ventana
        self.setWindowTitle('Simulador de Encendido de PC con Cola de Prioridad')
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: black;")

        # etiqueta que muestra el estado de la PC
        self.estado_label = QLabel('Estado: Apagada')
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_label.setStyleSheet("color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 18px; background: black;")
        self.layout.addWidget(self.estado_label)

        # boton para encender la PC
        self.encender_btn = QPushButton('Encender Computadora')
        self.encender_btn.clicked.connect(self.encender_pc)
        self.encender_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.layout.addWidget(self.encender_btn)

        # boton para apagar la PC
        self.apagar_btn = QPushButton('Apagar Computadora')
        self.apagar_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.apagar_btn.setEnabled(False)
        self.apagar_btn.clicked.connect(self.apagar_pc)
        self.layout.addWidget(self.apagar_btn)

        # lista que muestra las tareas de la PC
        self.lista_tareas = QListWidget()
        self.lista_tareas.setStyleSheet("background-color: black; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.layout.addWidget(self.lista_tareas)

        # barra de progreso para mostrar avance de tareas
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar {background-color: #222; color: #00FF00; border: 1px solid #00FF00; font-family: 'Consolas', 'Courier New', monospace;} QProgressBar::chunk {background-color: #00FF00;}")
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        # lista de tareas principales con su prioridad
        self.tareas = [
            (1, 'Encendido electrico (Power On)'),
            (2, 'POST (Power-On Self-Test)'),
            (3, 'Ejecucion del firmware BIOS/UEFI'),
            (4, 'Deteccion y configuracion de dispositivos de arranque'),
            (5, 'Carga del gestor de arranque (Bootloader)'),
            (6, 'Carga del nucleo del sistema operativo (Kernel)'),
            (7, 'Inicializacion de drivers y servicios basicos del sistema'),
            (8, 'Montaje del sistema de archivos'),
            (9, 'Inicio de servicios del sistema operativo'),
            (10, 'Carga del entorno de usuario / login'),
            (11, 'Carga de programas de inicio del usuario'),
        ]
        # uso un heap minimo para manejar las tareas
        self.cola = MinHeap()
        for prioridad, tarea in self.tareas:
            self.cola.insertar(prioridad, tarea)
        self._mostrar_tareas()

        # botones para agregar y eliminar tareas
        botones_layout = QHBoxLayout()
        self.agregar_btn = QPushButton('Agregar Tarea')
        self.agregar_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; border: 1px solid #00FF00;")
        self.agregar_btn.clicked.connect(self.agregar_tarea)
        botones_layout.addWidget(self.agregar_btn)
        self.eliminar_btn = QPushButton('Eliminar Tarea Seleccionada')
        self.eliminar_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; border: 1px solid #00FF00;")
        self.eliminar_btn.clicked.connect(self.eliminar_tarea)
        botones_layout.addWidget(self.eliminar_btn)
        self.layout.addLayout(botones_layout)

    # muestra las tareas en la lista y actualiza la barra de progreso
    def _mostrar_tareas(self):
        self.lista_tareas.clear()
        for prioridad, tarea in sorted(self.tareas):
            self.lista_tareas.addItem(f"Prioridad {prioridad}: {tarea}")
        # pone el color verde a todos los items
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            item.setForeground(Qt.GlobalColor.green)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self.tareas))
        self._verificar_tareas_principales()

    # agrega una nueva tarea a la lista
    def agregar_tarea(self):
        nombre, ok1 = QInputDialog.getText(self, 'Agregar Tarea', 'Nombre de la tarea:')
        if not ok1 or not nombre.strip():
            return
        prioridades_existentes = {p for p, _ in self.tareas}
        prioridad, ok2 = QInputDialog.getInt(self, 'Agregar Tarea', 'Prioridad (numero, menor es mas importante):', min=1, max=100, value=5)
        if not ok2:
            return
        if prioridad in prioridades_existentes:
            QMessageBox.warning(self, 'Agregar Tarea', f'Ya existe una tarea con prioridad {prioridad}. Elige otra prioridad.')
            return
        self.tareas.append((prioridad, nombre.strip()))
        self._mostrar_tareas()

    # elimina la tarea seleccionada de la lista
    def eliminar_tarea(self):
        fila = self.lista_tareas.currentRow()
        if fila < 0 or fila >= len(self.tareas):
            QMessageBox.warning(self, 'Eliminar Tarea', 'Selecciona una tarea para eliminar.')
            return
        tareas_ordenadas = sorted(self.tareas)
        tarea_a_eliminar = tareas_ordenadas[fila]
        self.tareas.remove(tarea_a_eliminar)
        self._mostrar_tareas()
        self._verificar_tareas_principales()

    # verifica que las tareas principales existan y sean correctas
    def _verificar_tareas_principales(self):
        prioridades = {p for p, _ in self.tareas}
        # las tareas principales son las de prioridad 1 a 11
        principales = set(range(1, 12))
        # textos originales de cada tarea principal
        tareas_originales = {
            1: 'Encendido electrico (Power On)',
            2: 'POST (Power-On Self-Test)',
            3: 'Ejecucion del firmware BIOS/UEFI',
            4: 'Deteccion y configuracion de dispositivos de arranque',
            5: 'Carga del gestor de arranque (Bootloader)',
            6: 'Carga del nucleo del sistema operativo (Kernel)',
            7: 'Inicializacion de drivers y servicios basicos del sistema',
            8: 'Montaje del sistema de archivos',
            9: 'Inicio de servicios del sistema operativo',
            10: 'Carga del entorno de usuario / login',
            11: 'Carga de programas de inicio del usuario',
        }
        # revisa que todas las tareas principales esten y sean correctas
        validas = True
        for p in principales:
            if (p, tareas_originales[p]) not in self.tareas:
                validas = False
                break
        if not validas:
            self.encender_btn.setEnabled(False)
            self.apagar_btn.setEnabled(False)
        else:
            self.encender_btn.setEnabled(True)
            if self.estado_label.text() == 'Estado: Tareas ejecutadas':
                self.apagar_btn.setEnabled(True)

    # funcion que simula encender la PC
    def encender_pc(self):
        # revisa que todas las tareas principales esten y sean correctas
        tareas_originales = {
            1: 'Encendido electrico (Power On)',
            2: 'POST (Power-On Self-Test)',
            3: 'Ejecucion del firmware BIOS/UEFI',
            4: 'Deteccion y configuracion de dispositivos de arranque',
            5: 'Carga del gestor de arranque (Bootloader)',
            6: 'Carga del nucleo del sistema operativo (Kernel)',
            7: 'Inicializacion de drivers y servicios basicos del sistema',
            8: 'Montaje del sistema de archivos',
            9: 'Inicio de servicios del sistema operativo',
            10: 'Carga del entorno de usuario / login',
            11: 'Carga de programas de inicio del usuario',
        }
        principales = set(range(1, 12))
        for p in principales:
            if (p, tareas_originales[p]) not in self.tareas:
                QMessageBox.warning(self, 'Encender', 'No puedes encender la computadora si alguna tarea principal (prioridad 1 a 11) fue eliminada o modificada.')
                return
        self.estado_label.setText('Estado: Encendida')
        self.encender_btn.setEnabled(False)
        self.apagar_btn.setEnabled(False)
        self.agregar_btn.setEnabled(False)
        self.eliminar_btn.setEnabled(False)
        self.lista_tareas.clear()
        self.ejecucion = []
        self._tareas_restantes = []
        # uso un heap minimo para ejecutar las tareas en orden
        temp_cola = MinHeap()
        for prioridad, tarea in self.tareas:
            temp_cola.insertar(prioridad, tarea)
        while not temp_cola.esta_vacia():
            self._tareas_restantes.append(temp_cola.extraer())
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self._tareas_restantes))
        self._mostrar_siguiente_tarea()

    # muestra la siguiente tarea que se esta ejecutando
    def _mostrar_siguiente_tarea(self):
        total = self.progress_bar.maximum()
        current = self.progress_bar.value()
        if self._tareas_restantes:
            prioridad, tarea = self._tareas_restantes.pop(0)
            self.lista_tareas.addItem(f"Ejecutando (Prioridad {prioridad}): {tarea}")
            item = self.lista_tareas.item(self.lista_tareas.count()-1)
            item.setForeground(Qt.GlobalColor.green)
            self.progress_bar.setValue(current + 1)
            QTimer.singleShot(1200, self._mostrar_siguiente_tarea)
        else:
            self.estado_label.setText('Estado: Tareas ejecutadas')
            self.apagar_btn.setEnabled(True)
            QMessageBox.information(self, 'Tareas', '¡Todas las tareas han sido ejecutadas!')
            self.agregar_btn.setEnabled(True)
            self.eliminar_btn.setEnabled(True)

    # funcion que ya no se usa, solo queda por compatibilidad
    def ejecutar_tareas(self):
        pass

    # funcion que simula apagar la PC
    def apagar_pc(self):
        # revisa que todas las tareas principales esten y sean correctas
        tareas_originales = {
            1: 'Encendido electrico (Power On)',
            2: 'POST (Power-On Self-Test)',
            3: 'Ejecucion del firmware BIOS/UEFI',
            4: 'Deteccion y configuracion de dispositivos de arranque',
            5: 'Carga del gestor de arranque (Bootloader)',
            6: 'Carga del nucleo del sistema operativo (Kernel)',
            7: 'Inicializacion de drivers y servicios basicos del sistema',
            8: 'Montaje del sistema de archivos',
            9: 'Inicio de servicios del sistema operativo',
            10: 'Carga del entorno de usuario / login',
            11: 'Carga de programas de inicio del usuario',
        }
        principales = set(range(1, 12))
        for p in principales:
            if (p, tareas_originales[p]) not in self.tareas:
                QMessageBox.warning(self, 'Apagar', 'No puedes apagar la computadora si alguna tarea principal (prioridad 1 a 11) fue eliminada o modificada.')
                return
        self.estado_label.setText('Estado: Apagando...')
        self.apagar_btn.setEnabled(False)
        self.agregar_btn.setEnabled(False)
        self.eliminar_btn.setEnabled(False)
        self.lista_tareas.clear()
        self._tareas_apagar = []
        # uso un heap maximo para cerrar las tareas en orden inverso
        temp_cola = MaxHeap()
        for prioridad, tarea in self.tareas:
            temp_cola.insertar(prioridad, tarea)
        while not temp_cola.esta_vacia():
            self._tareas_apagar.append(temp_cola.extraer())
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self._tareas_apagar))
        self._apagar_siguiente_tarea()

    # muestra la siguiente tarea que se esta cerrando
    def _apagar_siguiente_tarea(self):
        total = self.progress_bar.maximum()
        current = self.progress_bar.value()
        if self._tareas_apagar:
            prioridad, tarea = self._tareas_apagar.pop(0)
            self.lista_tareas.addItem(f"Cerrando (Prioridad {prioridad}): {tarea}")
            item = self.lista_tareas.item(self.lista_tareas.count()-1)
            item.setForeground(Qt.GlobalColor.green)
            self.progress_bar.setValue(current + 1)
            QTimer.singleShot(1200, self._apagar_siguiente_tarea)
        else:
            self.estado_label.setText('Estado: Apagada')
            QTimer.singleShot(1000, self.close)

# punto de entrada de la app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = SimuladorPC()
    ventana.show()
    sys.exit(app.exec())