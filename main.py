import os
from dotenv import load_dotenv
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70℉(placeholder)", self)
        self.emoji_label = QLabel("☀️")
        self.description_label = QLabel("Sunny", self)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())