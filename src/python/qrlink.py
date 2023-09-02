
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
        self.posicionar_elementos()

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




    def posicionar_elementos(self):

        # Defina a posição da imagem da câmera e do QR Code
        self.posicao_camera = (0, 0)  # Superior esquerdo
        self.posicao_qrcode = ((self.largura // 2)+10, 50)  # Superior direito
        self.posicao_grafico_dados = (0, self.altura // 2)  # Centro inferior
        self.posicao_grafico_dados_velocidade = ((self.largura // 2)+10, self.altura // 2)  # Centro inferior
        self.posicao_texto = ((self.largura // 2)+10, 10)



    def iniciar_pygame(self):

        # Initialize pygame
        pygame.init()

        # Create a window
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("QR Code and Camera")


    def gerar_qrcode(self):

        self.tempo_atual = time.time()

        self.imagem_qrcode = self.qr_code_util.criar_qrcode(gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)


    def verificar_input_usuario_e_eventos(self):

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                self.running = False

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


                elif evento.key == pygame.K_SPACE:

                    print (self.metricas.dados_mbps)




    def processar_imagem_camera(self):

        # Capture a frame from the camera
        frame_camera = self.camera.capturar_frame()

        if frame_camera is not None:

            frame_pygame = pygame.surfarray.make_surface(frame_camera)
            self.tela.blit(frame_pygame, self.posicao_camera)

            # Tente ler um QR Code da imagem da câmera
            qr_code_data = self.qr_code_util.ler_qrcode(cv2.cvtColor(frame_camera, cv2.COLOR_RGBA2BGR))

            if qr_code_data:
                            
                tamanho = len(qr_code_data)  

                # Calcula a taxa de transferência em Mbps
                self.tempo_atual = time.time()
                diferenca_tempo = self.tempo_atual - self.tempo_anterior
                taxa_transferencia = (tamanho * 8) / (diferenca_tempo * 1000000)  # Mbps                                  
                self.tempo_anterior = self.tempo_atual

                self.metricas.adicionar_leitura(self.tempo_atual, tamanho, self.qrcode_version)

                #Gera um novo QRCode
                self.imagem_qrcode = self.qr_code_util.criar_qrcode(gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)
                



    def rodar(self):

        while self.running:

            
            self.verificar_input_usuario_e_eventos()
                        

            # Fill the screen with white color
            self.tela.fill((0, 0, 0))


            texto = \
                f"Version( {self.qrcode_version} ) - " + \
                f"Payload( {self.payload} ) - " + \
                f"Box size( {self.box_size} ) -" + \
                f"Taxa( {self.taxa_transferencia:.2f} Mbps )"

            texto_pygame = self.fonte.render(texto, True, (255, 255, 255))
            self.tela.blit(texto_pygame, self.posicao_texto)  # Posição inferior esquerda
            

            if self.metricas.existem_dados():
                
                self.tela.blit(self.metricas.imagem_grafico_dados(), self.posicao_grafico_dados)
            
                self.tela.blit(self.metricas.imagem_grafico_medias(), self.posicao_grafico_dados_velocidade)
            

            self.tela.blit(self.imagem_qrcode, self.posicao_qrcode)


            self.processar_imagem_camera()

            # Update the screen
            pygame.display.flip()


        # Release the camera and quit pygame
        self.camera.release()
        pygame.quit()

       








# Set window dimensions
largura, altura = 2000, 1000 # Largura dobrada para acomodar ambas as imagens lado a lado

tela = TelaQRLink(largura, altura)

tela.rodar()







