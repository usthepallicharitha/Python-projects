import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from datetime import datetime

# ================= CONFIG =================
API_KEY = "f86fe6cc97faa2be6889159a7d153bf7"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ================= WINDOW =================
root = tk.Tk()
root.title("Global Weather App")
root.geometry("950x550")
root.configure(bg="#0f172a")

# ================= FUNCTIONS =================
def get_weather():
    city = city_entry.get().strip()
    if city == "":
        messagebox.showerror("Error", "Enter City Name (Ex: Delhi or Delhi,IN)")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        data = requests.get(CURRENT_URL, params=params).json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", "City not found")
            return

        update_current_weather(data)
        update_forecast(data["coord"]["lat"], data["coord"]["lon"])

    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_current_weather(data):
    city_label.config(text=f"{data['name']}, {data['sys']['country']}")
    temp_label.config(text=f"{data['main']['temp']} °C")
    desc_label.config(text=data["weather"][0]["description"].title())

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    details.config(text=f"""
Feels Like : {data['main']['feels_like']} °C
Min Temp   : {data['main']['temp_min']} °C
Max Temp   : {data['main']['temp_max']} °C
Humidity   : {data['main']['humidity']} %
Pressure   : {data['main']['pressure']} hPa
Wind Speed : {data['wind']['speed']} m/s
Sunrise    : {sunrise}
Sunset     : {sunset}
""")

    set_icon(data["weather"][0]["main"])


def update_forecast(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    data = requests.get(FORECAST_URL, params=params).json()
    forecast_box.delete("1.0", tk.END)

    forecast_box.insert(tk.END, "5-Day Weather Forecast:\n\n")
    for item in data["list"][::8]:  # Daily forecast
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"].title()
        forecast_box.insert(tk.END, f"{date} → {temp} °C | {desc}\n")


def set_icon(condition):
    icons = {
        "Clear": "icons/clear.png",
        "Clouds": "icons/clouds.png",
        "Rain": "icons/rain.png",
        "Snow": "icons/snow.png",
        "Thunderstorm": "icons/thunder.png",
        "Mist": "icons/mist.png"
    }

    path = icons.get(condition, "icons/clouds.png")
    img = Image.open(path).resize((120, 120))
    img = ImageTk.PhotoImage(img)
    icon_label.config(image=img)
    icon_label.image = img

# ================= UI =================
tk.Label(root, text="🌍 Global Weather Report",
         font=("Segoe UI", 26, "bold"),
         fg="white", bg="#0f172a").pack(pady=10)

search = tk.Frame(root, bg="#0f172a")
search.pack()

city_entry = tk.Entry(search, font=("Arial", 14), width=28)
city_entry.pack(side="left", padx=10)

tk.Button(search, text="Get Weather",
          font=("Arial", 12, "bold"),
          bg="#22c55e", fg="black",
          command=get_weather).pack(side="left")

content = tk.Frame(root, bg="#0f172a")
content.pack(fill="both", expand=True, pady=20)

left = tk.Frame(content, bg="#0f172a")
left.pack(side="left", padx=40)

city_label = tk.Label(left, font=("Arial", 22),
                      fg="white", bg="#0f172a")
city_label.pack()

temp_label = tk.Label(left, font=("Arial", 48, "bold"),
                      fg="#22c55e", bg="#0f172a")
temp_label.pack()

desc_label = tk.Label(left, font=("Arial", 16),
                      fg="white", bg="#0f172a")
desc_label.pack()

icon_label = tk.Label(left, bg="#0f172a")
icon_label.pack(pady=10)

right = tk.Frame(content, bg="#1e293b", padx=20, pady=20)
right.pack(side="right", fill="both", expand=True)

details = tk.Label(right, font=("Arial", 14),
                   fg="white", bg="#1e293b", justify="left")
details.pack(anchor="w")

forecast_box = tk.Text(right, height=10, font=("Arial", 12),
                       bg="#020617", fg="#e5e7eb")
forecast_box.pack(fill="both", expand=True, pady=10)

# ================= RUN =================
root.mainloop()