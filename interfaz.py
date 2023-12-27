import sys
from configuraciones_generales import *


class PantallaInicio:
    def __init__(self):
        self.silenciado = None
        self.pantalla = pygame.display.get_surface()
        self.reloj = pygame.time.Clock()
        self.sonido = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Menu9.wav'))
        self.sonido_salir = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Cancel.wav'))

    def mostrar_pantalla(self):
        fondo = pygame.image.load(os.path.join(RUTA_IMAGENES, 'mapa', 'fondo_inicio.png')).convert()
        self.pantalla.blit(fondo, (0, 0))
        pygame.display.flip()

        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, 'musica', '4 - Village.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        esperar = True
        while esperar:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        esperar = False
                        # Detener la música de inicio antes de salir
                        pygame.mixer.music.stop()
                        self.sonido.play()
                    if evento.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.sonido_salir.play()
                        pygame.time.wait(1000)

                        pygame.quit()
                        sys.exit()

                    if evento.key == pygame.K_m:
                        if self.silenciado:
                            pygame.mixer.music.unpause()
                            self.silenciado = False
                        else:
                            pygame.mixer.music.pause()
                            self.silenciado = True

            self.reloj.tick(1)


class Menu:

    def __init__(self):

        self.pantalla = pygame.display.get_surface()

        self.pantalla = pygame.display.get_surface()
        self.pantalla_rect = self.pantalla.get_rect()
        self.fondo = pygame.Surface((LARGO, ANCHO))
        self.fondo.fill((0, 0, 0))
        self.fondo.set_alpha(200)
        self.sonido = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Menu9.wav'))
        self.sonido_salir = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Cancel.wav'))

        self.silenciado = None

        # Cargar la imagen que deseas mostrar

        self.imagen_win = pygame.image.load(os.path.join(RUTA_IMAGENES, 'personajes', 'jugador.png'))
        self.imagen_win_rect = self.imagen_win.get_rect(center=(LARGO // 2, ANCHO // 4))

        self.imagen_dead = pygame.image.load(os.path.join(RUTA_IMAGENES, 'personajes', 'enemigos.png'))
        self.imagen_dead_rect = self.imagen_dead.get_rect(center=(LARGO // 2, ANCHO // 4))

        self.fuente = pygame.font.Font(os.path.join(FUENTE), 25)
        self.fuente_grande = pygame.font.Font(os.path.join(FUENTE), 50)

        self.texto_win = self.fuente_grande.render('Has ganado', True, (255, 255, 255))
        self.texto_win_rect = self.texto_win.get_rect(center=(LARGO // 2, ANCHO // 3))
        self.texto_dead = self.fuente_grande.render('Has muerto', True, (255, 255, 255))
        self.texto_dead_rect = self.texto_dead.get_rect(center=(LARGO // 2, ANCHO // 3))
        self.texto_pausa = self.fuente_grande.render('Juego pausado', True, (255, 255, 255))
        self.texto_pausa_rect = self.texto_pausa.get_rect(center=(LARGO // 2, ANCHO // 3))

        self.texto_reanudar = self.fuente.render('Presiona doble P para reanudar', True, (255, 255, 255))
        self.texto_reanudar_rect = self.texto_reanudar.get_rect(center=(LARGO // 2, ANCHO // 2 + 50))

        self.texto_inicio = self.fuente.render('Presiona I para volver al inicio', True, (255, 255, 255))
        self.texto_inicio_rect = self.texto_inicio.get_rect(center=(LARGO // 2, ANCHO // 2 + 120))

        self.texto_silenciar = self.fuente.render('Presiona M para silenciar', True, (255, 255, 255))
        self.texto_silenciar_rect = self.texto_silenciar.get_rect(center=(LARGO // 2, ANCHO // 2 + 170))

        self.texto_salir = self.fuente.render('Presiona ESC para salir', True, (255, 255, 255))
        self.texto_salir_rect = self.texto_salir.get_rect(center=(LARGO // 2, ANCHO // 2 + 220))

    def mostrar_pantalla_pausa(self):
        self.pantalla.blit(self.fondo, (0, 0))
        # Mostrar la imagen antes del texto
        self.pantalla.blit(self.texto_pausa, self.texto_pausa_rect)
        self.pantalla.blit(self.texto_reanudar, self.texto_reanudar_rect)
        self.pantalla.blit(self.texto_inicio, self.texto_inicio_rect)
        self.pantalla.blit(self.texto_salir, self.texto_salir_rect)
        self.pantalla.blit(self.texto_silenciar, self.texto_silenciar_rect)

        pygame.display.flip()

        pygame.display.flip()

        eleccion = None
        while not eleccion:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_i:
                        self.sonido.play()

                        # reprodicir sonido

                        # ejecutar el juego
                        from main import Juego
                        juego = Juego()
                        juego.ejecutar()

                    elif evento.key == pygame.K_m:

                        if self.silenciado:
                            pygame.mixer.music.unpause()
                            self.silenciado = False
                        else:
                            pygame.mixer.music.pause()
                            self.silenciado = True

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.sonido_salir.play()
                        pygame.time.wait(1000)
                        pygame.quit()
                        sys.exit()

                    elif evento.key == pygame.K_p:
                        self.sonido.play()
                        eleccion = 'continuar'

        return eleccion

    def mostrar_pantalla_win(self):
        self.pantalla.blit(self.fondo, (0, 0))

        self.pantalla.blit(self.imagen_win, self.imagen_win_rect)
        self.pantalla.blit(self.texto_win, self.texto_win_rect)
        self.pantalla.blit(self.texto_inicio, self.texto_inicio_rect)
        self.pantalla.blit(self.texto_salir, self.texto_salir_rect)
        self.pantalla.blit(self.texto_silenciar, self.texto_silenciar_rect)

        pygame.display.flip()

        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, 'musica', '15 - Credit Theme.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        eleccion = None
        while not eleccion:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_i:
                        self.sonido.play()
                        # ejecutar el juego
                        from main import Juego
                        juego = Juego()
                        juego.ejecutar()

                    elif evento.key == pygame.K_m:
                        if self.silenciado:
                            pygame.mixer.music.unpause()
                            self.silenciado = False
                        else:
                            pygame.mixer.music.pause()
                            self.silenciado = True

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.sonido_salir.play()
                        pygame.time.wait(1000)

                        pygame.quit()
                        sys.exit()

        return eleccion

    def mostrar_pantalla_dead(self):

        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.imagen_dead, self.imagen_dead_rect)

        self.pantalla.blit(self.texto_dead, self.texto_dead_rect)
        self.pantalla.blit(self.texto_inicio, self.texto_inicio_rect)
        self.pantalla.blit(self.texto_salir, self.texto_salir_rect)
        self.pantalla.blit(self.texto_silenciar, self.texto_silenciar_rect)
        pygame.display.flip()

        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, 'musica', '24 - Final Area.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        eleccion = None
        while not eleccion:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_i:
                        self.sonido.play()
                        # ejecutar el juego
                        from main import Juego
                        juego = Juego()
                        juego.ejecutar()

                    elif evento.key == pygame.K_m:
                        if self.silenciado:
                            pygame.mixer.music.unpause()
                            self.silenciado = False
                        else:
                            pygame.mixer.music.pause()
                            self.silenciado = True

                    elif evento.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.sonido_salir.play()
                        pygame.time.wait(1000)

                        pygame.quit()
                        sys.exit()
        return eleccion


class ElementosInterfaz:
    def __init__(self):

        self.area_pantalla = pygame.display.get_surface()
        self.tipo_fuente = pygame.font.Font(FUENTE, FUENTE_TAMANIO)
        self.tipo_fuente2 = pygame.font.Font(FUENTE2, FUENTE2_TAMANIO)
        self.indicador_vida = pygame.Rect(65, 37, INDICADOR_VIDA_LARGO, INDICADOR_ANCHO)


        self.imagen_dead = pygame.image.load(os.path.join(RUTA_IMAGENES, 'personajes', 'enemigos_16_px.png'))
        self.imagen_dead_rect = self.imagen_dead.get_rect( x = LARGO - 105, y = 31)

        self.imagen_win = pygame.image.load(os.path.join(RUTA_IMAGENES, 'personajes', 'jugador_16px.png'))
        self.imagen_win_rect = self.imagen_win.get_rect( x =   40, y = 31)


    # Descripcion: Muestra el titulo de la barra de vida
    def mostrar_titulo_juego(self, texto):

        texto_superficie = self.tipo_fuente2.render(texto, True, COLOR_TEXTO)
        texto_cuadro = texto_superficie.get_rect(midtop=(LARGO / 2, 20))
        fondo_cuadro = pygame.Surface((texto_cuadro.width + 40, texto_cuadro.height + 40), pygame.SRCALPHA)

        pygame.draw.rect(fondo_cuadro, (0, 0, 0, 128), fondo_cuadro.get_rect())

        self.area_pantalla.blit(texto_superficie, texto_cuadro)

    # Descripcion: Muestra el texto y porcentaje de vida del jugador
    def mostrar_vida_y_porcentaje(self, vida):
        # Renderizar la primera línea
        texto_vida = self.tipo_fuente.render('         ', False, COLOR_TEXTO)

        # Renderizar la segunda línea con el porcentaje de vida
        if vida <= 0:
            texto_porcentaje = self.tipo_fuente.render('Vida:' '0%', False, COLOR_TEXTO)
        else:
            texto_porcentaje = self.tipo_fuente.render('Vida:' f'{int(vida)}%', False, COLOR_TEXTO)

        # Establecer la posición para ambas líneas
        x = 35
        y_primera_linea = 50
        y_segunda_linea = y_primera_linea + 30  # Ajusta la separación entre líneas según sea necesario

        # Cuadro para la primera línea
        cuadro_primera_linea = texto_vida.get_rect(bottomleft=(x, y_primera_linea))

        # Cuadro para la segunda línea
        cuadro_segunda_linea = texto_porcentaje.get_rect(bottomleft=(x, y_segunda_linea))

        # Dibujar los cuadros y texto en la pantalla
        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_primera_linea.inflate(20, 20))
        self.area_pantalla.blit(texto_vida, cuadro_primera_linea)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_primera_linea.inflate(20, 20), 3)

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_segunda_linea.inflate(20, 20))
        self.area_pantalla.blit(texto_porcentaje, cuadro_segunda_linea)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_segunda_linea.inflate(20, 20), 3)

    # Descripcion: Muestra el indicador de vida del jugador alinear debajo de  mostrar_vida_y_porcentaje
    def mostrar_indicador_vida(self, vida):
        if vida <= 0:
            vida = 0
        if vida >= 100:
            vida = 100

        self.indicador_vida.width = vida * INDICADOR_VIDA_LARGO / 100

        pygame.draw.rect(self.area_pantalla, COLOR_VIDA, self.indicador_vida)

    # En la clase Jugador
    def mostrar_score_y_experiencia(self, score, score_para_ganar):
        texto_score = f'Objetivo: {score_para_ganar}'
        texto_score_para_ganar = f'Score: {int(score)}'

        superficie_score = self.tipo_fuente.render(texto_score, False, COLOR_TEXTO)
        superficie_score_para_ganar = self.tipo_fuente.render(texto_score_para_ganar, False, COLOR_TEXTO)

        x = LARGO - 30
        y_score = 50
        y_score_para_ganar = y_score + superficie_score.get_height() + 10

        cuadro_score = superficie_score.get_rect(bottomright=(x, y_score))
        cuadro_score_para_ganar = superficie_score_para_ganar.get_rect(bottomright=(x, y_score_para_ganar))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_score.inflate(20, 20))
        self.area_pantalla.blit(superficie_score, cuadro_score)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_score.inflate(20, 20), 3)

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_score_para_ganar.inflate(20, 20))
        self.area_pantalla.blit(superficie_score_para_ganar, cuadro_score_para_ganar)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_score_para_ganar.inflate(20, 20), 3)

    def enemigos_derrotados(self, enemigos_derrotados):
        # Renderizar la primera línea
        texto_kills = self.tipo_fuente.render('        ', False, COLOR_TEXTO)

        # Renderizar la segunda línea con la cantidad de enemigos derrotados
        texto_cantidad = self.tipo_fuente.render(f'Kills: {enemigos_derrotados}', False, COLOR_TEXTO)

        # Establecer la posición para ambas líneas
        x = LARGO - 30
        y_primera_linea = 50
        y_segunda_linea = y_primera_linea + 30  # Ajusta la separación entre líneas según sea necesario

        # Cuadro para la primera línea
        cuadro_primera_linea = texto_kills.get_rect(bottomright=(x, y_primera_linea))

        # Cuadro para la segunda línea
        cuadro_segunda_linea = texto_cantidad.get_rect(bottomright=(x, y_segunda_linea))

        # Dibujar los cuadros y texto en la pantalla
        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_primera_linea.inflate(20, 20))
        self.area_pantalla.blit(texto_kills, cuadro_primera_linea)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_primera_linea.inflate(20, 20), 3)

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_segunda_linea.inflate(20, 20))
        self.area_pantalla.blit(texto_cantidad, cuadro_segunda_linea)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_segunda_linea.inflate(20, 20), 3)

    def img_dead(self):
        self.area_pantalla.blit(self.imagen_dead, self.imagen_dead_rect)

    def img_win(self):
        self.area_pantalla.blit(self.imagen_win,  self.imagen_win_rect)


    def vida(self, vida):
        texto_superficie = self.tipo_fuente.render(f'Vida: {int(vida)}', False, COLOR_TEXTO)

        x = 35
        y = 130
        texto_cuadro = texto_superficie.get_rect(bottomleft=(x, y))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, texto_cuadro.inflate(20, 20))
        self.area_pantalla.blit(texto_superficie, texto_cuadro)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, texto_cuadro.inflate(20, 20), 3)

    def velocidad(self, velocidad):
        texto_superficie = self.tipo_fuente.render(f'Velocidad: {int(velocidad)}', False, COLOR_TEXTO)

        x = 35
        y = 165
        texto_cuadro = texto_superficie.get_rect(bottomleft=(x, y))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, texto_cuadro.inflate(20, 20))
        self.area_pantalla.blit(texto_superficie, texto_cuadro)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, texto_cuadro.inflate(20, 20), 3)

    def danio_ataque(self, danio_ataque):
        texto_superficie = self.tipo_fuente.render(f'Ataque: {int(danio_ataque)}', False, COLOR_TEXTO)

        x = 35
        y = 200
        texto_cuadro = texto_superficie.get_rect(bottomleft=(x, y))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, texto_cuadro.inflate(20, 20))
        self.area_pantalla.blit(texto_superficie, texto_cuadro)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, texto_cuadro.inflate(20, 20), 3)

    def mostrar_mensaje(self, texto):
        texto_superficie = self.tipo_fuente.render(texto, False, COLOR_TEXTO)
        texto_cuadro = texto_superficie.get_rect(midbottom=(LARGO / 2, ANCHO - 20))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, texto_cuadro.inflate(20, 20))
        self.area_pantalla.blit(texto_superficie, texto_cuadro)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, texto_cuadro.inflate(20, 20), 3)

        # En la clase Jugador
        # En la clase Jugador

        # En la clase Jugador

    def mostrar_score(self, score, score_para_ganar):
        texto_score_para_ganar = f'Score: {int(score)}'

        superficie_score_para_ganar = self.tipo_fuente.render(texto_score_para_ganar, False, COLOR_TEXTO)

        x = LARGO - 30
        y_score = 100
        y_score_para_ganar = y_score + 10

        cuadro_score_para_ganar = superficie_score_para_ganar.get_rect(bottomright=(x, y_score_para_ganar))

        pygame.draw.rect(self.area_pantalla, COLOR_FONDO, cuadro_score_para_ganar.inflate(20, 20))
        self.area_pantalla.blit(superficie_score_para_ganar, cuadro_score_para_ganar)
        pygame.draw.rect(self.area_pantalla, COLOR_BORDE, cuadro_score_para_ganar.inflate(20, 20), 3)

    def display(self, jugador):
        self.mostrar_titulo_juego('SAMURAIGHOST VS GOBLINS')
        self.mostrar_vida_y_porcentaje(jugador.vida * 100 / jugador.vida_original)
        self.mostrar_indicador_vida(jugador.vida * 100 / jugador.vida_original)
        self.enemigos_derrotados(jugador.enemigos_derrotados)
        self.img_dead()
        self.img_win()
        self.mostrar_score(jugador.score, jugador.score_para_ganar)
       # self.mostrar_score_y_experiencia(jugador.score, jugador.score_para_ganar)

        self.vida(jugador.vida)
        self.velocidad(jugador.velocidad)
        self.danio_ataque(jugador.danio_ataque)

        self.mostrar_mensaje('   P para pausar     ESPACIO para atacar     M para silenciar     ESC para salir   ')
