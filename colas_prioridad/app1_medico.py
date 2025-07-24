from cola_prioridad import ColaPrioridadBase, MinHeap, MaxHeap
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QMessageBox, QListWidgetItem)
from PyQt6.QtGui import QFont, QColor
import sys

# Diccionario de enfermedades y su prioridad (1 = más urgente, 10 = menos urgente)
ENFERMEDADES_PRIORIDAD = {
    'infarto': 1,
    'accidente grave': 1,
    'ictus': 2,
    'hemorragia interna': 2,
    'neumonía': 3,
    'quemaduras severas': 3,
    'fractura expuesta': 4,
    'apendicitis': 4,
    'asma severa': 5,
    'diabetes descompensada': 5,
    'fractura simple': 6,
    'gripe': 7,
    'infección urinaria': 8,
    'alergia leve': 9,
    'consulta general': 10
}

def color_por_prioridad(prioridad):
    if prioridad <= 2:
        return QColor('#ffb3b3')  # Rojo claro
    elif 3 <= prioridad <= 6:
        return QColor('#fff7b3')  # Amarillo claro
    else:
        return QColor('#b3ffb3')  # Verde claro

class HospitalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hospital - Gestión de Pacientes')
        self.setMinimumWidth(600)
        self.cola = MinHeap()
        self.init_ui()
        self.setStyleSheet(self.estilos())

    def estilos(self):
        return """
        QWidget {
            background: #f6f8fa;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 15px;
        }
        QLabel {
            color: #22223b;
            font-weight: bold;
        }
        QLineEdit, QComboBox {
            background: #fff;
            border: 1.5px solid #b5b5b5;
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 15px;
            color: #111;
        }
        QComboBox QAbstractItemView {
            color: #111;
            background: #fff;
        }
        QPushButton {
            background: #4f8cff;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 18px;
            font-size: 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #2563eb;
        }
        QListWidget {
            background: #f0f4ff;
            border: 1.5px solid #b5b5b5;
            border-radius: 8px;
            padding: 8px;
            font-size: 15px;
            color: #111;
        }
        QMessageBox QLabel {
            color: #22223b;
            font-size: 15px;
        }
        """

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)

        # Formulario para agregar paciente
        form_layout = QHBoxLayout()
        form_layout.setSpacing(12)
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText('Nombre del paciente')
        self.enfermedad_combo = QComboBox()
        self.enfermedad_combo.addItems(ENFERMEDADES_PRIORIDAD.keys())
        self.btn_agregar = QPushButton('Agregar paciente')
        self.btn_agregar.clicked.connect(self.agregar_paciente)
        form_layout.addWidget(QLabel('Nombre:'))
        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(QLabel('Enfermedad:'))
        form_layout.addWidget(self.enfermedad_combo)
        form_layout.addWidget(self.btn_agregar)
        layout.addLayout(form_layout)

        # Lista de espera
        self.lista_espera = QListWidget()
        layout.addWidget(QLabel('Pacientes en espera:'))
        layout.addWidget(self.lista_espera)

        # Botón para atender paciente
        self.btn_atender = QPushButton('Atender siguiente paciente')
        self.btn_atender.clicked.connect(self.atender_paciente)
        layout.addWidget(self.btn_atender)

        self.setLayout(layout)
        self.actualizar_lista()

    def agregar_paciente(self):
        nombre = self.nombre_input.text().strip()
        enfermedad = self.enfermedad_combo.currentText()
        if not nombre:
            QMessageBox.warning(self, 'Error', 'Ingrese el nombre del paciente.')
            return
        prioridad = ENFERMEDADES_PRIORIDAD[enfermedad]
        self.cola.insertar(prioridad, {'nombre': nombre, 'enfermedad': enfermedad})
        self.nombre_input.clear()
        self.actualizar_lista()

    def atender_paciente(self):
        paciente = self.cola.extraer()
        if paciente:
            prioridad, datos = paciente
            QMessageBox.information(self, 'Paciente Atendido', f"Atendiendo a {datos['nombre']} (Enfermedad: {datos['enfermedad'].title()}, Prioridad: {prioridad})")
        else:
            QMessageBox.information(self, 'Sin pacientes', 'No hay pacientes en espera.')
        self.actualizar_lista()

    def actualizar_lista(self):
        self.lista_espera.clear()
        if self.cola.esta_vacia():
            self.lista_espera.addItem('No hay pacientes en la cola.')
        else:
            for prioridad, datos in sorted(self.cola.heap):
                item = QListWidgetItem(f"{datos['nombre']} - {datos['enfermedad'].title()} (Prioridad: {prioridad})")
                item.setBackground(color_por_prioridad(prioridad))
                self.lista_espera.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = HospitalApp()
    ventana.show()
    sys.exit(app.exec())

