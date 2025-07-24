from cola_prioridad import MaxHeap, MinHeap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QComboBox, QListWidgetItem, QTimeEdit
)
from PyQt6.QtCore import Qt, QTime

# Mini aplicación de prueba con PyQt6 para gestionar eventos con prioridad

class EventoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Eventos con Prioridad")
        self.setMinimumWidth(500)
        self.eventos = []  # Guardar todos los eventos como (prioridad, evento)
        self.init_ui()
        self.setStyleSheet(self.get_styles())

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Encabezado bonito
        header = QLabel("♦♦♦♦♦♦♦ ☺ Gestor de Eventos con Prioridad ☺ ♦♦♦♦♦♦♦")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px; color: #111;")
        layout.addWidget(header)

        # ComboBox para elegir el orden
        orden_layout = QHBoxLayout()
        orden_label = QLabel("Orden:")
        orden_label.setStyleSheet("font-size: 16px; color: #111; font-weight: bold;")
        self.orden_combo = QComboBox()
        self.orden_combo.addItems(["Descendente (más importante primero)", "Ascendente (menos importante primero)"])
        self.orden_combo.setCurrentIndex(0)
        orden_layout.addWidget(orden_label)
        orden_layout.addWidget(self.orden_combo)
        orden_layout.addStretch()
        layout.addLayout(orden_layout)

        # Entrada de evento
        self.evento_input = QLineEdit()
        self.evento_input.setPlaceholderText("Nombre del evento")
        self.prioridad_input = QLineEdit()
        self.prioridad_input.setPlaceholderText("Prioridad (entero, mayor = más importante)")
        self.prioridad_input.setMaximumWidth(200)
        self.hora_input = QTimeEdit()
        self.hora_input.setDisplayFormat("HH:mm")
        self.hora_input.setTime(QTime.currentTime())
        self.hora_input.setMaximumWidth(100)
        agregar_btn = QPushButton("Agregar Evento")
        agregar_btn.clicked.connect(self.agregar_evento)
        agregar_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Layout de formulario
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(self.evento_input)
        form_layout.addWidget(self.prioridad_input)
        form_layout.addWidget(self.hora_input)
        form_layout.addWidget(agregar_btn)
        layout.addLayout(form_layout)

        # Botón y lista de eventos
        mostrar_btn = QPushButton("Mostrar eventos ordenados")
        mostrar_btn.clicked.connect(self.mostrar_eventos)
        mostrar_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        quitar_btn = QPushButton("Quitar todos los eventos")
        quitar_btn.clicked.connect(self.quitar_eventos)
        quitar_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(mostrar_btn)
        btns_layout.addWidget(quitar_btn)
        layout.addLayout(btns_layout)

        self.lista_eventos = QListWidget()
        self.lista_eventos.setStyleSheet("font-size: 16px; padding: 10px; color: #111;")
        # Cambiado: Quitar el modo de selección múltiple para usar checkboxes
        layout.addWidget(self.lista_eventos)

        eliminar_seleccionados_btn = QPushButton("Eliminar seleccionados")
        eliminar_seleccionados_btn.clicked.connect(self.eliminar_seleccionados)
        eliminar_seleccionados_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(eliminar_seleccionados_btn)

        self.setLayout(layout)

    def agregar_evento(self):
        evento = self.evento_input.text().strip()
        prioridad_text = self.prioridad_input.text().strip()
        hora = self.hora_input.time().toString("HH:mm")
        if not evento or not prioridad_text:
            QMessageBox.warning(self, "Error", "Debe ingresar el nombre y la prioridad del evento.")
            return
        try:
            prioridad = int(prioridad_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "La prioridad debe ser un número entero.")
            return
        self.eventos.append((prioridad, evento, hora))
        self.evento_input.clear()
        self.prioridad_input.clear()
        self.hora_input.setTime(QTime.currentTime())
        QMessageBox.information(self, "Evento agregado", f"Evento '{evento}' agregado con prioridad {prioridad} a las {hora}.")

    def mostrar_eventos(self):
        self.lista_eventos.clear()
        if not self.eventos:
            self.lista_eventos.addItem("No hay eventos para mostrar.")
            return
        orden = self.orden_combo.currentIndex()
        if orden == 0:
            heap = MaxHeap()
        else:
            heap = MinHeap()
        for prioridad, evento, hora in self.eventos:
            heap.insertar(prioridad, (evento, hora))
        eventos_ordenados = []
        while not heap.esta_vacia():
            prioridad, (evento, hora) = heap.extraer()
            eventos_ordenados.append((prioridad, evento, hora))
        for prioridad, evento, hora in eventos_ordenados:
            item = QListWidgetItem(f"Prioridad: {prioridad} - Evento: {evento} - Hora: {hora}")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.lista_eventos.addItem(item)

    def quitar_eventos(self):
        self.eventos.clear()
        self.lista_eventos.clear()
        self.lista_eventos.addItem("No hay eventos para mostrar.")

    def eliminar_seleccionados(self):
        # Obtener los textos de los eventos seleccionados
        items_a_eliminar = []
        for i in range(self.lista_eventos.count()):
            item = self.lista_eventos.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                items_a_eliminar.append(item.text())
        # Eliminar de self.eventos los que coincidan
        nuevos_eventos = []
        for prioridad, evento, hora in self.eventos:
            texto = f"Prioridad: {prioridad} - Evento: {evento} - Hora: {hora}"
            if texto not in items_a_eliminar:
                nuevos_eventos.append((prioridad, evento, hora))
        self.eventos = nuevos_eventos
        self.mostrar_eventos()

    def get_styles(self):
        return """
        QWidget {
            background: #f7f7fa;
            font-family: 'Segoe UI', 'Arial', sans-serif;
        }
        QLineEdit {
            border: 2px solid #bdbdbd;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
            background: #fff;
            color: #111;
        }
        QLineEdit:focus {
            border: 2px solid #6c63ff;
            background: #f0f0ff;
            color: #111;
        }
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6c63ff, stop:1 #48c6ef);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.2s;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #48c6ef, stop:1 #6c63ff);
        }
        QListWidget {
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            color: #111;
        }
        QListWidget::indicator {
            width: 20px;
            height: 20px;
            margin: 2px;
        }
        QListWidget::indicator:unchecked {
            border: 2px solid #666;
            background: #fff;
            border-radius: 3px;
        }
        QListWidget::indicator:checked {
            border: 2px solid #6c63ff;
            background: #6c63ff;
            border-radius: 3px;
            image: none;
        }
        QListWidget::indicator:checked:after {
            content: "✓";
            color: white;
            font-weight: bold;
        }
        QComboBox {
            border: 2px solid #bdbdbd;
            border-radius: 8px;
            padding: 6px;
            font-size: 15px;
            background: #eaeaff;
            color: #222;
            selection-background-color: #6c63ff;
            selection-color: #fff;
        }
        QComboBox QAbstractItemView {
            background: #eaeaff;
            color: #222;
            selection-background-color: #6c63ff;
            selection-color: #fff;
        }
        QMessageBox QLabel {
            font-size: 15px;
            color: #111;
        }
        QTimeEdit {
            color: #111;
            font-size: 16px;
            border: 2px solid #bdbdbd;
            border-radius: 8px;
            padding: 6px 10px;
            background: #fff;
            min-width: 80px;
        }
        QTimeEdit:focus {
            border: 2px solid #6c63ff;
            background: #f0f0ff;
            color: #111;
        }
        """

# Lanzar la aplicación sin usar sys
app = QApplication([])
window = EventoApp()
window.show()
app.exec()
