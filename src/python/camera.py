



import cv2




class Camera:



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
