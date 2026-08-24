import pygame

from scripts.interfaces import Botao, Texto
from scripts.jogador import Jogador
from scripts.obstaculo import Obstaculo


class Menu:
    def __init__(self, tamanho_tela):
        self.largura_tela, self.altura_tela = tamanho_tela
        self.titulo = Texto("Carro Turbo", 82, (255, 255, 255), (self.largura_tela // 2, 210))
        self.subtitulo = Texto("Desvie dos cones", 38, (255, 196, 67), (self.largura_tela // 2, 270))
        self.botao_jogar = Botao(
            (self.largura_tela // 2 - 110, 340, 220, 64),
            "Jogar",
            (255, 154, 53),
            (255, 190, 68),
            (29, 22, 15),
        )
        self.estado = "menu"

    def atualizar(self, eventos, tempo_delta):
        self.estado = "menu"

        if self.botao_jogar.clicou(eventos):
            self.estado = "partida"

        return self.estado

    def desenhar(self, tela):
        tela.fill((28, 112, 88))
        self._desenhar_pista_de_fundo(tela)
        self.titulo.desenhar(tela)
        self.subtitulo.desenhar(tela)
        self.botao_jogar.desenhar(tela)

    def _desenhar_pista_de_fundo(self, tela):
        pista = pygame.Rect(self.largura_tela // 2 - 90, 0, 180, self.altura_tela)
        pygame.draw.rect(tela, (45, 51, 64), pista)
        pygame.draw.rect(tela, (232, 238, 247), (pista.left - 5, 0, 5, self.altura_tela))
        pygame.draw.rect(tela, (232, 238, 247), (pista.right, 0, 5, self.altura_tela))

        for y in range(-20, self.altura_tela, 88):
            pygame.draw.rect(tela, (255, 255, 255), (self.largura_tela // 2 - 3, y, 6, 42))


class Partida:
    def __init__(self, tamanho_tela):
        self.largura_tela, self.altura_tela = tamanho_tela
        self.area_pista = pygame.Rect(76, 0, self.largura_tela - 152, self.altura_tela)
        self.fonte_pontos = pygame.font.Font(None, 42)
        self.reiniciar()

    def reiniciar(self):
        self.jogador = Jogador((self.largura_tela, self.altura_tela), self.area_pista)
        self.obstaculos = []
        self.pontos = 0
        self.contador_pontos = 0
        self.contador_obstaculo = 0
        self.intervalo_obstaculo = 0.9
        self.velocidade_obstaculo = 260
        self.deslocamento_pista = 0
        self.estado = "partida"

    def atualizar(self, eventos, tempo_delta):
        self.estado = "partida"
        self.jogador.atualizar(tempo_delta)
        self._atualizar_pontos(tempo_delta)
        self._atualizar_obstaculos(tempo_delta)
        self._aumentar_dificuldade()
        self.deslocamento_pista = (self.deslocamento_pista + self.velocidade_obstaculo * tempo_delta) % 84

        if self._jogador_colidiu():
            self.estado = "menu"

        return self.estado

    def desenhar(self, tela):
        tela.fill((37, 115, 91))
        self._desenhar_pista(tela)

        for obstaculo in self.obstaculos:
            obstaculo.desenhar(tela)

        self.jogador.desenhar(tela)
        self._desenhar_pontos(tela)

    def _atualizar_pontos(self, tempo_delta):
        self.contador_pontos += tempo_delta

        if self.contador_pontos >= 1:
            self.pontos += 1
            self.contador_pontos = 0

    def _atualizar_obstaculos(self, tempo_delta):
        self.contador_obstaculo += tempo_delta

        if self.contador_obstaculo >= self.intervalo_obstaculo:
            self.obstaculos.append(Obstaculo(self.area_pista, self.velocidade_obstaculo))
            self.contador_obstaculo = 0

        for obstaculo in self.obstaculos:
            obstaculo.velocidade = self.velocidade_obstaculo
            obstaculo.atualizar(tempo_delta)

        self.obstaculos = [
            obstaculo for obstaculo in self.obstaculos if not obstaculo.saiu_da_tela(self.altura_tela)
        ]

    def _aumentar_dificuldade(self):
        self.velocidade_obstaculo = 260 + self.pontos * 9
        self.intervalo_obstaculo = max(0.42, 0.9 - self.pontos * 0.01)

    def _jogador_colidiu(self):
        return any(obstaculo.colidiu_com(self.jogador) for obstaculo in self.obstaculos)

    def _desenhar_pista(self, tela):
        pygame.draw.rect(tela, (45, 51, 64), self.area_pista)
        pygame.draw.rect(tela, (232, 238, 247), (self.area_pista.left - 5, 0, 5, self.altura_tela))
        pygame.draw.rect(tela, (232, 238, 247), (self.area_pista.right, 0, 5, self.altura_tela))

        largura_faixa = self.area_pista.width // 3

        for linha in (self.area_pista.left + largura_faixa, self.area_pista.left + largura_faixa * 2):
            for y in range(int(-84 + self.deslocamento_pista), self.altura_tela + 84, 84):
                pygame.draw.rect(tela, (245, 245, 245), (linha - 3, y, 6, 40))

    def _desenhar_pontos(self, tela):
        texto = self.fonte_pontos.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        fundo = texto.get_rect(topleft=(18, 16)).inflate(24, 12)
        pygame.draw.rect(tela, (16, 24, 35), fundo, border_radius=8)
        tela.blit(texto, (30, 22))
