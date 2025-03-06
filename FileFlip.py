import os
import sys
import winreg
from PIL import Image

# Single Image Conversion Function
def convert_image(input_path, target_format):
    try:
        img = Image.open(input_path)
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{target_format.lower()}"

        if target_format.lower() == "jpg":
            img = img.convert("RGB")

        img.save(output_path, target_format.upper())
        # print(f"Converted {input_path} to {output_path}")

    except Exception as e:
        print(f"Error converting {input_path} to {target_format}: {e}")

# Register Context Menu using CommandStore
def register_context_menu():
    image_formats = {
        "png": "To PNG",
        "jpg": "To JPG",
        "bmp": "To BMP"
    }
    exe_path = sys.executable  # Path to the script's Python interpreter
    base_path = r"SystemFileAssociations\image\shell\FileFlip"
    command_store_base = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell"

    try:
        # Step 1: Create the main menu entry
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, base_path) as key:
            winreg.SetValueEx(key, "MUIVerb", 0, winreg.REG_SZ, "Convert with FileFlip")
            winreg.SetValueEx(key, "SubCommands", 0, winreg.REG_SZ, ";".join([f"FileFlip.to{fmt.upper()}" for fmt in image_formats]))

        # Step 2: Register each conversion command inside CommandStore
        for fmt, label in image_formats.items():
            command_store_path = f"{command_store_base}\\FileFlip.to{fmt.upper()}"
            command_key_path = command_store_path + "\\command"
            command = f'"{exe_path}" "to_{fmt}" "%1"'

            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, command_store_path) as subkey:
                winreg.SetValueEx(subkey, "MUIVerb", 0, winreg.REG_SZ, label)

            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, command_key_path) as cmdkey:
                winreg.SetValueEx(cmdkey, "", 0, winreg.REG_SZ, command)

        print("Context menu successfully registered with CommandStore!")

    except Exception as e:
        print(f"Failed to register context menu: {e}")

# Unregister Context Menu
def unregister_context_menu():
    base_path = r"SystemFileAssociations\image\shell\FileFlip"
    command_store_base = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell"

    try:
        # Remove main context menu entry
        try:
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, base_path)
            print("Context menu successfully unregistered!")
        except FileNotFoundError:
            print("Context menu already removed.")

        # Remove subcommands from CommandStore
        for fmt in ["PNG", "JPG", "BMP"]:
            command_store_path = f"{command_store_base}\\FileFlip.to{fmt}"
            command_key_path = command_store_path + "\\command"

            try:
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, command_key_path)
            except FileNotFoundError:
                pass

            try:
                winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, command_store_path)
            except FileNotFoundError:
                pass

    except Exception as e:
        print(f"Failed to unregister context menu: {e}")

# Main Logic
if __name__ == "__main__":
    valid_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

    if len(sys.argv) == 1:  # Register the menu
        unregister_context_menu()
        register_context_menu()
        input("Press Enter to exit...")
    elif len(sys.argv) == 3:  # Conversion requested
        action, file_path = sys.argv[1], sys.argv[2]
        ext = os.path.splitext(file_path)[1].lower()

        if ext not in valid_extensions:
            print(f"Unsupported file type: {ext}. Only images ({', '.join(valid_extensions)}) are supported.")
            sys.exit(1)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            sys.exit(1)

        current_ext = ext.lstrip(".").lower()  # e.g., "jpg" from ".jpg"
        if action.startswith("to_"):
            target_format = action[3:]
            # Skip redundant conversion (e.g., "To JPG" for .jpg files)
            if target_format == current_ext or (target_format == "jpg" and current_ext == "jpeg"):
                print(f"Redundant conversion skipped: {file_path} is already {target_format.upper()}.")
            else:
                convert_image(file_path, target_format)
        else:
            print(f"Unknown action: {action}")
    else:
        print("Invalid arguments. Run without args to register, or use via context menu.")
