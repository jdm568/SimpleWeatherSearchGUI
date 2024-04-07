from tkinter import *
from tkinter import messagebox
import requests
import json

def get_weather(latitude, longitude):
    delete_text()
    res = requests.get(f"https://api.weather.gov/points/{latitude},{longitude}")
    if res.status_code == 404:
        messagebox.showerror("Error", "Cannot find city forecast. Please try again.")
        return None
      
    json = res.json()
    forecast = json["properties"]["forecast"]
    daily_forecast = requests.get(forecast).json()

    for section in daily_forecast["properties"]["periods"]:
        day = section["name"]
        temp = section["temperature"]
        detail = section["detailedForecast"]
        add_text(f"{day}: {temp} \n")

def get_city():
    choice=city_select.get()
    if choice is None:
        return
    lat_lon=city_latlon[choice]
    lat.set(lat_lon[0])
    lon.set(lat_lon[1])
    get_weather(lat.get(),lon.get())

def add_text(text):
    test_widget.insert(END, text)

def delete_text():
    test_widget.delete("1.0", "end")
    
root = Tk()
root.geometry("600x600") 
root.title("Weather App")

lat = StringVar()
lat.set("")
lon = StringVar()
lon.set("")

city_select = StringVar()
city_select.set("Select a City")
cities = ["California", "Colorado", "Connecticut", "Delaware", "Florida"]
city_latlon = {"California": ["36.1700", "-119.7462"],
               "Colorado": ["39.0646", "-105.3272"],
              "Connecticut": ["41.5834", "-72.7622"],
              "Delaware": ["39.3498", "-75.5148"],
              "Florida": ["27.8333", "-81.7170"]}

lat_label = Label(root, text="Enter Latitude")
lat_entry = Entry(root, width=35, borderwidth=5, textvariable=lat)

lon_label = Label(root, text="Enter Longitude")
lon_entry = Entry(root, width=35, borderwidth=5, textvariable=lon)

forecast_button = Button(root, font = 24, text = "Get Forecast", 
                command=lambda: get_weather(lat.get(), lon.get()))

close_button = Button(root, font = 24, text = "Exit", 
                command=root.destroy)

dropdown = OptionMenu(root, city_select, *city_latlon)
choose_button = Button(root, text="Select", command=get_city)

test_widget = Text(root, font = ("Helvitica", "16"),
                  height=10, width=25)

dropdown.pack(pady=20)
lat_label.pack()
lat_entry.pack()
lon_label.pack()
lon_entry.pack()
choose_button.pack(pady=10)
forecast_button.pack(pady=10)
test_widget.pack()
close_button.pack(pady=10)

root.mainloop()