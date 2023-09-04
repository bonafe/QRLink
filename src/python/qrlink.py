

import pygame

import numpy as np

from qrcode import QRCode

import cv2


from io import BytesIO
import tempfile


import random
import time
import datetime



from tela import TelaQRLink

from camera import Camera

from metricas_qrlink import MetricasQRLink

from qr_code_util import QRCodeUtil




class QRLink:



    def __init__(self):    

        # Informações sobre o QRCode utilizado no momento
        self.payload = 512
        
        self.qrcode_version = 10 
        
        self.box_size = 10   


        # Métricas de desempenho
        self.metricas = MetricasQRLink()

        # Câmera
        self.camera = Camera()

        # Gerador e Leitor de QRCode
        self.qr_code_util = QRCodeUtil()


        self.imagem_qrcode = self.qr_code_util.criar_qrcode(self.gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)

        self.tempo_anterior = time.time()

        self.taxa_transferencia = 0

        
        largura, altura = 2000, 1000 # Largura dobrada para acomodar ambas as imagens lado a lado

        self.tela = TelaQRLink(self, largura, altura)

        self.tela.rodar(self.atualizar_elementos_tela)




    def atualizar_elementos_tela(self):

        self.imagem_camera = self.processar_imagem_camera()

        self.imagem_grafico_dados = self.metricas.imagem_grafico_dados()

        self.imagem_grafico_taxa_transmissao = self.metricas.imagem_grafico_taxa_transmissao()        

        (self.taxa, self.qrcode_segundo) = self.metricas.taxa_transmissao()

        self.atualizar_texto()

        self.tela.atualizar(
            imagem_camera=self.imagem_camera,
            imagem_qrcode=self.imagem_qrcode,
            imagem_grafico_dados=self.imagem_grafico_dados,
            imagem_grafico_taxa_transmissao=self.imagem_grafico_taxa_transmissao,
            texto_cabecalho=self.texto_cabecalho
        )



    def atualizar_texto(self):

        self.texto_cabecalho = \
            f"Version( {self.qrcode_version} ) - " + \
            f"Payload( {self.payload} ) - " + \
            f"Box size( {self.box_size} ) -" + \
            f"Taxa( {self.taxa} Mbps ) -" + \
            f"QRCode/segundo( {self.qrcode_segundo} )"



    def gerar_qrcode(self):

        self.tempo_atual = time.time()

        self.imagem_qrcode = self.qr_code_util.criar_qrcode(self.gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)


    

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




    def gerar_buffer_randomico(self, tamanho):

        buffer = bytearray()

        for _ in range(tamanho):
            buffer.append(random.randint(0, 255))

        return bytes(buffer)




if __name__ == "__main__":

    QRLink()


