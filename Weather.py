import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests

# Window settings
win = tk.Tk()
win.title("WeathApp")
win.geometry("450x350")
win.minsize(450, 300)
win.maxsize(500, 600)
win.rowconfigure(26, weight=10)
icon = tk.PhotoImage(file='umb.png')
win.iconphoto(False, icon)

# Default settings
location = 'Moscow'
api = '68ff8c52647f4e5f9fc154455231307'
base_url = 'http://api.weatherapi.com/v1'

# List to keep track of all weather icon labels
weather_icon_labels = []


# The block of functions
# Function to change city on button click
def set_city():
    try:
        test_location = new_city.get()
        test_url = f'{base_url}/current.json?key={api}&q={test_location}&aqi=no'
        test_resp = requests.get(test_url).json()
        test_loc = test_resp['location']['name']
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
    else:
        global location
        location = test_location
        url = test_url
        global response
        response = test_resp
        for label in weather_icon_labels:
            label.destroy()
        loc['text'] = test_loc
        today_only_forecast()


# Function to show only today's weather (shown by default)
def today_only_forecast():
    for label in weather_icon_labels:
        label.destroy()

    # API request
    url = f'{base_url}/current.json?key={api}&q={location}&aqi=no'
    response = requests.get(url).json()
    date = response['location']['localtime'][:10]
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

    # Today's Weather widgets (shown by default)
    # 1.1.City
    win_city = tk.Label(win, font=('TkDefaultFont', 14), text=city, pady=25)
    win_city.grid(column=0, row=5, sticky='e')

    # 1.2.Day
    today = tk.Label(win,
                     text='Today (' + date + ')',
                     fg='#5B8B9D',
                     font='Calibri 9 underline',
                     padx=50,
                     pady=10)
    today.grid(column=0, row=6, sticky='w')

    # 1.3.Timezone
    local_time = tk.Label(win, text='Local time', font=('Technic', 10), padx=50)
    local_time.grid(column=0, row=7, sticky='w')
    win_day_night = tk.Label(win, text=day_night)
    win_day_night.grid(column=1, row=7)
    win_time = tk.Label(win, text=time)
    win_time.grid(column=2, row=7)

    # 1.4.Temp
    temp = tk.Label(win, text='Temp', padx=50, font=('Technic', 10))
    temp.grid(column=0, row=8, sticky='w')
    win_temp_celsius = tk.Label(win, text=temp_celsius, padx=0, pady=0)
    win_temp_celsius.grid(column=1, row=8)
    win_temp_fahrenheit = tk.Label(win, text=temp_fahrenheit, padx=0, pady=0)
    win_temp_fahrenheit.grid(column=2, row=8)

    # 1.5.Sky
    sky = tk.Label(win, text='Sky', padx=50, font=('Technic', 10))
    sky.grid(column=0, row=9, sticky='w')
    win_weather = tk.Label(win, text=weather)
    win_weather.grid(column=1, row=9)
    win_clouds = tk.Label(win, text=clouds)
    win_clouds.grid(column=2, row=9)

    # 1.6.Wind
    wind = tk.Label(win, text='Wind', padx=50, font=('Technic', 10))
    wind.grid(column=0, row=10, sticky='w')
    win_wind_km = tk.Label(win, text=str(wind_km) + ' km/h')
    win_wind_km.grid(column=1, row=10)
    win_wind_ml = tk.Label(win, text=str(wind_miles) + ' mph')
    win_wind_ml.grid(column=2, row=10)

    # 1.7.Weather icon
    win_weather_icon = tk.Label(win)
    win_weather_icon.grid(column=1, row=5, sticky='we')
    icon_url = f'https:{weather_icon}'
    icon_response = requests.get(icon_url, stream=True)
    image_bytes = icon_response.raw.read()
    img = ImageTk.PhotoImage(Image.open(BytesIO(image_bytes)))
    win_weather_icon.config(image=img)
    win_weather_icon.image = img

    weather_icon_labels.append(local_time)
    weather_icon_labels.append(win_day_night)
    weather_icon_labels.append(win_time)
    weather_icon_labels.append(temp)
    weather_icon_labels.append(sky)
    weather_icon_labels.append(wind)
    weather_icon_labels.append(win_city)
    weather_icon_labels.append(win_day_night)
    weather_icon_labels.append(win_time)
    weather_icon_labels.append(win_temp_celsius)
    weather_icon_labels.append(win_temp_fahrenheit)
    weather_icon_labels.append(win_weather)
    weather_icon_labels.append(win_clouds)
    weather_icon_labels.append(win_wind_km)
    weather_icon_labels.append(win_wind_ml)
    weather_icon_labels.append(win_weather_icon)


