from openai import OpenAI
import sys
import os
import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, simpledialog, Radiobutton, StringVar, BooleanVar, Checkbutton
import pygame
import json

# https://coderslegacy.com/add-image-data-files-in-pyinstaller-exe/
# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Function to read or create the config file
def get_or_create_config():
    if not os.path.isfile(config_path):
        # If config does not exist, create it with default values
        config = {
            "api_key": None,
            "voice": "echo",
            "hd_quality": False,
            "output_directory": bundle_dir,
            "filename": "marshmallow.mp3"
        }
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        # Read existing config
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
    return config

# Function to select directory
def select_directory():
    directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, directory)

# Function to paste text from clipboard
def paste_from_clipboard():
    try:
        # Get text from clipboard
        clipboard_text = window.clipboard_get()
        # Delete any existing text in the entry
        text_entry.delete(0, tk.END)
        # Insert text from clipboard
        text_entry.insert(0, clipboard_text)
        text_entry.config(fg=default_fg)
    except tk.TclError:
        # Handle exception if there is no text in the clipboard
        pass

# Function that will be called when the button is clicked
def on_button_click():
    input_text = text_entry.get()
    voice_selection = voice_var.get()
    hd_quality = hd_var.get()
    output_directory = directory_entry.get()
    filename = filename_entry.get()

    audio_filename = os.path.join(output_directory, filename if filename else "marshmallow.mp3")
    print("Performing text to speech...")

    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_selection,
        input=input_text
    )
    response.stream_to_file(audio_filename)
    print("Done.")

    # Load the mp3 file
    pygame.mixer.music.load(audio_filename)
    
    # Play the mp3 file
    pygame.mixer.music.play()

# Placeholder setup functions
def add_placeholder(entry, placeholder_text):
    if not entry.get():
        entry.insert(0, placeholder_text)
        entry.config(fg='grey')

def clear_placeholder(event):
    if event.widget.get() == "Enter text here or paste from clipboard.":
        event.widget.delete(0, tk.END)
    event.widget.config(fg=default_fg)

if getattr(sys, 'frozen', False):
    # The application is frozen (bundled by PyInstaller)
    bundle_dir = sys._MEIPASS
    campfire_png_path = os.path.join(bundle_dir, 'campfire.png')
else:
    # The application is not frozen (running from a script)
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    campfire_png_path = os.path.join(bundle_dir, 'resources', 'campfire.png')

home_path = os.path.expanduser("~")
config_path = f'{home_path}/.campfire.config.json'

# Load or create config
config = get_or_create_config()

# Initialize the pygame mixer
pygame.mixer.init()

# Check if the API key is in the config, if not, prompt for it
api_key = config.get('api_key')

if not api_key:
    # If the API key is not set in the config, ask the user to input it
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    api_key = simpledialog.askstring("API Key", "Enter your OpenAI API key:", parent=root)
    root.destroy()  # Destroy the root window after input
    if api_key:  # Save the provided API key back to the config file if it was given
        config['api_key'] = api_key
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)

if not api_key:
    raise ValueError("No OpenAI API key provided")

# Set the API key in the environment
os.environ['OPENAI_API_KEY'] = api_key

# Create a new Tkinter window
window = tk.Tk()
window.title("Campfire")

# Set the window size
window.geometry('725x500')  # Increased the height to accommodate the settings header and separator

# Create a frame for the logo, text entry, and paste button
top_frame = tk.Frame(window)
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

logo_image = PhotoImage(file=campfire_png_path)

# Create a label to display the logo image and place it to the left of the text box
logo_label = tk.Label(top_frame, image=logo_image)
logo_label.pack(side=tk.LEFT, padx=5)

# Create the text entry widget and place it next to the logo
text_entry = tk.Entry(top_frame, width=50)
text_entry.pack(side=tk.LEFT, padx=5)
# set the default foreground color before setting placeholder text
default_fg = text_entry.cget('fg')

add_placeholder(text_entry, "Enter text here or paste from clipboard.")


# Binding the focus in and focus out events to add and clear placeholder text
text_entry.bind("<FocusIn>", clear_placeholder)
text_entry.bind("<FocusOut>", lambda event: add_placeholder(text_entry, "Enter text here or paste from clipboard."))

# Create the paste button
paste_button = tk.Button(top_frame, text="Paste", command=paste_from_clipboard)
paste_button.pack(side=tk.LEFT, padx=5)

# Create the button to submit the input text
listen_button = tk.Button(top_frame, text="Listen", command=on_button_click)
listen_button.pack(side=tk.LEFT, padx=5)

# Separator and Settings header
settings_header_frame = tk.Frame(window)
settings_header_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
settings_label = tk.Label(settings_header_frame, text="Settings", font=('Arial', 12, 'bold'))
settings_label.pack(side=tk.LEFT, anchor=tk.W)
separator = ttk.Separator(window, orient='horizontal')
separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

# Voice options
voice_var = StringVar(value=config.get("voice"))
voices_frame = tk.LabelFrame(window, text="Voice")
voices_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Loop to create radio buttons for voice options
for voice in ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]:
    rb = Radiobutton(voices_frame, text=voice.capitalize(), variable=voice_var, value=voice)
    rb.pack(anchor=tk.W)

# HD quality option
hd_var = BooleanVar(value=config.get("hd_quality"))
hd_frame = tk.Frame(window)
hd_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
hd_label = tk.Label(hd_frame, text="HD (better quality)")
hd_label.pack()
hd_yes = Radiobutton(hd_frame, text="Yes", variable=hd_var, value=True)
hd_yes.pack(anchor=tk.W)
hd_no = Radiobutton(hd_frame, text="No", variable=hd_var, value=False)
hd_no.pack(anchor=tk.W)

# Filename entry frame
filename_frame = tk.Frame(window)
filename_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

filename_label = tk.Label(filename_frame, text="Filename:")
filename_label.pack(side=tk.LEFT, padx=5)

filename_entry = tk.Entry(filename_frame, width=20)
filename_entry.insert(0, config.get("filename"))
filename_entry.pack(side=tk.LEFT, padx=5)

# Directory picker frame
directory_frame = tk.Frame(window)
directory_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

directory_button = tk.Button(directory_frame, text="Select Directory", command=select_directory)
directory_button.pack(side=tk.LEFT, padx=5)

directory_entry = tk.Entry(directory_frame, width=50)
directory_entry.insert(0, config.get("output_directory"))
directory_entry.pack(side=tk.LEFT, padx=5)

# Run the Tkinter event loop
window.mainloop()