import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import numpy as np

def test_sound():
    # Estrutura de resultado padronizada, consistência com o JSON e relatórios
    result = {"test_name": "Som", "microfone": "incompleto", "fone": "incompleto"}

    sample_rate = 44100
    duration = 3
    recording = None

    def record_audio():
        nonlocal recording
        try:
            messagebox.showinfo("Gravação", "Gravando áudio por 3 segundos... Faça barulho para testar.")
            recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
            sd.wait()
            messagebox.showinfo("Gravação Concluída", "Reproduzindo a gravação.")
            sd.play(recording, samplerate=sample_rate)
            sd.wait()
            confirm_microphone()
        except Exception as e:
            print(f"[Erro] Falha ao gravar o áudio: {e}")
            result["microfone"] = "falha"
            root.destroy()

    def confirm_microphone():
        heard = messagebox.askyesno("Confirmação", "Você conseguiu ouvir a gravação no alto-falante?")
        result["microfone"] = "ok" if heard else "falha"
        mic_label.config(text=f"Microfone: {'OK ✅' if heard else 'Falha ❌'}", fg="green" if heard else "red")
        print(f"[Debug] Microfone confirmado como {'OK' if heard else 'Falha'}")
        proceed_headphone_test()

    def proceed_headphone_test():
        messagebox.showinfo("Teste de Fone", "Conecte o fone de ouvido e clique em 'Testar Fone' para continuar.")

    def play_headphone_test():
        try:
            if recording is not None:
                sd.play(recording, samplerate=sample_rate)
                sd.wait()
                heard = messagebox.askyesno("Confirmação", "Você ouviu o som no fone de ouvido?")
                result["fone"] = "ok" if heard else "falha"
                headphone_label.config(text=f"Fone de Ouvido: {'OK ✅' if heard else 'Falha ❌'}", fg="green" if heard else "red")
                print(f"[Debug] Fone de Ouvido confirmado como {'OK' if heard else 'Falha'}")
            else:
                messagebox.showerror("Erro", "Nenhuma gravação encontrada para reproduzir.")
            root.destroy()
        except Exception as e:
            print(f"[Erro] Falha ao reproduzir o áudio: {e}")
            result["fone"] = "falha"
            root.destroy()

    # Interface Tkinter
    root = tk.Tk()
    root.title("Teste de Som")
    root.geometry("400x300")

    tk.Label(root, text="Teste de Som: verifique o funcionamento do microfone e do fone de ouvido.").pack(pady=10)

    mic_label = tk.Label(root, text="Microfone: Pendente")
    mic_label.pack(pady=5)

    headphone_label = tk.Label(root, text="Fone de Ouvido: Pendente")
    headphone_label.pack(pady=5)

    tk.Button(root, text="Iniciar Teste de Microfone", command=record_audio).pack(pady=10)
    tk.Button(root, text="Iniciar Teste de Fone", command=play_headphone_test).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    root.mainloop()

    # Retorna o resultado final padronizado para uso direto no relatório
    return result
