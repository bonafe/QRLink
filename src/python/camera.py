



import cv2

import pygame


from qr_code_util import QRCodeUtil



class CameraQRCode:



    def __init__(self, camera_id=0):


        self.camera_id = camera_id

        self.camera = cv2.VideoCapture(self.camera_id)


        # Verifique se a captura foi aberta com sucesso
        if not self.camera.isOpened():

            print("Erro ao abrir a câmera.")            

            exit()




    def capturar_frame(self):

        # Capture um quadro da webcam
        ret, frame = self.camera.read()

        # Para usar no pygame é preciso rotacionar o quadro
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.flip(frame, 0)

        # Verifique se a captura foi bem-sucedida
        if not ret:
            print("Erro ao capturar o quadro.")
            return None
        else:
            # Converta o quadro OpenCV em um formato Pygame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        

            return frame_rgb



    def processar_imagem_camera(self, callback):

        # Capture a frame from the camera
        frame_camera = self.capturar_frame()

        if frame_camera is not None:
            
            # Tente ler um QR Code da imagem da câmera
            qr_code_data = QRCodeUtil.ler_qrcode(cv2.cvtColor(frame_camera, cv2.COLOR_RGBA2BGR))

            if qr_code_data:

                callback(qr_code_data)                                                                            


            frame_pygame = pygame.surfarray.make_surface(frame_camera)

            return frame_pygame     