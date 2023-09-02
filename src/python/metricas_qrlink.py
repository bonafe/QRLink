

# Importa as bibliotecas necessárias
# Explica o que cada biblioteca faz:

# matplotlib.pyplot: biblioteca para plotar gráficos
import matplotlib.pyplot as plt

import matplotlib.animation as animation

# matplotlib.backends.backend_agg.FigureCanvasAgg: biblioteca para renderizar gráficos
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# pandas: biblioteca para manipulação de dados
import pandas as pd

# numpy: biblioteca para manipulação de matrizes
import numpy as np

# pygame: biblioteca para criar interfaces gráficas
import pygame



# Classe para armazenar e plotar as métricas do QRLink
class MetricasQRLink:
  

  # Construtor da classe: inicializa as variáveis e cria os gráficos
  def __init__(self) -> None:
     
    
    self.dados = {'Tempo': [], 'Payload': [], 'QRCode Mode': []}
    

    plt.rcParams['axes.grid'] = True


    self.fig_dados, self.ax_dados = plt.subplots(figsize=(8, 4))
    self.canvas_dados = FigureCanvas(self.fig_dados)
    self.ax_dados.set_title('Tempo vs. Payload')
    self.ax_dados.set_xlabel('Tempo')
    self.ax_dados.set_ylabel('Payload')

    # Plota o gráfico        
    self.grafico_linha_dados = self.ax_dados.plot(self.dados['Tempo'], self.dados['Payload'], marker='o', linestyle='-')[0]

    self.fig_media_velocidade, self.ax_media_velocidade = plt.subplots(figsize=(8, 4))
    self.canvas_media_velocidade = FigureCanvas(self.fig_media_velocidade)
    self.ax_media_velocidade.set_title('Tempo vs. Mbps')
    self.ax_media_velocidade.set_xlabel('Tempo')
    self.ax_media_velocidade.set_ylabel('Mbps')    




  def adicionar_leitura(self, tempo, payload, qrcode_version):
    
    print (f'Adicionando leitura: {tempo} --- Payload: {payload} --- QRCode Mode: {qrcode_version}')

    self.dados['Tempo'].append(tempo)
    self.dados['Payload'].append(payload)
    self.dados['QRCode Mode'].append(qrcode_version)





  def imagem_grafico_dados(self):

    self.grafico_linha_dados.set_xdata(self.dados['Tempo'])
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
    



  def imagem_grafico_medias(self):

    return self.imagem_grafico_dados()    

    self.dados_mbps = self.gerar_dataframe_medias()

    # Plota o gráfico
    self.ax_media_velocidade.plot(self.dados_mbps['Tempo'], self.dados_mbps['Média Mbps'], marker='o', linestyle='-')

    # Atualiza o gráfico no pygame
    self.canvas_media_velocidade.draw()
    renderer = self.canvas_media_velocidade.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = self.canvas_media_velocidade.get_width_height()
    imagem_grafico_pygame = pygame.image.fromstring(raw_data, size, "RGB")

    return imagem_grafico_pygame




  def existem_dados(self):
    return len(self.dados['Tempo']) > 0




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
  