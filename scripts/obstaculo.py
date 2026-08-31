from pathlib import Path
from random import randint

import pygame


CAMINHO_ASSETS = Path(__file__).resolve().parents[1] / "assets"


class Obstaculo:
    imagem_base = None

    def __init__(self, area_pista, velocidade):
        self.area_pista = area_pista
        self.velocidade = velocidade
        self.largura = 44
        self.altura = 50

        if Obstaculo.imagem_base is None:
            caminho_imagem = CAMINHO_ASSETS / "cone.png"
            if not caminho_imagem.exists():
                raise FileNotFoundError(f"Imagem do obstaculo nao encontrada: {caminho_imagem}")

            imagem = pygame.image.load(caminho_imagem).convert_alpha()
            Obstaculo.imagem_base = pygame.transform.scale(imagem, (self.largura, self.altura))

        self.imagem = Obstaculo.imagem_base
        x_minimo = self.area_pista.left + 16
        x_maximo = self.area_pista.right - self.largura - 16
        if x_minimo > x_maximo:
            raise ValueError("A area da pista e estreita demais para criar obstaculos.")

        self.retangulo = self.imagem.get_rect(topleft=(randint(x_minimo, x_maximo), -self.altura))
        self.posicao_y = float(self.retangulo.y)

    def atualizar(self, tempo_delta):
        self.posicao_y += self.velocidade * tempo_delta
        self.retangulo.y = round(self.posicao_y)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.retangulo)

    def saiu_da_tela(self, altura_tela):
        return self.retangulo.top > altura_tela

    def colidiu_com(self, jogador):
        return self.retangulo.inflate(-18, -14).colliderect(jogador.pegar_caixa_colisao())
