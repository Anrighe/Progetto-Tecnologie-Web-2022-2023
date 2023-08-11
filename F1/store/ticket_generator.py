from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
import os


def generate_ticket(id_ordine, nome, cognome, nome_circuito, settore, data_evento, posto):
    '''Genera un biglietto in formato pdf e ritorna il percorso al pdf generato'''
    current_path = os.getcwd()
    logo_path = f'{current_path}/static/images/F1-Logo.png'

    ticket_path = f'static/tickets/Ordine_{id_ordine}_{nome}_{cognome}.pdf'

    ticket_canvas = canvas.Canvas(ticket_path)

    # Importing custom F1 font #C:\\Python\\Progetto-Tecnologie-Web-2022-2023\\F1\\static\\font\\Formula1-Regular_web_0.ttf
    pdfmetrics.registerFont(TTFont('F1-font-regular', f'{current_path}/static/font/Formula1-Regular_web_0.ttf'))

    ticket_canvas.setPageSize((360, 720))

    ticket_canvas.setStrokeColorRGB(0.16, 0.137, 0.321)

    ticket_canvas.setFillColorRGB(0.16, 0.137, 0.321)

    ticket_canvas.rect(5, 5, 350, 710, fill=1)


    ticket_canvas.setStrokeColorRGB(1, 1, 1)
    ticket_canvas.rect(10, 10, 340, 700, stroke=1, fill=0)

    ticket_canvas.setDash(2, 1)
    ticket_canvas.line(10, 325, 350, 325)

    ticket_canvas.setFillColorRGB(1, 1, 1)
    ticket_canvas.setFont('F1-font-regular', 22)
    ticket_canvas.drawString(135, 670, 'F1 - 2023')

    ticket_canvas.setFont('F1-font-regular', 28)
    ticket_canvas.drawString(75, 610, 'Il tuo biglietto')

    ticket_canvas.setFont('F1-font-regular', 22)
    ticket_canvas.drawString(30, 275, f'Numero posto: {posto}')
    ticket_canvas.setFont('F1-font-regular', 16)
    ticket_canvas.drawString(30, 200, f'Nominativo: {nome} {cognome}')
    ticket_canvas.drawString(30, 125, f'Circuito: {nome_circuito} - Settore {settore}')
    ticket_canvas.drawString(30, 50, f'Data: {data_evento}')

    ticket_canvas.drawImage(logo_path, 35, 700-42, width=76, height=42, preserveAspectRatio=True, mask='auto')

    # Dati del qr-code
    data = f'{nome} {cognome}, {nome_circuito} - {settore}, {data_evento}, ID Ordine: {id_ordine}, Numero posto: {posto}'
    qrcode_image = qrcode.make(data)
    qrcode_path = f'{current_path}/static/tickets/qr.png'
    qrcode_image.save(qrcode_path)

    ticket_canvas.drawImage(qrcode_path, 70, 355, width=225, height=225, preserveAspectRatio=True, mask='auto')

    ticket_canvas.save()

    return ticket_path

#generate_ticket(1, 'Enrico', 'Marras', 'Circuito 1', '1', '10/08/2023', 55)
