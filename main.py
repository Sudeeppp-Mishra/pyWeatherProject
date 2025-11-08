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
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel()
        self.description_label = QLabel(self)
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # NOTE: Here we didn't aligned get_weather_button to center because currently it takes up the width of the window as we expand them so no need to horizontally align it
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        
        self.setStyleSheet("""
                           QLabel, QPushButton{
                               font-family: 'Poppins', 'Roboto', 'Segoe UI', 'Arial', sans-serif;
                           }
                           
                           QLabel#city_label{
                               font-size: 40px;
                               font-style: italic;
                           }
                           
                           QLineEdit#city_input{
                               font-size: 40px;
                           }
                           
                           QPushButton#get_weather_button{
                               font-size: 30px;
                               font-weight: bold;
                           }
                           
                           QLabel#temperature_label{
                               font-size: 60px;
                           }
                           
                           QLabel#emoji_label{
                               font-size: 100px;
                                   font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Arial";
                           }
                           
                           QLabel#description_label{
                               font-size: 50px;
                           }
                           """)
        
        self.city_input.setFixedHeight(60)
        
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        
        try:
            response = requests.get(url)
            response.raise_for_status() # normally our try block don't auto raise the HTTPError kind of exceptions so raise_for_status() method raises this exception if there is this exception
            data = response.json()
            
            if data['cod'] == 200: # cod is named for response code so 200 response code means OK
                self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_error: # this error is returned if status code is 400-599 (NOTE: 400-499 -> Client error responses and 500-599 -> Server error responses) -> and NOTE that this exception is found in requests module that we imported
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input!")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key!")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied!")
                case 404:
                    self.display_error("Not found:\nCity not found!")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later!")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server!")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down!")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server!")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection!")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out!")
                    
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL!") 
        
        except requests.exceptions.RequestException as req_error: # this is due to n/w problem or invalid url
            self.display_error(f"Request Error:\n{req_error}")
        
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_K = data["main"]["temp"]
        temperature_C = temperature_K - 273.15
        temperature_F = (temperature_K*9/5)-459.67
        
        weather_description = data["weather"][0]["description"]
        
        weather_id = data["weather"][0]["id"]
        
        self.temperature_label.setText(f"{temperature_C:.0f}℃")
        self.description_label.setText(weather_description.title())
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        
    @staticmethod   
    def get_weather_emoji(weather_id):
        if 200<=weather_id<=232:
            return "⛈️"
        elif 300<=weather_id<=321:
            return "🌦️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "❄️"
        elif 701<=weather_id<=741:
            return "😶‍🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif 801<=weather_id<=804:
            return "☁️"
        else:
            return ""
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())