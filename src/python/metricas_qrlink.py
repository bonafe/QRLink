

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import numpy as np
import pygame

class MetricasQRLink:
  


  def __init__(self) -> None:
     
    self.lista = []
    self.dados = pd.DataFrame(columns=['Tempo', 'Payload', 'QRCode Mode'])

    
    plt.rcParams['axes.grid'] = True


    self.fig_dados, self.ax_dados = plt.subplots(figsize=(8, 4))
    self.canvas_dados = FigureCanvas(self.fig_dados)
    self.ax_dados.set_title('Tempo vs. Payload')
    self.ax_dados.set_xlabel('Tempo')
    self.ax_dados.set_ylabel('Payload')


    self.fig_media_velocidade, self.ax_media_velocidade = plt.subplots(figsize=(8, 4))
    self.canvas_media_velocidade = FigureCanvas(self.fig_media_velocidade)
    self.ax_media_velocidade.set_title('Tempo vs. Mbps')
    self.ax_media_velocidade.set_xlabel('Tempo')
    self.ax_media_velocidade.set_ylabel('Mbps')    




  def adicionar_leitura(self, tempo, payload, qrcode_version):
    
    #Adiciona nova leitura ao dataframe
    self.lista.append({'Tempo': tempo, 'Payload': payload, 'QRCode Mode': qrcode_version})




  def imagem_grafico_dados(self):

    # Plota o gráfico    
    self.dados = pd.DataFrame(self.lista)
    self.ax_dados.plot(self.dados['Tempo'], self.dados['Payload'], marker='o', linestyle='-')    
    
    # Atualiza o gráfico no pygame
    self.canvas_dados.draw()
    renderer = self.canvas_dados.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = self.canvas_dados.get_width_height()
    imagem_grafico_pygame = pygame.image.fromstring(raw_data, size, "RGB")

    return imagem_grafico_pygame
    



  def imagem_grafico_medias(self):

    dados_mbps = self.gerar_dataframe_medias()

    # Plota o gráfico
    self.ax_media_velocidade.plot(dados_mbps['Tempo'], dados_mbps['Média Mbps'], marker='o', linestyle='-')

    # Atualiza o gráfico no pygame
    self.canvas_media_velocidade.draw()
    renderer = self.canvas_media_velocidade.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = self.canvas_media_velocidade.get_width_height()
    imagem_grafico_pygame = pygame.image.fromstring(raw_data, size, "RGB")

    return imagem_grafico_pygame




  def existem_dados(self):
    return len(self.lista) > 0




  # Suponha que você já tenha o DataFrame 'dados' com as colunas 'Tempo', 'Payload' e 'QRCode Mode'
  def gerar_dataframe_medias(self):


        # Defina a janela de tempo desejada em segundos
      janela_tempo = 1  # 1 segundo

      # Inicialize listas para armazenar os tempos centrais e as médias do Mbps
      tempos_centrais = []
      medias_mbps = []
    

      # Itere sobre os dados para calcular as médias do Mbps em janelas de tempo
      inicio_janela = self.dados['Tempo'].min()
      fim_janela = inicio_janela + janela_tempo
          
      while fim_janela <= self.dados['Tempo'].max():
          
          # Filtre os dados dentro da janela de tempo
          dados_janela = self.dados[(self.dados['Tempo'] >= inicio_janela) & (self.dados['Tempo'] < fim_janela)]
          
          # Calcule a média do Mbps para esta janela de tempo
          media_mbps = np.mean((dados_janela['Payload'] * 8) / (dados_janela['Tempo'].diff() * 1000000))
          
          # Calcule o tempo central da janela
          tempo_central = (inicio_janela + fim_janela) / 2                    

          # Adicione os valores à lista
          tempos_centrais.append(tempo_central)
          medias_mbps.append(media_mbps)
          
          # Mova a janela para o próximo intervalo
          inicio_janela = fim_janela
          fim_janela += janela_tempo

      # Crie um novo DataFrame com os tempos centrais e as médias do Mbps
      novo_dataframe = pd.DataFrame({'Tempo': tempos_centrais, 'Média Mbps': medias_mbps})

      # Exiba o novo DataFrame
      return novo_dataframe
  