
import cv2


import numpy as np
from qrcode import QRCode
import pygame

from io import BytesIO
import tempfile


import random
import time
import datetime


from camera import Camera

from metricas_qrlink import MetricasQRLink

from qr_code_util import QRCodeUtil



def gerar_buffer_randomico(tamanho):

    buffer = bytearray()

    for _ in range(tamanho):
        buffer.append(random.randint(0, 255))

    return bytes(buffer)



class TelaQRLink:

    

    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura
        

        self.payload = 512
        self.qrcode_version = 10 
        self.box_size = 10       

        self.metricas = MetricasQRLink()
        self.camera = Camera()
        self.qr_code_util = QRCodeUtil()

         # Main loop
        self.running = True
        
        self.imagem_qrcode = self.qr_code_util.criar_qrcode(gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)


        self.tempo_anterior = time.time()

        self.taxa_transferencia = 0

        self.iniciar_pygame()

        self.fonte = pygame.font.Font(None, 36)






    def iniciar_pygame(self):

        # Initialize pygame
        pygame.init()

        # Create a window
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)
        pygame.display.set_caption("QR Code and Camera")




    def gerar_qrcode(self):

        self.tempo_atual = time.time()

        self.imagem_qrcode = self.qr_code_util.criar_qrcode(gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)




    def verificar_input_usuario_e_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.running = False


            elif evento.type == pygame.VIDEORESIZE:                

                # Se o usuário redimensionar a janela, você pode tratar o evento aqui
                (self.largura, self.altura) = evento.size


            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_UP:
                    
                    # Aumenta box_size
                    self.qrcode_version += 5

                    self.gerar_qrcode()
                    

                elif evento.key == pygame.K_DOWN:

                    # Diminui qrcode_version (com verificação para garantir que não seja menor que 1)
                    self.qrcode_version = max(self.qrcode_version - 5, 1)

                    self.gerar_qrcode()

                    
                elif evento.key == pygame.K_RIGHT:

                    # Aumenta payload em incrementos de 128
                    self.payload += 128

                    self.gerar_qrcode()

                    
                elif evento.key == pygame.K_LEFT:
                    
                    # Diminui payload em incrementos de 128 (com verificação para garantir que não seja menor que 128)
                    self.payload = max(self.payload - 128, 128)

                    self.gerar_qrcode()


                




    def processar_imagem_camera(self):

        # Capture a frame from the camera
        frame_camera = self.camera.capturar_frame()

        if frame_camera is not None:
            
            # Tente ler um QR Code da imagem da câmera
            qr_code_data = self.qr_code_util.ler_qrcode(cv2.cvtColor(frame_camera, cv2.COLOR_RGBA2BGR))

            if qr_code_data:
                            
                tamanho = len(qr_code_data)  

                # Calcula a taxa de transferência em Mbps
                self.tempo_atual = time.time()
                diferenca_tempo = self.tempo_atual - self.tempo_anterior
                self.taxa_transferencia = (tamanho * 8) / (diferenca_tempo * 1000000)  # Mbps                                  
                self.tempo_anterior = self.tempo_atual

                self.metricas.adicionar_leitura(self.tempo_atual, tamanho, self.qrcode_version)

                self.gerar_qrcode()


            frame_pygame = pygame.surfarray.make_surface(frame_camera)

            return frame_pygame
            



    def rodar(self):

        while self.running:
            
            self.renderizar()

        # Release the camera and quit pygame
        self.camera.release()
        pygame.quit()
    

    

    def renderizar(self):
            
        self.verificar_input_usuario_e_eventos()
                    

        # Fill the screen with white color
        self.tela.fill((0, 0, 0))


        texto = \
            f"Version( {self.qrcode_version} ) - " + \
            f"Payload( {self.payload} ) - " + \
            f"Box size( {self.box_size} ) -" + \
            f"Taxa( {self.metricas.taxa_transmissao()} Mbps )"

        texto_pygame = self.fonte.render(texto, True, (255, 255, 255))
        (largura_texto, altura_texto) = texto_pygame.get_size()
        self.tela.blit(texto_pygame, (self.largura/2-largura_texto/2 ,0))
        
        


        imagem_camera = self.processar_imagem_camera()


        #QRCode ocupa metade da largura da tela
        largura_qrcode = self.largura / 2

        #Redimensiona a imagem do QRCode
        imagem_qrcode_redimensionada = self.redimensionar(self.imagem_qrcode, largura_qrcode)    

        #Posiciona o QRCode no canto superior direito
        x_qrcode = self.largura - imagem_qrcode_redimensionada.get_width()

        #Logo abaixo da mensagem de texto
        y_qrcode = altura_texto

        #Desenha o QRCode na tela
        self.tela.blit(imagem_qrcode_redimensionada, (x_qrcode, y_qrcode))




        # 1/3 da metade da largura da tela
        largura_camera = (self.largura / 2) // 3        

        # Crie uma nova superfície com o novo tamanho
        imagem_camera_redimensionada = self.redimensionar(imagem_camera, largura_camera)

        print (f'origial ({imagem_camera.get_width()}) --- largura_camera: {largura_camera}  --- largura redimensionada: {imagem_camera_redimensionada.get_width()}')

        # Desenha a imagem da câmera na tela encostada no QRCode
        self.tela.blit(imagem_camera_redimensionada, (x_qrcode - imagem_camera_redimensionada.get_width(), altura_texto))



        #Posicionar os gráficos verticalmente
        y = altura_texto
        
        # 2/3 da metade da largura da tela
        largura_grafico = ((self.largura/2)/3)*2

        imagem_grafico_dados = self.metricas.imagem_grafico_dados()

        imagem_grafico_dados_redimensionada = self.redimensionar(imagem_grafico_dados, largura_grafico)

        self.tela.blit(imagem_grafico_dados_redimensionada, (0, y))
    
        y = y + imagem_grafico_dados_redimensionada.get_height() + 10


        imagem_grafico_taxa_transmissao = self.metricas.imagem_grafico_taxa_transmissao()

        imagem_grafico_taxa_transmissao_redimensionada = self.redimensionar(imagem_grafico_taxa_transmissao, largura_grafico)

        self.tela.blit(imagem_grafico_taxa_transmissao_redimensionada, (0, y))

        y = y + imagem_grafico_taxa_transmissao_redimensionada.get_height() + 10





        # Update the screen
        pygame.display.flip()


    

    def redimensionar(self, imagem, largura, altura=None, manter_proporcao=True):

        if manter_proporcao:

            altura = int(imagem.get_height() * largura / imagem.get_width())

            if altura > self.altura:

                altura = self.altura

                largura = int(imagem.get_width() * altura / imagem.get_height())


        # Redimensione a superfície original para a nova superfície
        imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))

        return imagem_redimensionada







# Set window dimensions
largura, altura = 2000, 1000 # Largura dobrada para acomodar ambas as imagens lado a lado

tela = TelaQRLink(largura, altura)

tela.rodar()







