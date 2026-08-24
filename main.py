import pygame

from scripts.cenas import Menu, Partida


LARGURA_TELA = 480
ALTURA_TELA = 720
FPS = 60


def main():
    pygame.init()
    pygame.display.set_caption("Carro Turbo")

    tamanho_tela = (LARGURA_TELA, ALTURA_TELA)
    tela = pygame.display.set_mode(tamanho_tela)
    relogio = pygame.time.Clock()

    cenas = {
        "menu": Menu(tamanho_tela),
        "partida": Partida(tamanho_tela),
    }

    cena_atual = "menu"
    rodando = True

    while rodando:
        tempo_delta = relogio.tick(FPS) / 1000
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False

        proxima_cena = cenas[cena_atual].atualizar(eventos, tempo_delta)

        if proxima_cena != cena_atual:
            cena_atual = proxima_cena

            if cena_atual == "partida":
                cenas["partida"].reiniciar()

        cenas[cena_atual].desenhar(tela)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
