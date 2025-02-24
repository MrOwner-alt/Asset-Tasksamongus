import sys
import webbrowser
import requests
import time
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

# Download URLs
DOWNLOAD_TASKS = {
    "Game Launcher": "https://drive.google.com/uc?export=download&id=19XadHajpOThi_-_2oDTu55kUe9iilpd9",
    "Singleplayer": "https://drive.google.com/uc?export=download&id=1kliZq9eYqKPcdxl0F7ZbAO11kimolPZ7",
    "Credits": "https://drive.google.com/uc?export=download&id=1kUbsymO_D8txE9EVcp4iBvZkY4bcKyXX",
    "Multiplayer": "https://drive.google.com/uc?export=download&id=1Jep7Bl9dDFq9netCuUUjNZ1OojuEed4C",
    "Sound File": "https://drive.google.com/uc?export=download&id=1hwFxJqYxoagG_oWyWAdQMd_Ghhd0nxbL",
}

OLDER_INSTALLER_URL = "addones.html"
download_speed_limit = None

def set_download_speed_limit():
    """Set the download speed limit."""
    global download_speed_limit
    root = tk.Tk()
    root.withdraw()
    speed = simpledialog.askinteger("Speed Limit", "Enter download speed limit in KB/s (0 for no limit):", minvalue=0)
    root.destroy()
    download_speed_limit = speed if speed is not None else None
    if download_speed_limit is not None:
        print(f"🔧 Download speed limit set to: {download_speed_limit} KB/s")

def download_file(url, file_name):
    """Download a file and save it locally."""
    try:
        print(f"📥 Starting download: {file_name}")
        
        # First request to get the confirmation token
        response = requests.get(url, stream=True)
        if "confirm=" in response.url:  # Check if we need to confirm
            confirm_token = response.url.split("confirm=")[1].split("&")[0]
            url = f"{url}&confirm={confirm_token}"  # Append the confirmation token to the URL

        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(file_name, "wb") as file:
            total_downloaded = 0
            chunk_size = 8192
            for chunk in response.iter_content(chunk_size=chunk_size):
                if download_speed_limit is not None:
                    total_downloaded += len(chunk)
                    file.write(chunk)
                    if total_downloaded / 1024 > download_speed_limit:  # Convert to KB
                        time.sleep(1)  # Pause to limit speed
                        total_downloaded = 0  # Reset after pause
                else:
                    file.write(chunk)
        print(f"✅ Downloaded: {file_name}")
    except requests.RequestException as e:
        print(f"❌ Failed to download {file_name}: {e}")

def show_install_popup():
    """Ask if the user wants to launch the older installer first."""
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askyesno(
        "Installation Options",
        "⚠️ RECOMMENDED: Install files via the older installer (addones.html) for the best experience.\n\n"
        "Would you like to launch the older installer now?\n\n"
        "Yes → Opens older installer\n"
        "No → Continue with this installer"
    )
    root.destroy()
    
    if response:
        webbrowser.open(OLDER_INSTALLER_URL)  # Open the installer webpage
        sys.exit()  # Exit after opening installer
    return response  # False means "No", so continue normally

def choose_download_mode():
    """Ask how the user wants to download files."""
    root = tk.Tk()
    root.withdraw()
    choice = simpledialog.askstring(
        "Download Mode",
        "Choose download mode:\n\n"
        "1. Type 'all' to download all files (ZIP or raw)\n"
        "2. Type 'custom' to visit links and choose per file\n"
        "3. Type 'select' to download specific files from the list."
    )
    root.destroy()

    if choice is None:
        sys.exit()  # Exit if user cancels
    elif choice.lower() == "custom":
        return "custom"
    elif choice.lower() == "select":
        return "select"
    return "all"

def choose_download_format():
    """Ask if the user wants to download as ZIP or raw."""
    root = tk.Tk()
    root.withdraw()
    choice = simpledialog.askstring(
        "Download Format",
        "Choose download format:\n\n1. Type 'zip' for ZIP format\n"
        "2. Type 'raw' for raw files"
    )
    root.destroy()
    
    if choice is None:
        sys.exit()  # Exit if user cancels
    return "zip" if choice.lower() == "zip" else "raw"

