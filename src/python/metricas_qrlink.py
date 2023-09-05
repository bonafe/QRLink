

# Importa as bibliotecas necessárias
# Explica o que cada biblioteca faz:

# matplotlib.pyplot: biblioteca para plotar gráficos
import matplotlib.pyplot as plt

import matplotlib.animation as animation

# matplotlib.backends.backend_agg.FigureCanvasAgg: biblioteca para renderizar gráficos
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# numpy: biblioteca para manipulação de matrizes
import numpy as np

# pygame: biblioteca para criar interfaces gráficas
import pygame

# datetime: biblioteca para manipulação de datas e horas
import matplotlib.dates as mdates

import datetime

# Classe para armazenar e plotar as métricas do QRLink
class MetricasQRLink:
  

  # Construtor da classe: inicializa as variáveis e cria os gráficos
  def __init__(self) -> None:
     
    
    self.dados = {'Tempo': [], 'Tempo Data Hora': [], 'Payload': [], 'QRCode Mode': []}
    

    plt.rcParams['axes.grid'] = True
    plt.xticks(rotation=70)

    self.fig_dados, self.ax_dados = plt.subplots(figsize=(8, 4))
    self.canvas_dados = FigureCanvas(self.fig_dados)
    self.ax_dados.set_title('Tempo vs. Payload')
    self.ax_dados.set_xlabel('Tempo')
    self.ax_dados.set_ylabel('Payload')
    
    self.ax_dados.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S.%f'))    

    # Plota o gráfico        
    self.grafico_linha_dados = self.ax_dados.plot(self.dados['Tempo'], self.dados['Payload'], marker='o', linestyle='-')[0]



    self.fig_media_velocidade, self.ax_media_velocidade = plt.subplots(figsize=(8, 4))
    self.canvas_media_velocidade = FigureCanvas(self.fig_media_velocidade)
    self.ax_media_velocidade.set_title('Tempo vs. Mbps')
    self.ax_media_velocidade.set_xlabel('Tempo')
    self.ax_media_velocidade.set_ylabel('Mbps')  
    

    #self.ax_media_velocidade.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S.%f'))

    # Plota o gráfico        
    self.grafico_linha_media_velocidade = self.ax_media_velocidade.plot([], [], marker='o', linestyle='-')[0]




  def adicionar_leitura(self, tempo, payload, qrcode_version):
        
    self.dados['Tempo'].append(tempo)
    self.dados['Tempo Data Hora'].append(datetime.datetime.utcfromtimestamp(tempo)
)
    self.dados['Payload'].append(payload)
    self.dados['QRCode Mode'].append(qrcode_version)





  def imagem_grafico_dados(self):

    self.grafico_linha_dados.set_xdata(self.dados['Tempo Data Hora'])
    self.grafico_linha_dados.set_ydata(self.dados['Payload']) 

    self.grafico_linha_dados.axes.relim()
    self.grafico_linha_dados.axes.autoscale_view()    

    # Atualiza o gráfico no pygame
    self.canvas_dados.draw()
    renderer = self.canvas_dados.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = self.canvas_dados.get_width_height()
    imagem_grafico_pygame = pygame.image.fromstring(raw_data, size, "RGB")

    return imagem_grafico_pygame
    



  def imagem_grafico_taxa_transmissao(self):
    
    tempos_centrais, medias_mbps = self.gerar_lista_medias()  

    self.grafico_linha_media_velocidade.set_xdata(tempos_centrais)
    self.grafico_linha_media_velocidade.set_ydata(medias_mbps) 

    self.grafico_linha_media_velocidade.axes.relim()
    self.grafico_linha_media_velocidade.axes.autoscale_view()    

    # Atualiza o gráfico no pygame
    self.canvas_media_velocidade.draw()
    renderer = self.canvas_media_velocidade.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = self.canvas_media_velocidade.get_width_height()
    imagem_grafico_pygame = pygame.image.fromstring(raw_data, size, "RGB")

    return imagem_grafico_pygame




  def existem_dados(self):
    return len(self.dados['Tempo']) > 0



  def taxa_transmissao(self):
     
    if not self.existem_dados():
        return ([], []) 
    
    else:

      janela_tempo = 10 
      taxa_transmissao = 0
      qrcodes_segundo = 0

      inicio_janela = max(self.dados['Tempo']) - janela_tempo
      fim_janela = inicio_janela + janela_tempo
      
      dados_janela = [(tempo, payload) for tempo, payload in zip(self.dados['Tempo'], self.dados['Payload']) if inicio_janela <= tempo < fim_janela]

      if dados_janela:

        tempos, payloads = zip(*dados_janela)

        tamanho_total = (np.sum(payloads) * 8 ) / 1000000
        tempo_total = fim_janela - inicio_janela
        taxa_transmissao = tamanho_total / tempo_total    
        qrcodes_segundo = len(dados_janela) / tempo_total
      

      return (taxa_transmissao, qrcodes_segundo)


  def gerar_lista_medias(self):
        
        if not self.existem_dados():
            return ([], []) 
        
        else:

          janela_tempo = 1  # 1 segundo
          tempos_centrais = []
          medias_mbps = []

          inicio_janela = min(self.dados['Tempo'])
          fim_janela = inicio_janela + janela_tempo

          while fim_janela <= max(self.dados['Tempo']):
              dados_janela = [(tempo, payload) for tempo, payload in zip(self.dados['Tempo'], self.dados['Payload']) if inicio_janela <= tempo < fim_janela]
              if dados_janela:
                  tempos, payloads = zip(*dados_janela)

                  tamanho_total = (np.sum(payloads) * 8) / 1000000
                  tempo_total = fim_janela - inicio_janela
                  velocidade = tamanho_total / tempo_total
                  
                  tempo_central = (inicio_janela + fim_janela) / 2
                  tempos_centrais.append(tempo_central)
                  medias_mbps.append(velocidade)
              inicio_janela = fim_janela
              fim_janela += janela_tempo

          return (tempos_centrais, medias_mbps)