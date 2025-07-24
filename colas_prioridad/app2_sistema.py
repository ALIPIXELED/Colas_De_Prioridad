import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QMessageBox, QProgressBar, QHBoxLayout, QInputDialog
from PyQt6.QtCore import Qt, QTimer
from cola_prioridad import MinHeap, MaxHeap

class SimuladorPC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simulador de Encendido de PC con Cola de Prioridad')
        self.setGeometry(100, 100, 400, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: black;")

        self.estado_label = QLabel('Estado: Apagada')
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_label.setStyleSheet("color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 18px; background: black;")
        self.layout.addWidget(self.estado_label)

        self.encender_btn = QPushButton('Encender Computadora')
        self.encender_btn.clicked.connect(self.encender_pc)
        self.encender_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.layout.addWidget(self.encender_btn)

        # Eliminar el botón de ejecutar tareas
        # self.run_btn = QPushButton('Ejecutar Tareas')
        # self.run_btn.setEnabled(False)
        # self.run_btn.clicked.connect(self.ejecutar_tareas)
        # self.run_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        # self.layout.addWidget(self.run_btn)

        self.apagar_btn = QPushButton('Apagar Computadora')
        self.apagar_btn.setStyleSheet("background-color: #222; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.apagar_btn.setEnabled(False)
        self.apagar_btn.clicked.connect(self.apagar_pc)
        self.layout.addWidget(self.apagar_btn)

        self.lista_tareas = QListWidget()
        self.lista_tareas.setStyleSheet("background-color: black; color: #00FF00; font-family: 'Consolas', 'Courier New', monospace; font-size: 16px; border: 1px solid #00FF00;")
        self.layout.addWidget(self.lista_tareas)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar {background-color: #222; color: #00FF00; border: 1px solid #00FF00; font-family: 'Consolas', 'Courier New', monospace;} QProgressBar::chunk {background-color: #00FF00;}")
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.tareas = [
            (1, 'Cargar sistema operativo (muy importante)'),
            (3, 'Abrir navegador'),
            (2, 'Cargar antivirus'),
            (5, 'Abrir reproductor de música'),
            (4, 'Sincronizar archivos en la nube'),
        ]
        self.cola = MinHeap()
        for prioridad, tarea in self.tareas:
            self.cola.insertar(prioridad, tarea)
        self._mostrar_tareas()

        # Botones para agregar y eliminar tareas
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

    def _mostrar_tareas(self):
        self.lista_tareas.clear()
        for prioridad, tarea in sorted(self.tareas):
            self.lista_tareas.addItem(f"Prioridad {prioridad}: {tarea}")
        # Forzar color verde en todos los items
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            item.setForeground(Qt.GlobalColor.green)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self.tareas))
        self._verificar_tareas_principales()

    def agregar_tarea(self):
        nombre, ok1 = QInputDialog.getText(self, 'Agregar Tarea', 'Nombre de la tarea:')
        if not ok1 or not nombre.strip():
            return
        prioridades_existentes = {p for p, _ in self.tareas}
        prioridad, ok2 = QInputDialog.getInt(self, 'Agregar Tarea', 'Prioridad (número, menor es más importante):', min=1, max=100, value=5)
        if not ok2:
            return
        if prioridad in prioridades_existentes:
            QMessageBox.warning(self, 'Agregar Tarea', f'Ya existe una tarea con prioridad {prioridad}. Elige otra prioridad.')
            return
        self.tareas.append((prioridad, nombre.strip()))
        self._mostrar_tareas()

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

    def _verificar_tareas_principales(self):
        prioridades = {p for p, _ in self.tareas}
        # Puedes ajustar aquí qué prioridades son "principales". Por ejemplo, 1 y 2:
        principales = {1, 2}
        if not principales.issubset(prioridades):
            self.encender_btn.setEnabled(False)
            self.apagar_btn.setEnabled(False)
        else:
            self.encender_btn.setEnabled(True)
            # Solo habilitar apagar si ya se encendió y ejecutó todo
            if self.estado_label.text() == 'Estado: Tareas ejecutadas':
                self.apagar_btn.setEnabled(True)

    def encender_pc(self):
        prioridades = {p for p, _ in self.tareas}
        principales = {1, 2}
        if not principales.issubset(prioridades):
            QMessageBox.warning(self, 'Encender', 'No puedes encender la computadora si faltan tareas principales (prioridad 1 y 2).')
            return
        self.estado_label.setText('Estado: Encendida')
        self.encender_btn.setEnabled(False)
        self.apagar_btn.setEnabled(False)
        self.agregar_btn.setEnabled(False)
        self.eliminar_btn.setEnabled(False)
        self.lista_tareas.clear()
        self.ejecucion = []
        self._tareas_restantes = []
        temp_cola = MinHeap()
        for prioridad, tarea in self.tareas:
            temp_cola.insertar(prioridad, tarea)
        while not temp_cola.esta_vacia():
            self._tareas_restantes.append(temp_cola.extraer())
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self._tareas_restantes))
        self._mostrar_siguiente_tarea()

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

    def ejecutar_tareas(self):
        # Ya no se usa, pero se deja por compatibilidad
        pass

    def apagar_pc(self):
        prioridades = {p for p, _ in self.tareas}
        principales = {1, 2}
        if not principales.issubset(prioridades):
            QMessageBox.warning(self, 'Apagar', 'No puedes apagar la computadora si faltan tareas principales (prioridad 1 y 2).')
            return
        self.estado_label.setText('Estado: Apagando...')
        self.apagar_btn.setEnabled(False)
        self.agregar_btn.setEnabled(False)
        self.eliminar_btn.setEnabled(False)
        self.lista_tareas.clear()
        self._tareas_apagar = []
        temp_cola = MaxHeap()
        for prioridad, tarea in self.tareas:
            temp_cola.insertar(prioridad, tarea)
        while not temp_cola.esta_vacia():
            self._tareas_apagar.append(temp_cola.extraer())
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self._tareas_apagar))
        self._apagar_siguiente_tarea()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = SimuladorPC()
    ventana.show()
    sys.exit(app.exec())