def install_all_files(download_format):
    """Download all files based on the chosen format."""
    print("\n⚠️ WARNING: The service is currently under maintenance!")
    print("This does not affect installation, but it may slow down downloads or cause file corruption.\n")

    for task_name, url in DOWNLOAD_TASKS.items():
        file_extension = ".zip" if download_format == "zip" else ""  # Add ".zip" if chosen
        file_name = f"{task_name.replace(' ', '_')}{file_extension}"
        
        print(f"🔽 Downloading {task_name} as {'ZIP' if download_format == 'zip' else 'raw file'}...")
        download_file(url, file_name)

    print("\n✅ All files downloaded successfully.")

def custom_download():
    """Allow the user to visit each link and choose format per file."""
    print("\n🌐 Opening download links...")

    for task_name, url in DOWNLOAD_TASKS.items():
        root = tk.Tk()
        root.withdraw()
        choice = simpledialog.askstring(
            "Custom Download",
            f"{task_name}:\nDo you want to download it as ZIP or raw?\n\n"
            "Type 'zip' for ZIP\nType 'raw' for raw\nType 'visit' to open link in browser"
        )
        root.destroy()

        if choice is None:
            sys.exit()  # Exit if user cancels
        elif choice.lower() == "visit":
            webbrowser.open(url)
        else:
            file_extension = ".zip" if choice.lower() == "zip" else ""  
            file_name = f"{task_name.replace(' ', '_')}{file_extension}"
            download_file(url, file_name)

    print("\n✅ Custom downloads completed.")

def select_files_to_download():
    """Allow the user to choose specific files to download."""
    print("\n📝 Select files to download (comma-separated):")
    for index, task_name in enumerate(DOWNLOAD_TASKS.keys(), start=1):
        print(f"{index}. {task_name}")
    
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("Select Files", "Enter numbers separated by commas:")
    root.destroy()
    
    if user_input is None:
        sys.exit()  # Exit if user cancels

    selected_indices = [int(num.strip()) for num in user_input.split(",") if num.strip().isdigit()]
    print(f"🔍 Selected indices: {selected_indices}")

    for index in selected_indices:
        if 1 <= index <= len(DOWNLOAD_TASKS):
            task_name = list(DOWNLOAD_TASKS.keys())[index - 1]
            url = DOWNLOAD_TASKS[task_name]
            download_format = choose_download_format()  # Ask for ZIP or raw
            file_extension = ".zip" if download_format == "zip" else ""
            file_name = f"{task_name.replace(' ', '_')}{file_extension}"
            print(f"🔽 Downloading {task_name} as {'ZIP' if download_format == 'zip' else 'raw file'}...")
            download_file(url, file_name)
        else:
            print(f"❌ Invalid index: {index}")

    print("\n✅ Selected files downloaded successfully.")

def create_main_menu():
    """Create the main menu for UI."""
    root = tk.Tk()
    root.title("File Download Manager")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0)

    # Buttons for each action
    install_button = ttk.Button(frame, text="Install Files", command=lambda: main())
    install_button.grid(row=0, column=0, padx=5, pady=5)

    speed_limit_button = ttk.Button(frame, text="Set Download Speed Limit", command=set_download_speed_limit)
    speed_limit_button.grid(row=1, column=0, padx=5, pady=5)

    root.mainloop()

def main():
    """Main function."""
    if not show_install_popup():  # If user clicks "No", continue
        download_mode = choose_download_mode()

        if download_mode == "all":
            download_format = choose_download_format()  # Ask for ZIP or raw
            install_all_files(download_format)
        elif download_mode == "custom":
            custom_download()
        elif download_mode == "select":
            select_files_to_download()

    sys.exit()

if __name__ == "__main__":
    create_main_menu()
