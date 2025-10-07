from tkinter import *
from tkinter import messagebox, filedialog, ttk
from PIL import Image
import base64
from googletrans import Translator  # Install with: pip install googletrans==4.0.0-rc1


# Function to encode a message in an image using LSB steganography
def encode_message_in_image(image_path, encrypted_message, output_image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")

    # Add delimiter to the encrypted message
    encrypted_message_with_delimiter = encrypted_message + "###END###"
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message_with_delimiter)

    # Ensure the image has enough pixels to hold the message
    width, height = img.size
    pixels = img.load()

    if len(binary_message) > width * height * 3:
        raise ValueError("Message is too large to encode in the selected image!")

    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Iterate over RGB values
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & 0xFE | int(binary_message[data_index])  # Modify LSB
                    data_index += 1
            pixels[x, y] = tuple(pixel)

    img.save(output_image_path)


# Function to decode the message from an image
def decode_message_from_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")

    width, height = img.size
    pixels = img.load()

    binary_message = ""
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Iterate over RGB values
                binary_message += str(pixel[i] & 1)  # Extract LSB

    # Convert binary to characters
    decoded_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        if len(byte) < 8:
            break  # Skip incomplete byte
        decoded_message += chr(int(byte, 2))

    # Detect the delimiter
    if "###END###" in decoded_message:
        return decoded_message.split("###END###")[0]
    else:
        raise ValueError("No valid hidden message found in the image!")


# Encrypt function
def encrypt():
    password = code.get()

    if password == "@maxpro":
        screen1 = Toplevel(screen)
        screen1.title("Encryption")
        screen1.geometry("400x200")
        screen1.configure(bg="#ed3833")

        message = text1.get(1.0, END).strip()

        # Encrypt the message using Base64
        encoded_message = base64.b64encode(message.encode("ascii")).decode("ascii")

        # Open file dialog to select an image for encoding
        image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.gif")])
        if not image_path:
            messagebox.showerror("Error", "No image selected!")
            return

        # Save the encrypted message into an image
        output_image_path = "output_image_with_steganography.png"
        try:
            encode_message_in_image(image_path, encoded_message, output_image_path)
            Label(screen1, text="Encrypted and Hidden in Image", font="arial", fg="white", bg="#ed3833").place(x=10, y=0)
            text2 = Text(screen1, font="Roboto 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
            text2.place(x=10, y=10, width=380, height=150)
            text2.insert(END, f"Message encrypted and hidden in image.\nOutput file saved at:\n{output_image_path}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    elif password == "":
        messagebox.showerror("Encryption", "Input password")
    elif password != "@maxpro":
        messagebox.showerror("Encryption", "Invalid Password")


# Decrypt function
def decrypt():
    password = code.get()

    if password == "@maxpro":
        screen2 = Toplevel(screen)
        screen2.title("Decryption")
        screen2.geometry("400x200")
        screen2.configure(bg="#00bd56")

        # Open file dialog to select an image for decoding
        image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", ".png;.jpg;.jpeg;.bmp;*.gif")])
        if not image_path:
            messagebox.showerror("Error", "No image selected!")
            return

        try:
            # Extract and decrypt the message from the image
            extracted_message = decode_message_from_image(image_path)
            decoded_message = base64.b64decode(extracted_message.encode("ascii")).decode("ascii")

            # Display the decrypted message
            Label(screen2, text="Decrypted Message", font="arial", fg="white", bg="#00bd56").place(x=10, y=0)
            text2 = Text(screen2, font="Roboto 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
            text2.place(x=10, y=10, width=380, height=150)
            text2.insert(END, decoded_message)

        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    elif password == "":
        messagebox.showerror("Decryption", "Input password")
    elif password != "@maxpro":
        messagebox.showerror("Decryption", "Invalid Password")


# Translator function with multiple languages
def translate_text():
    screen3 = Toplevel(screen)
    screen3.title("Translator")
    screen3.geometry("400x300")
    screen3.configure(bg="#1089ff")

    # Dictionary of supported languages
    language_codes = {
        "English": "en",
        "Kannada": "kn",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh-cn",
        "Japanese": "ja",
        "Russian": "ru",
        "Tamil": "ta",
        "Telugu": "te",
    }

    def perform_translation():
        try:
            # Get the English text from the input box
            input_text = text1.get(1.0, END).strip()

            if not input_text:
                messagebox.showerror("Error", "No text to translate!")
                return

            # Get the selected language code
            selected_language = language_dropdown.get()
            if selected_language not in language_codes:
                messagebox.showerror("Error", "Please select a valid language!")
                return

            dest_language = language_codes[selected_language]

            # Perform translation
            translator = Translator()
            translated_text = translator.translate(input_text, src="en", dest=dest_language).text

            # Display the translated text
            Label(screen3, text=f"Translated Text (English to {selected_language})", font="arial", fg="white", bg="#1089ff").place(x=10, y=50)
            text3 = Text(screen3, font="Roboto 10", bg="white", relief=GROOVE, wrap=WORD, bd=0)
            text3.place(x=10, y=80, width=380, height=150)
            text3.insert(END, translated_text)

        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

    # Label for language selection
    Label(screen3, text="Select Language:", font="arial", fg="white", bg="#1089ff").place(x=10, y=10)

    # Language dropdown menu
    language_dropdown = ttk.Combobox(screen3, values=list(language_codes.keys()), state="readonly", width=20)
    language_dropdown.place(x=150, y=10)
    language_dropdown.set("Kannada")  # Default language

    # Translate button
    Button(screen3, text="Translate", height="2", width=20, bg="#00bd56", fg="white", bd=0, command=perform_translation).place(x=100, y=240)


# Main screen setup
def main_screen():
    global screen
    global code
    global text1
    screen = Tk()
    screen.geometry("375x398")
    screen.title("Steganography App")

    def reset():
        code.set("")
        text1.delete(1.0, END)

    Label(text="Enter text for encryption, decryption, and translation", fg="black", font=("calibri", 13)).place(x=10, y=10)
    text1 = Text(font="Roboto 20", bg="white", relief=GROOVE, wrap=WORD, bd=0)
    text1.place(x=10, y=50, width=355, height=100)

    Label(text="Enter secret key for encryption and decryption", fg="black", font=("calibri", 13)).place(x=10, y=170)
    code = StringVar()
    Entry(textvariable=code, width=19, bd=0, font=("arial", 25), show="*").place(x=10, y=200)

    Button(text="ENCRYPT", height="2", width=23, bg="#ed3833", fg="white", bd=0, command=encrypt).place(x=10, y=250)
    Button(text="DECRYPT", height="2", width=23, bg="#00bd56", fg="white", bd=0, command=decrypt).place(x=200, y=250)
    Button(text="TRANSLATE", height="2", width=50, bg="#1089ff", fg="white", bd=0, command=translate_text).place(x=10, y=300)
    Button(text="RESET", height="2", width=50, bg="#1089ff", fg="white", bd=0, command=reset).place(x=10, y=350)

    screen.mainloop()


main_screen()