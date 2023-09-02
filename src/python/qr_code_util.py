


import cv2
import qrcode
from pyzbar.pyzbar import decode 
import pygame




class QRCodeUtil:

    def __init__(self):
        pass




    def criar_qrcode(self, conteudo, qrcode_version, box_size):

        qr = qrcode.QRCode(
            version=qrcode_version,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=10,
        )
        qr.add_data(conteudo)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Convert the PIL image to a Pygame surface
        img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

        return img_surface




    def ler_qrcode(self, frame):

        # Converte o quadro OpenCV para grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decodifica os QR Codes na imagem
        decoded_objects = decode(frame_gray)

        for obj in decoded_objects:
            if obj.type == 'QRCODE':
                return obj.data.decode('utf-8')  # Retorna o conteúdo do QR Code

        return None  # Retorna None se nenhum QR Code for encontrado
    


