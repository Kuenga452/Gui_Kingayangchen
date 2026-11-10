import tkinter as tk


# Create the main window
window = tk.Tk()

window.title("Tkinter Hello World")
window.geometry("350x200")

# Create a label
label = tk.Label(
    window,
    text="Hello, World!",
    font=("Arial", 20, "bold")
)
label.pack(pady=20)


# Function to handle button click
def show_message():
    label.config(text="Welcome to Tkinter!")


# Create a button
button = tk.Button(
    window,
    text="Click Me",
    command=show_message
)
button.pack(pady=10)


# Run the application
window.mainloop()