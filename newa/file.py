import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class weatherapp(QWidget):
    def __init__(self):
        super().__init__() #1.create all widgets/ elements below
        self.city_label = QLabel("Enter city name", self)
        self.cityinput = QLineEdit(self)
        self.getweatherbutton = QPushButton("Get weather", self)
        self.temperaturelabel = QLabel(self)
        self.emoji = QLabel(self)
        self.descriptionlabel = QLabel( self)
        self.initUI() #1. initialising all element customisations 
    
    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout() #3. init layout manager
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.cityinput)
        vbox.addWidget(self.getweatherbutton)
        vbox.addWidget(self.temperaturelabel)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.descriptionlabel)
        self.setLayout(vbox) #4. assign layout manager
        self.city_label.setAlignment(Qt.AlignCenter) #5. Align all elements center justify
        self.cityinput.setAlignment(Qt.AlignCenter)
        self.temperaturelabel.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.descriptionlabel.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label") #6. set object names to apply styles
        self.cityinput.setObjectName("cityinput")
        self.temperaturelabel.setObjectName("temperaturelabel")
        self.emoji.setObjectName("emoji")
        self.descriptionlabel.setObjectName("descriptionlabel")
        self.getweatherbutton.setObjectName("getweatherbutton")

        self.setStyleSheet("""QLabel, QPushButton{ font-family: Arial; } 
                           QLabel#city_label{
                           font-size: 40px; font-style:italic;}
                           QLineEdit#cityinput{font-size:20px;}
                           QPushButton#getweatherbutton{
                           font-size:30px; font-weight:bold}
                           QLabel#temperaturelabel{
                           font-size: 75px;}
                           QLabel#emoji{
                           font-size:100px; }
                           QLabel#descriptionlabel{
                           font-size:50px;}""") #7. set style sheet, each label button
        
        self.getweatherbutton.clicked.connect(self.getweather) #8 whenever the button is clicked, use this func

    def getweather(self):
        api_key = "d6bf3f7eff743e800ebbd71081ee7be1"
        city = self.cityinput.text() #9 init api key, get the city name from the line edit part into local variable
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url) #10 after the request thru url, we will get/be returned with a response object
            response.raise_for_status()
            data = response.json() #convert to json

            if data["cod"]==200:
                self.displayweather(data)

        except requests.exceptions.HTTPError: #incorrect 400... code
            self.displayerror(f"{response.status_code}")
        except requests.exceptions.RequestException as req_error: 
            self.displayerror("req error")
        except requests.exceptions.ConnectionError: #network errors
            self.displayerror("Conection error \n checj your internet")
        except requests.exceptions.Timeout: 
            self.displayerror("timeout error the resquest timed out")
        except requests.exceptions.TooManyRedirects: 
            self.displayerror("too many redirects \n check url")

    def displayerror(self, message):
        self.temperaturelabel.setText(message)
        self.emoji.clear()
        self.descriptionlabel.clear()

    def displayweather(self,data):
        tempk = data["main"]["temp"]
        tempc = tempk-273.15
        weatherid = data["weather"][0]["id"]
        self.temperaturelabel.setText(f"{tempc:.0f}ºC")
        weatherdescription = data["weather"][0]["description"]
        self.descriptionlabel.setText(weatherdescription)
        self.emoji.setText(self.getemoji(weatherid))

    @staticmethod
    def getemoji(weatherid):
        if weatherid>=200 and weatherid <=232:
            return "⛈"
        elif weatherid>=300 and weatherid <=321:
            return "🌤"
        elif weatherid>=500 and weatherid <=531:
            return "🌧"
        elif  weatherid>=600 and weatherid <=622:
            return "❄️"
        elif weatherid>=701 and weatherid <=741:
            return "🌫"
        elif  weatherid==762:
            return "🌋"
        elif weatherid == 771:
            return "💨"
        elif weatherid == 781:
            return "🌪"
        elif weatherid == 800:
            return "☀️"
        elif weatherid>=801 and weatherid <=804:
            return "☁️"
        else:
            return " "



if __name__=="__main__":
    app = QApplication(sys.argv)
    weather_app = weatherapp()
    weather_app.show()
    sys.exit(app.exec_())