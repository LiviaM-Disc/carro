import pygame


class Texto:
    def __init__(self, mensagem, tamanho, cor, centro):
        self.mensagem = mensagem
        self.fonte = pygame.font.Font(None, tamanho)
        self.cor = cor
        self.centro = centro

    def desenhar(self, tela):
        imagem = self.fonte.render(self.mensagem, True, self.cor)
        retangulo = imagem.get_rect(center=self.centro)
        tela.blit(imagem, retangulo)


class Botao:
    def __init__(self, retangulo, mensagem, cor, cor_hover, cor_texto):
        self.retangulo = pygame.Rect(retangulo)
        self.mensagem = mensagem
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.fonte = pygame.font.Font(None, 42)

    def clicou(self, eventos):
        mouse_pos = pygame.mouse.get_pos()
        mouse_em_cima = self.retangulo.collidepoint(mouse_pos)

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and mouse_em_cima:
                return True

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return True

        return False

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_hover if self.retangulo.collidepoint(mouse_pos) else self.cor

        pygame.draw.rect(tela, cor_atual, self.retangulo, border_radius=8)
        pygame.draw.rect(tela, (255, 255, 255), self.retangulo, width=2, border_radius=8)

        imagem_texto = self.fonte.render(self.mensagem, True, self.cor_texto)
        retangulo_texto = imagem_texto.get_rect(center=self.retangulo.center)
        tela.blit(imagem_texto, retangulo_texto)
