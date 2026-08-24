from pathlib import Path

import pygame


class Jogador:
    def __init__(self, tamanho_tela, area_pista):
        self.largura_tela, self.altura_tela = tamanho_tela
        self.area_pista = area_pista
        self.velocidade = 360
        self.largura = 54
        self.altura = 72

        caminho_imagem = Path(__file__).resolve().parents[1] / "assets" / "carro.png"
        imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.imagem = pygame.transform.scale(imagem, (self.largura, self.altura))
        self.retangulo = self.imagem.get_rect(midbottom=(self.largura_tela // 2, self.altura_tela - 34))
        self.posicao_x = float(self.retangulo.centerx)

    def atualizar(self, tempo_delta):
        teclas = pygame.key.get_pressed()
        movimento = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            movimento -= 1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            movimento += 1

        self.posicao_x += movimento * self.velocidade * tempo_delta

        metade_largura = self.retangulo.width / 2
        limite_esquerda = self.area_pista.left + 8 + metade_largura
        limite_direita = self.area_pista.right - 8 - metade_largura
        self.posicao_x = max(limite_esquerda, min(limite_direita, self.posicao_x))
        self.retangulo.centerx = round(self.posicao_x)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.retangulo)

    def pegar_caixa_colisao(self):
        return self.retangulo.inflate(-24, -12)
