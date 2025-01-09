import tkinter as tk
from tkinter import filedialog
import os

def show_final_screen(pdf_file, json_file, restart_callback, close_callback):
    def save_as_pdf():
        dest = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if dest:
            os.replace(pdf_file, dest)

    def save_as_json():
        dest = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if dest:
            os.replace(json_file, dest)

    def restart():
        root.destroy()
        restart_callback()

    def close():
        root.destroy()
        close_callback()
        
        

    root = tk.Tk()
    root.title("Testes Finalizados")
    tk.Label(root, text="Testes finalizados. O relatório foi gerado com sucesso.").pack(pady=10)
    tk.Button(root, text="Salvar cópia do PDF como...", command=save_as_pdf).pack(pady=5)
    tk.Button(root, text="Salvar JSON como...", command=save_as_json).pack(pady=5)
    tk.Button(root, text="Reiniciar testes", command=restart).pack(pady=5)
    tk.Button(root, text="Fechar programa", command=close).pack(pady=5)

    root.mainloop()