# Function to show icon in 3-day forecast
def icon_forecast(column, row, icon_source, type):
    sky_icon = tk.Label(win)
    if type == 'morning':
        sky_icon.grid(columnspan=2, row=row)
    else:
        sky_icon.grid(column=column, row=row)
    img = Image.open(BytesIO(icon_source.content))
    img = img.resize((30, 30))
    img = ImageTk.PhotoImage(img)
    sky_icon.config(image=img)
    sky_icon.image = img
    weather_icon_labels.append(sky_icon)

# Function to show 3-day forecast
def forecast():

    # Hide today's widgets
    for label in weather_icon_labels:
        label.destroy()

    # API request
    url_forecast = f'{base_url}/forecast.json?key={api}&q={location}&days=3&aqi=yes&alerts=yes'
    forecast_response = requests.get(url_forecast).json()

    # Show city
    city = forecast_response['location']['name']
    win_city = tk.Label(win, font=('TkDefaultFont', 14), text=city, pady=25)
    win_city.grid(column=0, row=5, sticky='e')

    # Current weather icon
    weather_icon = forecast_response['current']['condition']['icon']
    win_weather_icon = tk.Label(win)
    win_weather_icon.grid(column=1, row=5, sticky='we')
    icon_url = f'https:{weather_icon}'
    icon_response = requests.get(icon_url, stream=True)
    image_bytes = icon_response.raw.read()
    img = ImageTk.PhotoImage(Image.open(BytesIO(image_bytes)))
    win_weather_icon.config(image=img)
    win_weather_icon.image = img

    # 2. Variables for 3 days weather
    # 2.1. First day
    # Morning
    first_day = forecast_response['forecast']['forecastday'][0]['date']
    first_day_morning_temp = str(round(forecast_response['forecast']['forecastday'][0]['hour'][11]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][0]['hour'][11]['temp_f'])) + ' \N{DEGREE SIGN}F'
    first_day_morning_weather = forecast_response['forecast']['forecastday'][0]['hour'][11]['condition']['icon']
    first_morning_icon_url = f'https:{first_day_morning_weather}'
    first_morning_icon_response = requests.get(first_morning_icon_url, stream=True)
    # Midday
    first_day_midday_temp = str(round(forecast_response['forecast']['forecastday'][0]['hour'][15]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][0]['hour'][15]['temp_f'])) + ' \N{DEGREE SIGN}F'
    first_day_midday_weather = forecast_response['forecast']['forecastday'][0]['hour'][15]['condition']['icon']
    first_day_midday_wind_km = forecast_response['forecast']['forecastday'][0]['hour'][15]['wind_kph']
    first_day_midday_wind_ml = forecast_response['forecast']['forecastday'][0]['hour'][15]['wind_mph']
    first_midday_icon_url = f'https:{first_day_morning_weather}'
    first_midday_icon_response = requests.get(first_morning_icon_url, stream=True)
    # Night
    first_day_night_temp = str(round(forecast_response['forecast']['forecastday'][0]['hour'][22]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][0]['hour'][22]['temp_f'])) + ' \N{DEGREE SIGN}F'
    first_day_night_weather = forecast_response['forecast']['forecastday'][0]['hour'][22]['condition']['icon']
    first_night_icon_url = f'https:{first_day_night_weather}'
    first_night_icon_response = requests.get(first_night_icon_url, stream=True)
    # 2.2. Second day
    # Morning
    second_day = forecast_response['forecast']['forecastday'][1]['date']
    second_day_morning_temp = str(round(forecast_response['forecast']['forecastday'][1]['hour'][11]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][1]['hour'][11]['temp_f'])) + ' \N{DEGREE SIGN}F'
    second_day_morning_weather = forecast_response['forecast']['forecastday'][1]['hour'][11]['condition']['icon']
    second_morning_icon_url = f'https:{second_day_morning_weather}'
    second_morning_icon_response = requests.get(second_morning_icon_url, stream=True)
    # Midday
    second_day_midday_temp = str(round(forecast_response['forecast']['forecastday'][1]['hour'][15]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][1]['hour'][15]['temp_f'])) + ' \N{DEGREE SIGN}F'
    second_day_midday_weather = forecast_response['forecast']['forecastday'][1]['hour'][15]['condition']['icon']
    second_midday_icon_url = f'https:{second_day_midday_weather}'
    second_midday_icon_response = requests.get(second_midday_icon_url, stream=True)
    # Night
    second_day_night_temp = str(round(forecast_response['forecast']['forecastday'][1]['hour'][22]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][1]['hour'][22]['temp_f'])) + ' \N{DEGREE SIGN}F'
    second_day_night_weather = forecast_response['forecast']['forecastday'][1]['hour'][22]['condition']['icon']
    second_night_icon_url = f'https:{second_day_night_weather}'
    second_night_icon_response = requests.get(second_night_icon_url, stream=True)

    # 2.3. Third day
    # Morning
    third_day = forecast_response['forecast']['forecastday'][2]['date']
    third_day_morning_temp = str(round(forecast_response['forecast']['forecastday'][2]['hour'][11]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][2]['hour'][11]['temp_f'])) + ' \N{DEGREE SIGN}F'
    third_day_morning_weather = forecast_response['forecast']['forecastday'][2]['hour'][11]['condition']['icon']
    third_morning_icon_url = f'https:{third_day_morning_weather}'
    third_morning_icon_response = requests.get(third_morning_icon_url, stream=True)
    # Midday
    third_day_midday_temp = str(round(forecast_response['forecast']['forecastday'][2]['hour'][15]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][2]['hour'][15]['temp_f'])) + ' \N{DEGREE SIGN}F'
    third_day_midday_weather = forecast_response['forecast']['forecastday'][2]['hour'][15]['condition']['icon']
    third_midday_icon_url = f'https:{third_day_midday_weather}'
    third_midday_icon_response = requests.get(third_midday_icon_url, stream=True)
    # Night
    third_day_night_temp = str(round(forecast_response['forecast']['forecastday'][2]['hour'][22]['temp_c'])) \
                                     + ' \N{DEGREE SIGN}C' + ' / ' + str(round(forecast_response['forecast']\
                                     ['forecastday'][2]['hour'][22]['temp_f'])) + ' \N{DEGREE SIGN}F'
    third_day_night_weather = forecast_response['forecast']['forecastday'][2]['hour'][22]['condition']['icon']
    third_night_icon_url = f'https:{third_day_night_weather}'
    third_night_icon_response = requests.get(third_night_icon_url, stream=True)


    # Making new widgets
    # 1st day
    today_forecast = tk.Label(win,
                     text='Today (' + first_day + ')',
                     fg='#5B8B9D',
                     font='Calibri 9 underline',
                     padx=50,
                     pady=10)
    today_forecast.grid(column=0, row=6, sticky='w')
    first_morning = tk.Label(win, text='Morning', padx=30)
    first_morning.grid(column=0, row=12, sticky='e')
    first_midday = tk.Label(win, text='Day', padx=30)
    first_midday.grid(column=1, row=12, sticky='we')
    first_night = tk.Label(win, text='Night', padx=30)
    first_night.grid(column=2, row=12, sticky='we')
    first_sky = tk.Label(win, text='Sky', padx=50, font=('Technic', 10))
    first_sky.grid(column=0, row=13, sticky='w')
    first_temp = tk.Label(win, text='Temp', padx=50, font=('Technic', 10))
    first_temp.grid(column=0, row=14, sticky='w')
    first_morning_temp = tk.Label(win, text=first_day_morning_temp)
    first_morning_temp.grid(columnspan=2, row=14)
    first_midday_temp = tk.Label(win, text=first_day_midday_temp)
    first_midday_temp.grid(column=1, row=14)
    first_night_temp = tk.Label(win, text=first_day_night_temp)
    first_night_temp.grid(column=2, row=14)

    # Adding labels to list
    weather_icon_labels.append(today_forecast)
    weather_icon_labels.append(first_morning)
    weather_icon_labels.append(first_midday)
    weather_icon_labels.append(first_night)
    weather_icon_labels.append(first_sky)
    weather_icon_labels.append(first_temp)
    weather_icon_labels.append(first_morning_temp)
    weather_icon_labels.append(first_midday_temp)
    weather_icon_labels.append(first_night_temp)
    weather_icon_labels.append(win_city)

    # Morning weather icon
    icon_forecast(0, 13, first_morning_icon_response, 'morning')
    # Midday weather icon
    icon_forecast(1, 13, first_midday_icon_response, 0)
    # Night weather icon
    icon_forecast(2, 13, first_night_icon_response, 0)

    # 2nd day
    tomorrow_forecast = tk.Label(win,
                     text='Tomorrow (' + second_day + ')',
                     fg='#5B8B9D',
                     font='Calibri 9 underline',
                     padx=50,
                     pady=10)
    tomorrow_forecast.grid(column=0, row=16, sticky='w')
    second_morning = tk.Label(win, text='Morning', padx=30)
    second_morning.grid(column=0, row=17, sticky='e')
    second_midday = tk.Label(win, text='Day', padx=30)
    second_midday.grid(column=1, row=17, sticky='we')
    second_night = tk.Label(win, text='Night', padx=30)
    second_night.grid(column=2, row=17, sticky='we')
    second_sky = tk.Label(win, text='Sky', padx=50, font=('Technic', 10))
    second_sky.grid(column=0, row=18, sticky='w')
    second_temp = tk.Label(win, text='Temp', padx=50, font=('Technic', 10))
    second_temp.grid(column=0, row=19, sticky='w')
    second_morning_temp = tk.Label(win, text=second_day_morning_temp, padx=0, pady=0)
    second_morning_temp.grid(columnspan=2, row=19)
    second_midday_temp = tk.Label(win, text=second_day_midday_temp)
    second_midday_temp.grid(column=1, row=19)
    second_night_temp = tk.Label(win, text=second_day_night_temp)
    second_night_temp.grid(column=2, row=19)

    # Adding labels to list
    weather_icon_labels.append(tomorrow_forecast)
    weather_icon_labels.append(second_morning)
    weather_icon_labels.append(second_midday)
    weather_icon_labels.append(second_night)
    weather_icon_labels.append(second_sky)
    weather_icon_labels.append(second_temp)
    weather_icon_labels.append(second_morning_temp)
    weather_icon_labels.append(second_midday_temp)
    weather_icon_labels.append(second_night_temp)

    # Morning weather icon
    icon_forecast(0, 18, second_morning_icon_response, 'morning')
    # Midday weather icon
    icon_forecast(1, 18, second_midday_icon_response, 0)
    # Night weather icon
    icon_forecast(2, 18, second_night_icon_response, 0)

    # 3nd day
    third_forecast = tk.Label(win,
                     text='Next day (' + third_day + ')',
                     fg='#5B8B9D',
                     font='Calibri 9 underline',
                     padx=50,
                     pady=10)
    third_forecast.grid(column=0, row=21, sticky='w')
    third_morning = tk.Label(win, text='Morning', padx=30)
    third_morning.grid(column=0, row=22, sticky='e')
    third_midday = tk.Label(win, text='Day', padx=30)
    third_midday.grid(column=1, row=22, sticky='we')
    third_night = tk.Label(win, text='Night', padx=30)
    third_night.grid(column=2, row=22, sticky='we')
    third_sky = tk.Label(win, text='Sky', padx=50, font=('Technic', 10))
    third_sky.grid(column=0, row=23, sticky='w')
    third_temp = tk.Label(win, text='Temp', padx=50, font=('Technic', 10))
    third_temp.grid(column=0, row=24, sticky='w')
    third_morning_temp = tk.Label(win, text=third_day_morning_temp)
    third_morning_temp.grid(columnspan=2, row=24)
    third_midday_temp = tk.Label(win, text=third_day_midday_temp)
    third_midday_temp.grid(column=1, row=24)
    third_night_temp = tk.Label(win, text=third_day_night_temp)
    third_night_temp.grid(column=2, row=24)

    # Adding labels to list
    weather_icon_labels.append(third_forecast)
    weather_icon_labels.append(third_morning)
    weather_icon_labels.append(third_midday)
    weather_icon_labels.append(third_night)
    weather_icon_labels.append(third_sky)
    weather_icon_labels.append(third_temp)
    weather_icon_labels.append(third_morning_temp)
    weather_icon_labels.append(third_midday_temp)
    weather_icon_labels.append(third_night_temp)

    # Morning weather icon
    icon_forecast(0, 23, third_morning_icon_response, 'morning')
    # Midday weather icon
    icon_forecast(1, 23, third_midday_icon_response, 0)
    # Night weather icon
    icon_forecast(2, 23, third_night_icon_response, 0)


