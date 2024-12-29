import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime

AU_DISTANCE = 1.5e8  # 1 AU in kilometers
SOLAR_RADIUS = 696340  # Solar radius in kilometers

# Function to calculate Vp and Transit Time
def calculate_vp():
    try:
        # Retrieve user inputs
        Vfrt = float(entry_vfrt.get())
        Vlat = float(entry_vlat.get())
        Vsw = float(entry_vsw.get())
        AW = float(entry_aw.get())
        
        # Compute Vp using the given equation
        Vp = (3.2320 * Vfrt) + (0.7796 * Vlat) + (0.5618 * Vsw) + (-0.1087 * AW) - 205.1152
        Vp = round(Vp, 0)

        # Calculate Transit Time
        transit_time = AU_DISTANCE / (Vp * 3600)  # In hours
        transit_time = round(transit_time, 2)

        # Display Results
        label_result.config(text=f"Vp = {Vp:.2f} km/s\nTransit Time = {transit_time:.2f} hours")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for all inputs.")

# Function to calculate Vfrt and Vlat from height-time data
def calculate_speed():
    try:
        # Get the data from user input
        time_data = [time.strip() for time in entry_time.get("1.0", "end").splitlines() if time.strip()]
        height_data = [float(height.strip()) for height in entry_height.get("1.0", "end").splitlines() if height.strip()]
        
        if len(time_data) < 3 or len(height_data) < 3:
            raise ValueError("Please provide at least 3 time-height pairs.")
        if len(time_data) != len(height_data):
            raise ValueError("Time and height data must have the same number of entries.")

        # Convert time to seconds and height to kilometers
        times_in_seconds = [
            sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.split(":")))) for time in time_data
        ]
        heights_in_km = [height * SOLAR_RADIUS for height in height_data]

        # Calculate speeds using finite differences
        front_speeds = [(heights_in_km[i+1] - heights_in_km[i]) / (times_in_seconds[i+1] - times_in_seconds[i])
                        for i in range(len(times_in_seconds) - 1)]
        
        # Use average speeds for Vfrt and Vlat
        avg_speed = round(sum(front_speeds) / len(front_speeds), 2)
        
        # Inform the user of the calculated speeds
        messagebox.showinfo("Speed Calculated", f"Calculated Front/Lateral Speed: {avg_speed:.2f} km/s")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate speed: {e}")


        # Convert time to seconds and height to kilometers
        times_in_seconds = [
            sum(int(x) * 60 ** i for i, x in enumerate(reversed(time.split(":")))) for time in time_data
        ]
        heights_in_km = [height * SOLAR_RADIUS for height in height_data]

        # Calculate speeds using finite differences
        front_speeds = [(heights_in_km[i+1] - heights_in_km[i]) / (times_in_seconds[i+1] - times_in_seconds[i])
                        for i in range(len(times_in_seconds) - 1)]
        
        # Use average speeds for Vfrt and Vlat
        avg_speed = round(sum(front_speeds) / len(front_speeds), 2)
        
        # Update input fields
        entry_vfrt.delete(0, tk.END)
        entry_vlat.delete(0, tk.END)
        entry_vfrt.insert(0, f"{avg_speed:.2f}")
        entry_vlat.insert(0, f"{avg_speed:.2f}")
        messagebox.showinfo("Speed Calculated", f"Front/Lateral speed: {avg_speed:.2f} km/s")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate speeds: {e}")

# Create the main application window
root = tk.Tk()
root.title("The Regression-Based Model")
root.geometry("600x800")
root.configure(bg="#1a1a2e")

# Get the correct path to the bundled image
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load background image
try:
    image_path = resource_path("shock4.png")
    image = Image.open(image_path).resize((480, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=photo, bg="#1a1a2e")
    label_image.image = photo
    label_image.pack(pady=5)
except FileNotFoundError:
    print("Background image not found.")

# Header
label_header = tk.Label(root, text="RGBM", font=("Helvetica", 16, "bold"), fg="white", bg="#1a1a2e")
label_header.pack(pady=10)
label_header = tk.Label(root, text="CME/ICME Propagation Speed/Transit Time Estimator", font=("Helvetica", 12, "bold"), fg="white", bg="#1a1a2e")
label_header.pack(pady=10)

# Input Fields Frame
frame_inputs = tk.Frame(root, bg="#1a1a2e")
frame_inputs.pack(pady=5)

def create_input_field(parent, label_text):
    frame = tk.Frame(parent, bg="#1a1a2e")
    frame.pack(pady=5, anchor="w")
    label = tk.Label(frame, text=label_text, font=("Helvetica", 10), fg="white", bg="#1a1a2e")
    label.pack(side="left", padx=8)
    entry = tk.Entry(frame, font=("Helvetica", 10))
    entry.pack(side="left")
    return entry

entry_vfrt = create_input_field(frame_inputs, "Vfrt (Front expansion speed):")
entry_vlat = create_input_field(frame_inputs, "Vlat (Lateral expansion speed):")
entry_vsw = create_input_field(frame_inputs, "Vsw (Solar wind speed):")
entry_aw = create_input_field(frame_inputs, "AW (Angular width):")

# Height-Time Data Frame
frame_ht = tk.Frame(root, bg="#1a1a2e", highlightbackground="white", highlightthickness=1)
frame_ht.pack(pady=5)

label_ht = tk.Label(frame_ht, text="Height-Time Data (for Vfrt/Vlat)", font=("Helvetica", 10, "bold"), fg="white", bg="#1a1a2e")
label_ht.pack(pady=5)

entry_time = tk.Text(frame_ht, height=5, width=15, font=("Helvetica", 10))
entry_time.pack(side="left", padx=5)
entry_time.insert("1.0", "hh:mm:ss\nhh:mm:ss")

entry_height = tk.Text(frame_ht, height=5, width=15, font=("Helvetica", 10))
entry_height.pack(side="left", padx=5)
entry_height.insert("1.0", "Solar Radii\n...")

button_ht = tk.Button(frame_ht, text="Calculate Speed", font=("Helvetica", 10, "bold"), command=calculate_speed)
button_ht.pack(pady=5)

# Calculate Button
button_calculate = tk.Button(
    root, text="Calculate Vp & Transit Time", font=("Helvetica", 10, "bold"),
    bg="#0f3460", fg="white", command=calculate_vp
)
button_calculate.pack(pady=5)

# Results Label
label_result = tk.Label(root, text="", font=("Helvetica", 10), fg="#00ffdd", bg="#1a1a2e")
label_result.pack(pady=5)

# Footer
label_footer = tk.Label(root, text="@ Kwabena Kyeremateng, SERL, E-JUST", font=("Helvetica", 9), fg="gray", bg="#1a1a2e")
label_footer.pack(pady=5)

# Run the application
root.mainloop()
