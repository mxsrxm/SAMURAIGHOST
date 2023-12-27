# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023

# Descripcion: Este es el archivo principal del juego, aqui se ejecuta el juego

from nivel import Nivel

from interfaz import *
from configuraciones_generales import *

class Juego:

    def __init__(self):
        self.reloj = None
        self.juego_en_pausa = None
        self.pausa = False

        pygame.init()
        self.pantalla = pygame.display.set_mode((LARGO, ANCHO))
        pygame.display.set_caption('SamuraiGhost vs Goblins')
        self.tiempo = pygame.time.Clock()
        self.silenciado = False
        self.sonido= pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Menu9.wav'))


        self.nivel = Nivel()

        self.reloj = pygame.time.Clock()
        #self.pantalla_pausa = PantallaPausa()
        self.pantalla_pausa = Menu()

    def mostrar_pantalla_inicio(self):
        pantalla_inicio = PantallaInicio()
        pantalla_inicio.mostrar_pantalla()

        # Cargar y reproducir la música del juego
        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, 'musica', 'DarkCastle.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def pausar_juego(self):
        pygame.mixer.music.pause()
        self.pantalla_pausa.mostrar_pantalla_pausa()
        self.pausa = True

    def reanudar_juego(self):
        pygame.mixer.music.unpause()
        self.pausa = False

        while not self.juego_en_pausa:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if evento.key == pygame.K_p:
                        self.sonido.play()
                        self.juego_en_pausa = True
                        self.pausar_juego()

                        self.reiniciar_juego()

            self.nivel.run()
            pygame.display.update()
            self.tiempo.tick(FPS)

    def reiniciar_juego(self):
        self.nivel = Nivel()
        self.pausa = False
        self.juego_en_pausa = False
        self.reanudar_juego()

    def ejecutar(self):

        self.mostrar_pantalla_inicio()

        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, 'musica', 'DarkCastle.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if evento.key == pygame.K_p:
                        self.sonido.play()
                        if self.pausa:
                            self.reanudar_juego()
                        else:
                            self.pausar_juego()

                    if evento.key == pygame.K_m:
                        self.silenciado = not self.silenciado
                        if self.silenciado:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            if not self.pausa:
                self.nivel.run()

            pygame.display.update()
            self.tiempo.tick(FPS)

if __name__ == '__main__':
    game = Juego()
    game.ejecutar()