



import pygame




class TelaQRLink:

    

    def __init__(self, qrlink, largura, altura):

        self.qrlink = qrlink

        self.largura = largura

        self.altura = altura
    

         # Main loop
        self.running = True
        
        
        self.iniciar_pygame()

        self.fonte = pygame.font.Font(None, 36)






    def iniciar_pygame(self):

        # Initialize pygame
        pygame.init()

        # Create a window
        self.tela = pygame.display.set_mode((self.largura, self.altura), pygame.RESIZABLE)

        pygame.display.set_caption("QR Code and Camera")




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
                    self.qrlink.qrcode_version += 5

                    self.qrlink.gerar_qrcode()
                    

                elif evento.key == pygame.K_DOWN:

                    # Diminui qrcode_version (com verificação para garantir que não seja menor que 1)
                    self.qrlink.qrcode_version = max(self.qrlink.qrcode_version - 5, 1)

                    self.qrlink.gerar_qrcode()

                    
                elif evento.key == pygame.K_RIGHT:

                    # Aumenta payload em incrementos de 128
                    self.qrlink.payload += 128

                    self.qrlink.gerar_qrcode()

                    
                elif evento.key == pygame.K_LEFT:
                    
                    # Diminui payload em incrementos de 128 (com verificação para garantir que não seja menor que 128)
                    self.qrlink.payload = max(self.qrlink.payload - 128, 128)

                    self.qrlink.gerar_qrcode()


                

    def atualizar(self, imagem_camera, imagem_qrcode, imagem_grafico_dados, imagem_grafico_taxa_transmissao, texto_cabecalho):
            
        self.imagem_camera = imagem_camera

        self.imagem_qrcode = imagem_qrcode

        self.imagem_grafico_dados = imagem_grafico_dados

        self.imagem_grafico_taxa_transmissao = imagem_grafico_taxa_transmissao

        self.texto_cabecalho = texto_cabecalho
                

    

    def rodar(self, callback):

        while self.running:
            
            self.renderizar(callback)

        # Release the camera and quit pygame
        self.qrlink.camera.release()
        pygame.quit()
    

    

    def renderizar(self, callback):
            
        self.verificar_input_usuario_e_eventos()
                    
        if callback:
            callback()                    

        # Fill the screen with white color
        self.tela.fill((0, 0, 0))



        texto_pygame = self.fonte.render(self.texto_cabecalho, True, (255, 255, 255))
        (largura_texto, altura_texto) = texto_pygame.get_size()
        self.tela.blit(texto_pygame, (self.largura/2-largura_texto/2 ,0))



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
        imagem_camera_redimensionada = self.redimensionar(self.imagem_camera, largura_camera)

        # Desenha a imagem da câmera na tela encostada no QRCode
        self.tela.blit(imagem_camera_redimensionada, (x_qrcode - imagem_camera_redimensionada.get_width(), altura_texto))



        #Posicionar os gráficos verticalmente
        y = altura_texto
        
        # 2/3 da metade da largura da tela
        largura_grafico = ((self.largura/2)/3)*2
        

        imagem_grafico_dados_redimensionada = self.redimensionar(self.imagem_grafico_dados, largura_grafico)

        self.tela.blit(imagem_grafico_dados_redimensionada, (0, y))
    
        y = y + imagem_grafico_dados_redimensionada.get_height() + 10
        

        imagem_grafico_taxa_transmissao_redimensionada = self.redimensionar(self.imagem_grafico_taxa_transmissao, largura_grafico)

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


