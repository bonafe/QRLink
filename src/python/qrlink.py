

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

from camera import CameraQRCode

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
        self.camera = CameraQRCode()


        self.gerar_qrcode()

        self.tempo_anterior = time.time()

        self.taxa = 0

        
        largura, altura = 2000, 1000 # Largura dobrada para acomodar ambas as imagens lado a lado

        self.tela = TelaQRLink(self, largura, altura)

        self.tela.rodar(self.atualizar_elementos_tela)



    def qrcode_recebido(self, dados):

        tamanho = len(dados)  

        # Calcula a taxa de transferência em Mbps
        tempo_atual = time.time()

        diferenca_tempo = tempo_atual - self.tempo_anterior

        self.tempo_anterior = tempo_atual

        self.metricas.adicionar_leitura(tempo_atual, tamanho, self.qrcode_version)
                

        self.gerar_qrcode()





    def atualizar_elementos_tela(self):

        self.imagem_camera = self.camera.processar_imagem_camera(self.qrcode_recebido)

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
            f"Payload( {self.payload} bytes ) - " + \
            f"Box size( {self.box_size} ) -" + \
            f"Taxa( {round(self.taxa, 4)} Mbps ) -" + \
            f"QRCode/segundo( {self.qrcode_segundo} )"



    def gerar_qrcode(self):

        self.tempo_atual = time.time()

        self.imagem_qrcode = QRCodeUtil.criar_qrcode(self.gerar_buffer_randomico(self.payload), self.qrcode_version, self.box_size)


    

       




    def gerar_buffer_randomico(self, tamanho):

        buffer = bytearray()

        for _ in range(tamanho):
            buffer.append(random.randint(0, 255))

        return bytes(buffer)




if __name__ == "__main__":

    QRLink()


