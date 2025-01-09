from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_pdf_report(results, screenshots, technician_name, serial_number, bios_serial, windows_activation, battery_status, battery_health_percentage, pdf_path):
    # Configuração da página
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setTitle("Relatório de Teste de Hardware")

    # Margens e configurações gerais
    left_margin = 50  # Margem esquerda
    top_margin = 750  # Margem superior
    line_height = 14  # Altura de cada linha
    spacing = 1.3  # Espaçamento entre linhas no cabeçalho

    # Cabeçalho
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(left_margin, top_margin, "Relatório de Teste de Hardware")
    pdf.setFont("Helvetica", 12)
    pdf.line(left_margin, top_margin - 20, 550, top_margin - 20)

    # Informações gerais do cabeçalho
    header_info = [
        f"Técnico: {technician_name}",
        f"Número do Equipamento: {serial_number}",
        f"Serial da BIOS: {bios_serial}",
        f"Ativação do Windows: {windows_activation}",
        f"Bateria: {battery_status}",
        f"Saúde da Bateria: {battery_health_percentage}%",
    ]
    y_position = top_margin - 40
    for info in header_info:
        pdf.drawString(left_margin, y_position, info)
        y_position -= line_height * spacing

    # Resultados dos Testes
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(left_margin, y_position - 10, "Resultados dos Testes:")
    y_position -= 30
    pdf.setFont("Helvetica", 10)

    for result in results:
        test_name = result.get("test_name", "Desconhecido")
        test_result = result.get("result", "Sem resultado")

        if test_name == "Teste Inicial" and isinstance(test_result, dict):
            continue
            # pdf.setFont("Helvetica-Bold", 11)
            # pdf.drawString(left_margin, y_position, "Teste Inicial:")
            # y_position -= line_height
            # pdf.setFont("Helvetica", 10)
            # for key, value in test_result.items():
            #     # Remove informações que já estão no cabeçalho
            #     if key in ["bios_serial", "battery_health", "battery_health_percentage", "windows_activation", "equipment_number"]:
            #         continue
            #     elif key == "bios_match":
            #         pdf.drawString(left_margin + 20, y_position, f"- Compatibilidade da BIOS: {value}")
            #     y_position -= line_height

        elif test_name == "Câmera":
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(left_margin, y_position, "Câmera:")
            y_position -= line_height
            pdf.setFont("Helvetica", 10)
            if isinstance(test_result, dict):
                for key, value in test_result.items():
                    if key == "test_name":
                        continue  # Ignorar o nome do teste
                    pdf.drawString(left_margin + 20, y_position, f"- Resultado: {value}")
            else:
                pdf.drawString(left_margin + 20, y_position, f"- Resultado: {test_result}")
            y_position -= line_height

        elif test_name == "Som":
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(left_margin, y_position, "Som:")
            y_position -= line_height
            pdf.setFont("Helvetica", 10)
            pdf.drawString(left_margin + 20, y_position, f"- {test_result}")
            y_position -= line_height

        elif test_name == "Teclado":
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(left_margin, y_position, "Teclado:")
            y_position -= line_height
            pdf.setFont("Helvetica", 10)
            pdf.drawString(left_margin + 20, y_position, f"- {test_result}")
            y_position -= line_height

        # Verifica se precisa de uma nova página
        if y_position < 50:
            pdf.showPage()
            y_position = top_margin - 20
            pdf.setFont("Helvetica", 10)

    # Capturas de tela (se houver)
    if screenshots:
        for screenshot in screenshots:
            if y_position < 200:
                pdf.showPage()
                y_position = top_margin - 20
            pdf.drawImage(screenshot, left_margin, y_position - 200, width=200, height=150)
            y_position -= 220

    # Borda fina ao redor do conteúdo
    pdf.rect(left_margin - 10, 50, 500, top_margin - 30)

    pdf.save()
