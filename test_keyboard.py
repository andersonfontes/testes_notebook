import tkinter as tk
from tkinter import messagebox

def test_keyboard():
    result = {"test_name": "Teclado", "status": "incompleto", "untested_keys": []}
    tested_keys = set()

    # Layout de teclado ANSI atualizado
    keyboard_layout = [
        ["Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
        ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
        ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
        ["Caps_Lock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
        ["Shift_L", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Control_L", "Alt_L", "space", "↑", "←", "↓", "→"]
    ]

    # Mapeamento de teclas para keycodes atualizado
    key_mapping = {
        27: "Escape", 112: "F1", 113: "F2", 114: "F3", 115: "F4", 116: "F5", 117: "F6",
        118: "F7", 119: "F8", 120: "F9", 121: "F10", 122: "F11", 123: "F12",
        192: "`", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6", 55: "7",
        56: "8", 57: "9", 48: "0", 189: "-", 187: "=", 8: "Backspace",
        9: "Tab", 81: "Q", 87: "W", 69: "E", 82: "R", 84: "T", 89: "Y", 85: "U",
        73: "I", 79: "O", 80: "P", 219: "[", 221: "]", 220: "\\",
        20: "Caps_Lock", 65: "A", 83: "S", 68: "D", 70: "F", 71: "G", 72: "H",
        74: "J", 75: "K", 76: "L", 186: ";", 222: "'", 13: "Enter",
        16: "Shift_L", 90: "Z", 88: "X", 67: "C", 86: "V", 66: "B", 78: "N",
        77: "M", 188: ",", 190: ".", 191: "/", 32: "space",
        37: "←", 38: "↑", 39: "→", 40: "↓",
        17: "Control_L", 18: "Alt_L"
    }

    def key_press(event):
        key = key_mapping.get(event.keycode, None)

        if key and key in button_refs:
            button_refs[key].config(bg="green", fg="white")
            tested_keys.add(key)

    def reset_test():
        """Reseta todas as teclas para o estado inicial."""
        tested_keys.clear()
        for btn in button_refs.values():
            btn.config(bg="lightgray", fg="black")

    def finish_test():
        untested = [key for row in keyboard_layout for key in row if key not in tested_keys]
        if not untested:
            result["status"] = "OK"
            messagebox.showinfo("Teste de Teclado", "Teclado testado e OK!")
        else:
            result["untested_keys"] = untested
            messagebox.showwarning("Teste de Teclado", f"Teclas não testadas: {', '.join(untested)}")
        root.destroy()

    root = tk.Tk()
    root.title("Teste de Teclado")
    root.geometry("1200x500")

    button_refs = {}
    frame = tk.Frame(root)
    frame.pack(pady=10)
    for row in keyboard_layout:
        row_frame = tk.Frame(frame)
        row_frame.pack()
        for key in row:
            btn_width = 6 if key not in ["Backspace", "Enter", "Shift_L", "space", "Caps_Lock", "←", "↑", "↓", "→"] else 10
            if key == "space":
                btn_width = 20
            btn = tk.Button(row_frame, text=key, width=btn_width, height=2, bg="lightgray")
            btn.pack(side="left", padx=2, pady=2)
            button_refs[key] = btn

    # Botões de controle
    control_frame = tk.Frame(root)
    control_frame.pack(pady=20)
    reset_button = tk.Button(control_frame, text="Zerar", command=reset_test)
    reset_button.pack(side="left", padx=10)
    finish_button = tk.Button(control_frame, text="Avançar", command=finish_test)
    finish_button.pack(side="left", padx=10)

    root.bind("<KeyPress>", key_press)
    root.mainloop()
    return result
