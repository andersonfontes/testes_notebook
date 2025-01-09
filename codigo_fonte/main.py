# Atualizações no main.py
import tkinter as tk
import os
import json
import webbrowser
from generate_report import generate_pdf_report
from test_initial import test_initial
from test_camera import test_camera
from test_sound import test_sound
from test_keyboard import test_keyboard
from final_screen import show_final_screen

def main():
    # Variáveis globais
    test_results = []

    # Verifica ou cria diretórios para PDF e JSON
    os.makedirs("PDF", exist_ok=True)
    os.makedirs("JSON", exist_ok=True)

    def finalize_tests():
        # Obtém os valores necessários para o cabeçalho
        serial_number = initial_result.get("equipment_number", "desconhecido")
        bios_serial = initial_result.get("bios_serial", "desconhecido")
        windows_activation = initial_result.get("windows_activation", "desconhecido")
        battery_status = initial_result.get("battery_health", "desconhecido")
        battery_health_percentage = initial_result.get("battery_health_percentage", "desconhecido")  # Extraindo o novo valor

        pdf_file = os.path.join("PDF", f"test_{serial_number}.pdf")
        json_file = os.path.join("JSON", f"test_{serial_number}.json")

        # Salva JSON
        with open(json_file, "w") as jf:
            json.dump(test_results, jf, indent=4)

        # Gera o PDF
        try:
            generate_pdf_report(
                results=test_results,
                screenshots=[camera_result[1]],
                technician_name=initial_result.get("technician_name", ""),
                serial_number=serial_number,
                bios_serial=bios_serial,
                windows_activation=windows_activation,
                battery_status=battery_status,
                battery_health_percentage=battery_health_percentage,  # Passa o novo argumento
                pdf_path=pdf_file
            )
            webbrowser.open_new_tab(pdf_file)
        except Exception as e:
            print(f"Erro ao gerar relatório PDF: {e}")

        # Chama a tela final
        show_final_screen(
            pdf_file=pdf_file,
            json_file=json_file,
            restart_callback=main,
            close_callback=lambda: None
        )
        
   

    # Teste Inicial
    try:
        initial_result = test_initial()
        test_results.append({"test_name": "Teste Inicial", "result": initial_result})
    except Exception as e:
        print(f"Erro no Teste Inicial: {e}")

    # Teste de Câmera
    try:
        camera_result = test_camera()
        test_results.append({"test_name": "Câmera", "result": camera_result[0]})
    except Exception as e:
        print(f"Erro no Teste de Câmera: {e}")

    # Teste de Som
    try:
        sound_result = test_sound()
        sound_summary = f"Microfone: {sound_result['microfone']}, Fone de Ouvido: {sound_result['fone']}"
        test_results.append({"test_name": "Som", "result": sound_summary})
    except Exception as e:
        print(f"Erro no Teste de Som: {e}")

    # Teste de Teclado
    try:
        keyboard_result = test_keyboard()
        test_results.append({"test_name": "Teclado", "result": "Funcionando" if keyboard_result["status"] == "OK" else f"Falha: {', '.join(keyboard_result['untested_keys'])}"})
    except Exception as e:
        print(f"Erro no Teste de Teclado: {e}")

    finalize_tests()

if __name__ == "__main__":
    main()
