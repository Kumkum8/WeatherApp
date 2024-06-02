import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk

# Function to get weather information from OpenWeatherMap API

def get_weather(city):
    API_key = "ce3052b2a027d6830ea0c28603c6943b"  
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    try:
        # Parse the response JSON to get weather information
        weather = res.json()
        icon_id = weather['weather'][0]['icon']
        temperature = weather['main']['temp'] - 273.15
        description = weather['weather'][0]['description']
        city = weather['name']
        country = weather['sys']['country']

        # Get the icon URL and return all the weather information
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        return (icon_url, temperature, description, city, country)
    except KeyError as e:
        print("KeyError:", e)
        print("API Response:", res.json())
        messagebox.showerror("Error", "An error occurred while parsing weather data. Please try again.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        messagebox.showerror("Error", "An error occurred while fetching weather data. Please try again.")
        return None

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    # If the city is found, unpack the weather information
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Get weather icon image from URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label.configure(text=f"{temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

# Set up the main application window
root = ttk.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# Entry widget to enter the city name
city_entry = ttk.Entry(root, font="sans-serif, 18")
city_entry.pack(pady=10)

# Button to search for the weather information
search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label widget to show the city/country
location_label = tk.Label(root, font="sans-serif, 25")
location_label.pack(pady=20)

# Label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show the temperature
temperature_label = tk.Label(root, font="sans-serif, 20")
temperature_label.pack()

# Label widget to show the weather description
description_label = tk.Label(root, font="sans-serif, 20")
description_label.pack()

# Run the application
root.mainloop()
