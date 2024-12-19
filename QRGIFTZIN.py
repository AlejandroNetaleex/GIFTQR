import os
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import sys

# Obtener ruta del recurso (logo.png) para empaquetar con PyInstaller
def resource_path(relative_path):
    """Obtiene la ruta del archivo para ejecutables empaquetados con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        # Ruta temporal usada por PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Validar URL
def validate_url(url):
    pattern = re.compile(
        r'^(https?://)?'  # Protocolo opcional
        r'(([\w.-]+)\.([a-z\.]{2,6}))'  # Dominio
        r'([/\w .-]*)*/?$'  # Ruta opcional
    )
    return re.match(pattern, url)

# Generar código QR
def generate_qr():
    url = url_entry.get()
    qr_name = name_entry.get()

    if not validate_url(url):
        messagebox.showerror("Error", "Por favor, ingrese un enlace válido.")
        return

    if not qr_name:
        messagebox.showerror("Error", "Por favor, ingrese un nombre para el código QR.")
        return

    try:
        # Crear QR
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Agregar logo más grande
        logo_path = resource_path("logo.png")
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            logo_size = 120  # Tamaño más grande
            logo.thumbnail((logo_size, logo_size))
            qr_width, qr_height = qr_img.size
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, logo_position, mask=logo)

        # Agregar texto (nombre del código)
        try:
            font = ImageFont.truetype("arial.ttf", 18)  # Usamos la fuente Arial disponible en Windows
        except:
            font = ImageFont.load_default()  # Si no está disponible, usa la fuente predeterminada de Python

        draw = ImageDraw.Draw(qr_img)
        # Calcular el tamaño del texto con textbbox
        text_bbox = draw.textbbox((0, 0), qr_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((qr_width - text_width) // 2, qr_height - text_height - 10)
        draw.text(text_position, qr_name, fill="black", font=font)

        # Guardar QR
        folder = filedialog.askdirectory(title="Seleccione la carpeta para guardar el QR")
        if not folder:
            messagebox.showerror("Error", "Debe seleccionar una carpeta para guardar el QR.")
            return

        file_path = os.path.join(folder, f"{qr_name}.png")
        qr_img.save(file_path)

        messagebox.showinfo("Éxito", f"Código QR generado y guardado como {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el código QR: {e}")

# Interfaz gráfica
root = tk.Tk()
root.title("GiftQR - Generador de Códigos QR")
root.geometry("400x550")
root.configure(bg="#1e1e1e")  # Fondo oscuro

# Cargar logo en la interfaz
logo_path = resource_path("logo.png")
if os.path.exists(logo_path):
    try:
        logo_img = Image.open(logo_path)
        logo_img.thumbnail((150, 150))
        logo_tk = ImageTk.PhotoImage(logo_img)
        tk.Label(root, image=logo_tk, bg="#1e1e1e").pack(pady=10)
    except Exception as e:
        tk.Label(root, text="No se pudo cargar el logo.", bg="#1e1e1e", fg="#ff0000", font=("Arial", 12)).pack(pady=10)
else:
    tk.Label(root, text="Logo no encontrado.", bg="#1e1e1e", fg="#ff0000", font=("Arial", 12)).pack(pady=10)

# Título del programa
tk.Label(
    root, text="GiftQR", bg="#1e1e1e", fg="#ffffff", font=("Arial", 16, "bold")
).pack(pady=10)

# Etiquetas y campos de entrada
tk.Label(root, text="Ingrese el enlace:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=40, font=("Arial", 12), bg="#2d2d2d", fg="#ffffff")
url_entry.pack(pady=5)

tk.Label(root, text="Nombre del archivo QR:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 12)).pack(pady=5)
name_entry = tk.Entry(root, width=40, font=("Arial", 12), bg="#2d2d2d", fg="#ffffff")
name_entry.pack(pady=5)

# Botón para generar el QR
tk.Button(
    root,
    text="Generar QR",
    command=generate_qr,
    bg="#007bff",
    fg="#ffffff",
    font=("Arial", 12),
    width=20,
).pack(pady=20)

# Créditos en la parte inferior
tk.Label(
    root,
    text="© 2024 SOPORTE TI - MEJORA CONTINUA GIFTZIN. Desarrollado por Alejandro Machuca.",
    bg="#1e1e1e",
    fg="#ffffff",
    font=("Arial", 10),
    wraplength=380,
    justify="center",
).pack(side="bottom", pady=10)

# Iniciar aplicación
root.mainloop()
