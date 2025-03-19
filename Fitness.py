import tkinter as tk
from tkinter import messagebox, ttk
import json
import datetime
import csv

# File to store workout data
DATA_FILE = "workout_data.json"

# Load previous workouts from file
def load_workouts():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save workouts to file
def save_workouts(workouts):
    with open(DATA_FILE, "w") as file:
        json.dump(workouts, file, indent=4)

# Add a new workout entry
def add_workout():
    selected_exercise = exercise_var.get()
    custom_entry = custom_exercise.get()

    exercise_name = custom_entry if custom_entry else selected_exercise
    duration_text = duration_input.get()
    calories_text = calories_input.get()

    if not exercise_name or not duration_text or not calories_text:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        duration = int(duration_text)
        calories = int(calories_text)
    except ValueError:
        messagebox.showerror("Error", "Duration and Calories must be numbers.")
        return

    new_workout = {
        "date": str(datetime.date.today()),
        "exercise": exercise_name,
        "duration": duration,
        "calories": calories
    }

    workouts = load_workouts()
    workouts.append(new_workout)
    save_workouts(workouts)

    messagebox.showinfo("Success", "Workout added successfully!")
    refresh_workout_list()
    update_calories_display()
    update_progress_visual()

# Remove selected workout from list
def remove_workout():
    selected_index = workout_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Select a workout to delete.")
        return

    index = selected_index[0]
    workouts = load_workouts()
    del workouts[index]
    save_workouts(workouts)

    messagebox.showinfo("Deleted", "Workout removed.")
    refresh_workout_list()
    update_calories_display()
    update_progress_visual()

# Export data to CSV file
def export_data():
    workouts = load_workouts()
    with open("workout_history.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Exercise", "Duration (min)", "Calories Burned"])
        for workout in workouts:
            writer.writerow([workout["date"], workout["exercise"], workout["duration"], workout["calories"]])

    messagebox.showinfo("Exported", "Data saved as 'workout_history.csv'.")

# Refresh the workout list display
def refresh_workout_list():
    workouts = load_workouts()
    workout_listbox.delete(0, tk.END)
    for workout in workouts:
        workout_listbox.insert(tk.END, f"{workout['date']} | {workout['exercise']} | {workout['duration']} min | {workout['calories']} kcal")

# Update the total calories burned display
def update_calories_display():
    workouts = load_workouts()
    total_calories = sum(workout["calories"] for workout in workouts)
    calories_label.config(text=f"🔥 Total Calories Burned: {total_calories} kcal")

# Update progress visualization
def update_progress_visual():
    workouts = load_workouts()
    total_calories = sum(workout["calories"] for workout in workouts)

    progress_canvas.delete("progress")
    progress_width = min(500, (total_calories / 2000) * 500)  # Assuming goal = 2000 kcal
    progress_canvas.create_rectangle(0, 0, progress_width, 30, fill="limegreen", tags="progress")

# Set up the main window
root = tk.Tk()
root.title("R.D Fitness")
root.geometry("850x600")
root.config(bg="#1a1a1a")

# Header with App Name and Branding
header_frame = tk.Frame(root, bg="#333", pady=10)
header_frame.pack(fill=tk.X)

# Main Title (Large and Bold)
title_label = tk.Label(header_frame, text="💪 R.D FITNESS", font=("Arial", 24, "bold"), fg="lime", bg="#333")
title_label.pack(side=tk.LEFT, padx=20)

# Corner Branding (Rishi Fitness APP)
branding_label = tk.Label(header_frame, text="Rishi Fitness APP", font=("Arial", 12, "italic"), fg="white", bg="#333")
branding_label.pack(side=tk.RIGHT, padx=20)

# Left panel for inputs
input_frame = tk.Frame(root, bg="#222", padx=20, pady=20)
input_frame.pack(side=tk.LEFT, fill=tk.Y)

# Exercise dropdown
exercise_list = ["Running", "Cycling", "Yoga", "Weight Lifting", "Push-ups", "Jump Rope", "Swimming"]
exercise_var = tk.StringVar(value=exercise_list[0])

tk.Label(input_frame, text="Select Exercise:", fg="white", bg="#222").pack(pady=5)
exercise_dropdown = ttk.Combobox(input_frame, textvariable=exercise_var, values=exercise_list)
exercise_dropdown.pack(pady=5)

# Custom exercise input
tk.Label(input_frame, text="Or Enter Custom:", fg="white", bg="#222").pack(pady=5)
custom_exercise = tk.Entry(input_frame)
custom_exercise.pack(pady=5)

# Duration input
tk.Label(input_frame, text="Duration (minutes):", fg="white", bg="#222").pack(pady=5)
duration_input = tk.Entry(input_frame)
duration_input.pack(pady=5)

# Calories input
tk.Label(input_frame, text="Calories Burned:", fg="white", bg="#222").pack(pady=5)
calories_input = tk.Entry(input_frame)
calories_input.pack(pady=5)

# Buttons
button_style = {"font": ("Arial", 12), "fg": "white", "width": 20, "pady": 5}
tk.Button(input_frame, text="➕ Add Workout", bg="green", **button_style, command=add_workout).pack(pady=5)
tk.Button(input_frame, text="❌ Remove Workout", bg="red", **button_style, command=remove_workout).pack(pady=5)
tk.Button(input_frame, text="📂 Export to CSV", bg="purple", **button_style, command=export_data).pack(pady=5)

# Right panel for history & progress
history_frame = tk.Frame(root, bg="#1a1a1a", padx=20, pady=20)
history_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

# Workout history
tk.Label(history_frame, text="Workout History 📋", font=("Arial", 14, "bold"), fg="white", bg="#1a1a1a").pack()
workout_listbox = tk.Listbox(history_frame, width=50, height=10, font=("Arial", 10), bg="#333", fg="white")
workout_listbox.pack(pady=10)

# Calories burned
calories_label = tk.Label(history_frame, text="🔥 Total Calories Burned: 0 kcal", font=("Arial", 12, "bold"), fg="yellow", bg="#1a1a1a")
calories_label.pack(pady=10)

# Progress bar
tk.Label(history_frame, text="🔥 Progress Towards Goal", font=("Arial", 12, "bold"), fg="white", bg="#1a1a1a").pack(pady=5)
progress_canvas = tk.Canvas(history_frame, width=500, height=30, bg="gray")
progress_canvas.pack(pady=10)

# Initialize UI with saved data
refresh_workout_list()
update_calories_display()
update_progress_visual()

# Run the app
root.mainloop()
