from runpowershell import run_powershell_script, open_houdini_with_file
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QProcess, QThread, QTimer
import keras
import numpy as np
IMAGE = keras.preprocessing.image

class WorkerThread(QThread):
    progress_updated = pyqtSignal(int)
    task_finished = pyqtSignal() 
    
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.stop_event = False
        
    def run(self):
        print("run is working")
        try:
            pred_curl = calc_curv(self.image_path)
            run_powershell_script(pred_curl)
        except Exception as e:
            print(f"Error running the command: {e}")
        finally:
            self.task_finished.emit()
    print("thread is stopped")
    def stop(self):
        self.stop_event = True
        self.quit()
    # def __del__(self):
    #      WorkerThread.quit(self)
    #      WorkerThread.terminate(self)

class ImageDropWidget(QWidget):

    image_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.file_path = "C:/users/Haitam/backup/HairCards_recovered_bak22.hip"
        self.process = QProcess()
        self.drop_label = QLabel("Drag and Drop an Image Here", self)
        self.drop_label.setStyleSheet("border: 2px dashed black; padding: 10px;")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.image_path = None

        # Initialize the label and layout
        self.label = QLabel("Cooking...", self)
        self.label.setAlignment(Qt.AlignCenter)       
        self.label.setVisible(False)
     
        self.button = QPushButton("Generate", self)
        self.button.clicked.connect(self.start_cooking)
        self.button.setEnabled(False)
        print("thiiiiisisselfpath", self.file_path)
        self.button2 = QPushButton("Manual", self)
        self.button2.clicked.connect(self.open_houdini)
        self.button2.setEnabled(True)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_cooking)
        self.cancel_button.setEnabled(False)  # Disabled by default

        layout = QVBoxLayout()
        layout.addWidget(self.drop_label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowTitle("HairGen")
        self.resize(400, 300)

        self.image_dropped.connect(self.process_image)

    def closeEvent(self, event):
        if hasattr(self, "worker_thread"):
            self.worker_thread.stop()
            print("Rendering thread has stopped.")
            print("close!")
        QApplication.quit()

    def open_houdini(self):
        if self.file_path:
            open_houdini_with_file(self.file_path)
        else:
            print("Error: No file selected.")
    
    def dragEnterEvent(self, event):
        print("MIME Data formats:", event.mimeData().formats())
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.button.setEnabled(True)
            self.image_path = urls[0].toLocalFile()
            print("Dropped file path:", self.image_path)
            self.image_dropped.emit(self.image_path)
            if self.image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
                pixmap = QPixmap(self.image_path)
                self.drop_label.setPixmap(pixmap.scaled(
                    self.drop_label.width(),
                    self.drop_label.height(),
                    Qt.KeepAspectRatio
                ))
            else:
                print("Invalid file type")
                self.button.setEnabled(False)
    
    
    def process_image(self, image_path):
        print("Processing image:", image_path)

    def start_cooking(self):
        print("startcooking is working")
        self.button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.label.setVisible(True)
        self.worker_thread = WorkerThread(self.image_path)
        self.worker_thread.task_finished.connect(self.on_task_finished)
        self.worker_thread.start()


    def cancel_cooking(self):
        print("Canceling thread...")
        if hasattr(self, "worker_thread"):
            self.worker_thread.stop()  # Stop the thread
            self.cancel_button.setEnabled(False)  # Disable Cancel button
            self.button.setEnabled(True)  # Re-enable Generate button
            self.label.setVisible(False)  # Hide "Cooking..." label

    # def stop_thread(self):
    #     self.worker_thread.stop()
    #     self.worker_thread.join()

    def on_task_finished(self):
        self.button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.label.setVisible(False)
        print("Task Completed!")

def calc_curv(image_path):
        img = image_path
        im2 = IMAGE.load_img(img)
        im2 = im2.resize((256,256))
        im2 = np.array(im2)
        model = keras.models.load_model("D:/HN_Training_data/Saved_model/HN_Hairmodel2.keras")
        pred = model.predict(im2.reshape(1,256,256,3))
        pred_curl = pred[0][0]
        pred_curl = pred_curl/255
        pred_curl = float(pred_curl)
        
        print(pred_curl)
        return pred_curl