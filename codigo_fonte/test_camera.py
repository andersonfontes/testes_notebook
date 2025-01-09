import tkinter as tk
from PIL import Image, ImageTk
import cv2

def test_camera():
    result = {"test_name": "Camera", "result": "incompleto"}  # Valor padrão inicial
    screenshot_path = "camera_test_photo.png"

    video_width, video_height = 320, 240

    cap = cv2.VideoCapture(0)

    def update_frame():
        if cap.isOpened():  # Verifica se a captura está aberta antes de tentar atualizar
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (video_width, video_height))
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)
            video_label.after(10, update_frame)

    def take_photo():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (video_width, video_height))
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img.save(screenshot_path)
            photo = ImageTk.PhotoImage(img)
            photo_label.configure(image=photo)
            photo_label.image = photo
            cap.release()
            video_label.pack_forget()
            take_photo_button.pack_forget()
            message_label.config(text="A câmera está funcionando corretamente?")
            yes_button.pack(side="left", padx=10, pady=10)
            no_button.pack(side="right", padx=10, pady=10)

    def confirm_ok():
        result["result"] = "ok"
        root.destroy()

    def confirm_fail():
        result["result"] = "falha"
        root.destroy()

    def try_again():
        root.destroy()
        test_camera()

    root = tk.Tk()
    root.title("Teste de Camera")
    root.geometry(f"{video_width + 40}x{video_height + 200}")

    tk.Label(root, text="Teste de Câmera: verifique se a câmera está funcionando.").pack(pady=10)
    video_label = tk.Label(root)
    video_label.pack()

    take_photo_button = tk.Button(root, text="Tirar Foto", command=take_photo)
    take_photo_button.pack(pady=10)

    photo_label = tk.Label(root)
    photo_label.pack()

    message_label = tk.Label(root, text="")
    message_label.pack(pady=10)

    yes_button = tk.Button(root, text="Funcionando", command=confirm_ok)
    novamente_button = tk.Button(root, text="Tentar Novamente", command=try_again)
    no_button = tk.Button(root, text="Não Funcionando", command=confirm_fail)

    novamente_button.pack()

    # Inicia o feed de vídeo e garante que update_frame pare ao fechar a janela
    update_frame()
    root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy()))
    root.mainloop()

    return result, screenshot_path
