import qrcode
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Generator")
        self.label = QLabel()
        self.input = QLineEdit()
        self.img = QImage()
        self.pixmap = QPixmap()
        self.save_button = QPushButton("save")

        self.error_correct = qrcode.constants.ERROR_CORRECT_H
        self.fill_color = "black"
        self.back_color = "white"
        self.qr = qrcode.QRCode(
            version=None,
            error_correction=self.error_correct,
            box_size=10,
            border=2,
        )

        self.input.textEdited.connect(self.create_qr_code)
        self.save_button.clicked.connect(self.save_image)
        self.setCentralWidget(self.label)
        self.resize(self.pixmap.width(), self.pixmap.height())

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def create_qr_code(self):
        self.qr.clear()
        self.qr.version = None
        self.qr.add_data(self.input.text())
        self.qr.make(fit=True)
        self.img = self.qr.make_image(
            fill_color=self.fill_color,
            back_color=self.back_color,
        )
        pixmap = QPixmap.fromImage(ImageQt(self.img))
        self.label.setPixmap(pixmap)


    def get_dir_path(self):
        dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            directory="/home/",
            #options=QFileDialog.Option.DontUseNativeDialog,
        )
        return dir_path


    def save_image(self):
        path = self.get_dir_path() + "/" + self.input.text() + ".png"
        print("save QR Code to " + path)
        self.img.save(path)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
