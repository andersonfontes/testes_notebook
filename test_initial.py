import tkinter as tk
from tkinter import messagebox
import wmi
import psutil
import json
import subprocess
from check_battery import get_battery_health  # Função modularizada para saúde da bateria

def get_bios_serial():
    try:
        c = wmi.WMI()
        bios_serial = c.Win32_BIOS()[0].SerialNumber.strip()
        return bios_serial
    except Exception as e:
        print(f"Erro ao obter o número de série da BIOS: {e}")
        return "Desconhecido"

def get_battery_health_percentage():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent
    return "Desconhecido"

def check_windows_activation():
    # Verifica o status de ativação do Windows
    try:
        cmd = 'powershell "(Get-WmiObject -query \'select * from SoftwareLicensingProduct where PartialProductKey is not null\').LicenseStatus"'
        output = subprocess.check_output(cmd, shell=True, text=True)
        return "Ativado" if "1" in output else "Não Ativado"
    except Exception as e:
        print(f"Erro ao verificar a ativação do Windows: {e}")
        return "Desconhecido"

def test_initial():
    bios_serial = get_bios_serial()
    battery_health_percentage = get_battery_health_percentage()
    battery_health = get_battery_health()  # Inclui a saúde da bateria
    windows_activation = check_windows_activation()  # Inclui o status de ativação do Windows

    result_data = {
        "bios_serial": bios_serial,
        "battery_health_percentage": battery_health_percentage,
        "battery_health": battery_health,
        "windows_activation": windows_activation,
        "technician_name": "",
        "equipment_number": "",
        "bios_match": False
    }

    def auto_check_serial(event=None):
        entered_serial = input_serial.get()
        if len(entered_serial) == len(bios_serial):
            if entered_serial == bios_serial:
                result_data["bios_match"] = True
                check_label.config(text="✔️", fg="green")
                btn_submit.config(state=tk.NORMAL)
            else:
                result_data["bios_match"] = False
                check_label.config(text="❌", fg="red")
                messagebox.showerror("Erro", "Número de série incorreto. Tente novamente.")
                input_serial.delete(0, tk.END)
                btn_submit.config(state=tk.DISABLED)

    def on_submit():
        result_data["technician_name"] = input_technician_name.get()
        result_data["equipment_number"] = input_equipment_number.get()
        root.quit()

        # Grava os dados em um arquivo JSON para persistência
        with open("initial_test_results.json", "w") as json_file:
            json.dump(result_data, json_file, indent=4)
        print("Dados gravados em initial_test_results.json")

    root = tk.Tk()
    root.title("Teste Inicial")
    root.geometry("400x450")

    tk.Label(root, text="Número de Série da BIOS:").pack(anchor="w", padx=10)
    label_bios_serial_value = tk.Label(root, text=bios_serial, font=("Arial", 12, "bold"), fg="blue")
    label_bios_serial_value.pack(anchor="w", padx=10)

    tk.Label(root, text="Número de Série da Etiqueta (Escaneie ou Digite):").pack(anchor="w", padx=10)
    input_serial = tk.Entry(root, width=30)
    input_serial.pack(anchor="w", padx=10)
    input_serial.bind("<KeyRelease>", auto_check_serial)

    check_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
    check_label.pack(anchor="w", padx=10)

    tk.Label(root, text="Número do Equipamento:").pack(anchor="w", padx=10)
    input_equipment_number = tk.Entry(root, width=30)
    input_equipment_number.pack(anchor="w", padx=10)

    # Exibe a carga da bateria
    tk.Label(root, text="Carga da Bateria:").pack(anchor="w", padx=10)
    label_battery_health_percentage = tk.Label(root, text=f"{battery_health_percentage}%", font=("Arial", 12, "bold"), fg="green")
    label_battery_health_percentage.pack(anchor="w", padx=10)

    # Exibe a saúde da bateria
    tk.Label(root, text="Saúde da Bateria:").pack(anchor="w", padx=10)
    label_battery_health_value = tk.Label(root, text=battery_health, font=("Arial", 12, "bold"), fg="green")
    label_battery_health_value.pack(anchor="w", padx=10)

    # Exibe a ativação do Windows
    tk.Label(root, text="Ativação do Windows:").pack(anchor="w", padx=10)
    label_activation_status = tk.Label(root, text=windows_activation, font=("Arial", 12, "bold"), fg="blue")
    label_activation_status.pack(anchor="w", padx=10)

    tk.Label(root, text="Nome do Técnico:").pack(anchor="w", padx=10)
    input_technician_name = tk.Entry(root, width=30)
    input_technician_name.pack(anchor="w", padx=10)

    btn_submit = tk.Button(root, text="Avançar", command=on_submit, state=tk.DISABLED)
    btn_submit.pack(pady=10)

    root.mainloop()
    root.destroy()

    return result_data
