# Teste de Hipótese: Python

A primeira implementação em Python consiste em uma aplicação que exibe um QR Code na tela e procura por um QR Code na imagem da câmera. 

Quando um QR Code é lido, troca-se o QR Code. O usuário pode escolher o tamanho do pacote do QR Code em número de bytes. A aplicação exibe métricas de quantos QR Codes estão sendo lido por segundos e a taxa de transmissão em Megabytes e Gigabytes.


## Para rodar com Anaconda:


sudo apt-get install libzbar

conda env create -f qrlink

conda activate qrlink

pip install -r requirements.txt

python qrlink.py
