import qrcode
import pygame
import random


def gerar_buffer_randomico(tamanho):

    buffer = bytearray()

    for _ in range(tamanho):
        buffer.append(random.randint(0, 255))

    return bytes(buffer)



# Calcula a versão com base no tamanho do conteúdo
def calcular_versao(conteudo):
    for versao in range(1, 41):  # Verifica todas as versões possíveis (1 a 40)
        qr = qrcode.QRCode(
            version=versao,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(conteudo)
        qr.make(fit=True)
        bytes = qr.make_image().tobytes()
        print (len(bytes))
        if len(bytes) <= 2953:  # Tamanho máximo para uma versão 40
            return versao
    return 1  # Retorne a versão mínima se o conteúdo for muito grande

calcular_versao(gerar_buffer_randomico(2000))