# Making widgets in window
# Current city
tk.Label(win,
         text='Your current city:',
         font=('Technic', 10),
         padx=50,
         pady=5).grid(column=0, row=1, sticky='w')
loc = tk.Label(win,
               text=str(location),
               padx=35,
               pady=5)
loc.grid(column=1, row=1, columnspan=2, sticky='we')

# Area to type new city
tk.Label(win,
         text="New city:",
         font=('Technic', 10),
         padx=50).grid(column=0, row=2, sticky='w')

new_city = ttk.Entry(win, width=17)
new_city.grid(column=1, row=2)

# Choosing options of weather
choose_weather_option = tk.Label(win,
                                 text='Weather option',
                                 font=('Technic', 10),
                                 padx=50)
choose_weather_option.grid(row=3, column=0, sticky='w')

# Button of changing the city
change_city = ttk.Button(win, text='Change city', command=set_city)
change_city.grid(column=2, row=2, sticky='we')

# Button to choose only current weather
one_day_weather = ttk.Button(win, text='Today', command=today_only_forecast)
one_day_weather.grid(column=1, row=3, sticky='we')

# Button to choose 3 days forecast
three_days_weather = ttk.Button(win, text='3 days', command=forecast, width=17)
three_days_weather.grid(column=2, row=3, sticky='we')


# Developer's name
dev_label = tk.Label(win, text="Developed by A. Novotochin \u00A9", font=('Arial', 8), bg='white', fg='grey')
dev_label.grid(column=0, row=26, sticky='sw')

# Showing today's forecast by default
today_only_forecast()

win.mainloop()
