import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests


# Function to change city in program
def set_city():
    location = new_city.get()
    loc['text'] = str(location)
    base_url = 'http://api.weatherapi.com/v1'
    api = '68ff8c52647f4e5f9fc154455231307'
    url = f'{base_url}/current.json?key={api}&q={location}&aqi=no'
    try:
        response = requests.get(url).json()

        # Assigning the necessary variables from response
        city = response['location']['name']
        day_night = response['current']['is_day']
        if day_night == 1:
            day_night = 'Day'
        else:
            day_night = 'Night'
        time = response['location']['localtime'][-5:]
        temp_celsius = str(response['current']['temp_c']) + ' \N{DEGREE SIGN}C'
        temp_fahrenheit = str(response['current']['temp_f']) + ' \N{DEGREE SIGN}F'
        weather = response['current']['condition']['text']
        weather_icon = response['current']['condition']['icon']
        wind_miles = response['current']['wind_mph']
        wind_km = response['current']['wind_kph']
        clouds = response['current']['cloud']
        if clouds < 30:
            clouds = 'Low clouds'
        elif clouds < 60:
            clouds = 'Average clouds'
        else:
            clouds = 'Heavy clouds'
        # img = tk.PhotoImage(file=weather_icon)
        # tk.Label(win,
        #         image=img
        # )
        win_city['text'] = city
        win_day_night['text'] = day_night
        win_time['text'] = time
        win_temp['text'] = temp_celsius
        win_temp_fahrenheit['text'] = temp_fahrenheit
        win_weather['text'] = weather
        win_clouds['text'] = clouds
        win_wind_km['text'] = str(wind_km) + ' km/h'
        win_wind_ml['text'] = str(wind_miles) + ' mph/h'

        # Get the image for the weather icon and display it using a Label widget
        icon_url = f"https:{weather_icon}"
        icon_response = requests.get(icon_url, stream=True)
        image_bytes = icon_response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(image_bytes)))
        win_weather_icon.config(image=img)
        win_weather_icon.image = img

    except:
        error = tk.Tk()
        error.title("Error")
        error.geometry("200x100")
        error.minsize(200, 100)
        error.maxsize(200, 100)
        tk.Label(error,
                 text="Wrong city",
                 padx=70,
                 pady=30).grid(column=0, row=0)


# Window settings
win = tk.Tk()
win.title("WeathApp")
win.geometry("450x350")
win.minsize(450, 300)
win.maxsize(500, 500)
win.rowconfigure(9, weight=10)
icon = tk.PhotoImage(file='umb.png')
win.iconphoto(False, icon)

# Default location
location = 'Moscow'

# Making widgets in window
tk.Label(win,
         text='Your current city:',
         font=('Technic', 10),
         padx=50,
         pady=5).grid(column=0, row=1, sticky='w')
loc = tk.Label(win,
               text=str(location),
               padx=35,
               pady=5)
loc.grid(column=1, row=1, columnspan=2, sticky='w')
tk.Label(win,
         text="New city:",
         font=('Technic', 10),
         padx=50).grid(column=0, row=2, sticky='w')

new_city = ttk.Entry(win, width=20)
new_city.grid(column=1, row=2)
change_city = ttk.Button(win, text='Change city', command=set_city)
change_city.grid(column=1, row=3, sticky='we')

# API request
base_url = 'http://api.weatherapi.com/v1'
api = '68ff8c52647f4e5f9fc154455231307'
url = f'{base_url}/current.json?key={api}&q={location}&aqi=no'
response = requests.get(url).json()

# Response info to display
city = response['location']['name']
temp_celsius = str(response['current']['temp_c']) + ' \N{DEGREE SIGN}C'
temp_fahrenheit = str(response['current']['temp_f']) + ' \N{DEGREE SIGN}F'
day_night = response['current']['is_day']
if day_night == 1:
    day_night = 'Day'
else:
    day_night = 'Night'
time = response['location']['localtime'][-5:]
weather = response['current']['condition']['text']
weather_icon = response['current']['condition']['icon']
clouds = response['current']['cloud']
if clouds < 30:
    clouds = 'Low clouds'
elif clouds < 60:
    clouds = 'Average clouds'
else:
    clouds = 'Heavy clouds'
wind_km = response['current']['wind_kph']
wind_miles = response['current']['wind_mph']

# Weather widgets
# 1.City
win_city = tk.Label(win, font=('TkDefaultFont', 14), text=city, pady=25)
win_city.grid(column = 0, row=4, sticky='e')

# 2.Timezone
tk.Label(win, text='Local time', font=('Technic', 10), padx=50).grid(column=0, row=5, sticky='w')
win_day_night = tk.Label(win, text=day_night)
win_day_night.grid(column=1, row=5)
win_time = tk.Label(win, text=time)
win_time.grid(column=2, row=5)

# 3.Temperature
tk.Label(win, text='Temperature', padx=50, font=('Technic', 10)).grid(column=0, row=6, sticky='w')
win_temp = tk.Label(win, text=temp_celsius, padx=0, pady=0)
win_temp.grid(column=1, row=6)
win_temp_fahrenheit = tk.Label(win, text=temp_fahrenheit, padx=0, pady=0)
win_temp_fahrenheit.grid(column=2, row=6)

# 4.Sky
tk.Label(win, text='Sky', padx=50, font=('Technic', 10)).grid(column=0, row=7, sticky='w')
win_weather = tk.Label(win, text=weather)
win_weather.grid(column=1, row=7)
win_clouds = tk.Label(win, text=clouds)
win_clouds.grid(column=2, row=7)

# 5.Wind
tk.Label(win, text='Wind', padx=50, font=('Technic', 10)).grid(column=0, row=8, sticky='w')
win_wind_km = tk.Label(win, text=str(wind_km) + ' km/h')
win_wind_km.grid(column=1, row=8)
win_wind_ml = tk.Label(win, text=str(wind_miles) + ' mph')
win_wind_ml.grid(column=2, row=8)

# 6.Weather icon
win_weather_icon = tk.Label(win)
win_weather_icon.grid(column=1, row=4, sticky='we')
icon_url = f'https:{weather_icon}'
icon_response = requests.get(icon_url, stream=True)
image_bytes = icon_response.raw.read()
img = ImageTk.PhotoImage(Image.open(BytesIO(image_bytes)))
win_weather_icon.config(image=img)
win_weather_icon.image = img

dev_label = tk.Label(win, text="Developed by A. Novotochin \u00A9", font=('Arial', 8), bg='white', fg='grey')
dev_label.grid(column=0, row=9, sticky='sw')

win.mainloop()
