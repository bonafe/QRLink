
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







metricas = MetricasQRLink()

camera = Camera()

qr_code_util = QRCodeUtil()


payload = 512



# Initialize pygame
pygame.init()



# Set window dimensions
largura, altura = 2000, 1000 # Largura dobrada para acomodar ambas as imagens lado a lado

# Create a window
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("QR Code and Camera")



# Defina a posição da imagem da câmera e do QR Code
posicao_camera = (0, 0)  # Superior esquerdo
posicao_qrcode = ((largura // 2)+10, 50)  # Superior direito
posicao_grafico = (0, altura // 2)  # Centro inferior
posicao_grafico2 = ((largura // 2)+10, altura // 2)  # Centro inferior
posicao_texto = ((largura // 2)+10, 10)







qrcode_version = 10
payload = 512


# Main loop
running = True
desenhar_qrcode = True
imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version)


tempo_anterior = time.time()
taxa_transferencia = 0

fonte = pygame.font.Font(None, 36)


while running:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

        elif evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_UP:
                tempo_atual = time.time()
                
                # Aumenta box_size
                qrcode_version += 5

                imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version)
                
            elif evento.key == pygame.K_DOWN:
                tempo_atual = time.time()
                # Diminui qrcode_version (com verificação para garantir que não seja menor que 1)
                qrcode_version = max(qrcode_version - 5, 1)

                imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version)
                
            elif evento.key == pygame.K_RIGHT:
                tempo_atual = time.time()
                # Aumenta payload em incrementos de 128
                payload += 128

                imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version)
                
            elif evento.key == pygame.K_LEFT:
                tempo_atual = time.time()
                # Diminui payload em incrementos de 128 (com verificação para garantir que não seja menor que 128)
                payload = max(payload - 128, 128)

                imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version)

            elif evento.key == pygame.K_SPACE:
                print (metricas.dados_mbps)
                
      

    # Capture a frame from the camera
    frame_camera = camera.capturar_frame()

    # Fill the screen with white color
    tela.fill((255, 255, 255))



    # Exiba qrcode_version e tamanho do payload
    texto_qrcode_version = fonte.render(f"qrcode_version: {qrcode_version}", True, (0, 0, 0))
    tela.blit(texto_qrcode_version, (10, altura - 60))  # Posição inferior esquerda
    texto_payload = fonte.render(f"Tamanho do Payload: {payload} bytes", True, (0, 0, 0))
    tela.blit(texto_payload, (largura // 2 + 10, altura - 60))  # Posição inferior direita
    

    if metricas.existem_dados():
        
        tela.blit(metricas.imagem_grafico_dados(), posicao_grafico)
    
        tela.blit(metricas.imagem_grafico_medias(), posicao_grafico2)




    # Exiba a taxa de transferência na tela            
    texto_taxa = fonte.render(f"Taxa de Transferência: {taxa_transferencia:.2f} Mbps", True, (0, 0, 0))
    tela.blit(texto_taxa, posicao_texto)      



    # Draw the QR Code and camera frame side by side
    if desenhar_qrcode:
        tela.blit(imagem_qrcode, posicao_qrcode)

    if frame_camera is not None:

        frame_pygame = pygame.surfarray.make_surface(frame_camera)
        tela.blit(frame_pygame, posicao_camera)

        # Tente ler um QR Code da imagem da câmera
        qr_code_data = qr_code_util.ler_qrcode(cv2.cvtColor(frame_camera, cv2.COLOR_RGBA2BGR))

        if qr_code_data:
                        
            tamanho = len(qr_code_data)  

            # Calcula a taxa de transferência em Mbps
            tempo_atual = time.time()
            diferenca_tempo = tempo_atual - tempo_anterior
            taxa_transferencia = (tamanho * 8) / (diferenca_tempo * 1000000)  # Mbps                                  
            tempo_anterior = tempo_atual


            metricas.adicionar_leitura(tempo_atual, tamanho, qrcode_version)


            #Gera um novo QRCode
            imagem_qrcode = qr_code_util.criar_qrcode(gerar_buffer_randomico(payload), qrcode_version) 
            

    # Update the screen
    pygame.display.flip()

# Release the camera and quit pygame
camera.release()
pygame.quit()
