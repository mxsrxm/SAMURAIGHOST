# Version: 1.0
# Autor: Aldo Misraim Hernandez Gonzalez
# Ultima fecha de modificacion: 30/Noviembre/2023

import random
from sprite import *
from interfaz import *
import pandas as pd


class Jugador(Entidad):
    def __init__(self,
                 posicion, grupos, obstaculos_sprites, crear_ataque, destruir_ataque, tiempo_velocidad_extra=0, tiempo_ataque_extra=0):
        super().__init__(grupos)

        df = pd.read_csv(os.path.join(RUTA_CSV, 'u_personajes.csv'))

        # Convierte el DataFrame a una lista plana
        flat_list = df.values.flatten().tolist()

        # Cuenta el número de ocurrencias de cada índice
        contador_personaje_principal = flat_list.count(0)

        contador_ojo = flat_list.count(1)
        contador_calavera = flat_list.count(2)
        contador_demonio = flat_list.count(3)
        contador_monstruo = flat_list.count(4)
        contador_flamaAzul = flat_list.count(5)
        contador_flamaRoja = flat_list.count(6)

        contador_jefeAzul = flat_list.count(7)
        contador_jefeRojo = flat_list.count(8)
        contador_jefeDemonio = flat_list.count(9)

        contador_pocion_vida = flat_list.count(10)
        contador_pocion_velocidad = flat_list.count(11)
        contador_pocion_ataque = flat_list.count(12)


        contador_goblins = contador_ojo + contador_calavera + contador_demonio + contador_monstruo + contador_flamaAzul + contador_flamaRoja + contador_jefeAzul + contador_jefeRojo + contador_jefeDemonio

        # Imprime los resultados
        print(f"Número de personajes principales: {contador_personaje_principal}")
        print(f"Número de ojos: {contador_ojo}")
        print(f"Número de calaveras: {contador_calavera}")
        print(f"Número de demonios: {contador_demonio}")
        print(f"Número de monstruos: {contador_monstruo}")
        print(f"Número de flamas azules: {contador_flamaAzul}")
        print(f"Número de flamas rojas: {contador_flamaRoja}")
        print(f"Número de jefes azules: {contador_jefeAzul}")
        print(f"Número de jefes rojos: {contador_jefeRojo}")
        print(f"Número de jefes demonios: {contador_jefeDemonio}")
        print(f"Número de pociones de vida: {contador_pocion_vida}")
        print(f"Número de pociones de velocidad: {contador_pocion_velocidad}")
        print(f"Número de pociones de ataque: {contador_pocion_ataque}")
        print(f"Número de goblins: {contador_goblins}")


        self.contador_goblins_derrotados = contador_goblins

        self.sonido_bonus = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'menu', 'Menu9.wav'))


        self.imagen = pygame.image.load(os.path.join(RUTA_IMAGENES, 'personajes', 'jugador.png')).convert_alpha()
        self.rect = self.imagen.get_rect(topleft=posicion)
        self.impacto = self.rect.inflate(-6, CONJUNTO_ELEMENTOS['movimiento_jugador'])

        # Notas: Mantener la etiqueta de status en 'down' para que que el idle del jugador
        # funcione correctamente y la vista del idle sea hacia abajo (frente)

        self.importar_imagenes_jugador()
        self.status = 'down'
        self.atacando = False
        self.bloqueo_ataque = 100
        self.tiempo_de_ataque = None
        self.obstaculos_sprites = obstaculos_sprites

        # Se crea el ataque del jugador
        self.crear_ataque = crear_ataque
        self.destruir_ataque = destruir_ataque
        self.arma_index = 0
        self.arma = list(ataque.keys())[self.arma_index]
        self.cambiar_arma = True
        self.tiempo_cambio_arma = None
        self.tiempo_bloqueo_cambio_arma = 250

        # Se definen las habilidades del jugador

        self.tiempo_velocidad_extra = tiempo_velocidad_extra
        self.tiempo_ataque_extra = tiempo_ataque_extra

        self.vida = 5000
        self.vida_original = 5000

        self.danio_ataque_original = 15
        self.danio_ataque = self.danio_ataque_original

        self.velocidad_original = 4.5
        self.velocidad = self.velocidad_original




        self.score = 0
        self.enemigos_derrotados = 0








        # Se define el porcentaje de vida del jugador
        if self.vida >= 1:
            self.porcentaje_vida = self.vida * 100 / self.vida
        else:
            self.vida <= 0
            self.porcentaje_vida = 0


        self.score_para_ganar = random.randint(1500, 4000)

        # Se la vulnerabilidad del jugador
        self.vulnerabilidad = True
        self.tiempo_de_herida = None
        self.duracion_de_invulnerabilidad = 500

        # Se definen los sonidos del jugador
        self.sonido_de_arma = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, 'sonido_ataque', 'golpe.wav'))
        self.sonido_de_arma.set_volume(1)



    # En la clase Jugador
    def actualizar_temporizador_velocidad(self):
        if self.tiempo_velocidad_extra > 0:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_pasado = tiempo_actual - self.tiempo_velocidad_extra


            if tiempo_pasado >= 10000:  # 10 segundos en milisegundos
                self.tiempo_velocidad_extra = 0
                self.velocidad = self.velocidad_original

    def actualizar_temporizador_ataque(self):
        if self.tiempo_ataque_extra > 0:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_pasado = tiempo_actual - self.tiempo_ataque_extra


            if tiempo_pasado >= 10000:  # 10 segundos en milisegundos
                self.tiempo_aatque_extra = 0
                self.danio_ataque = self.danio_ataque_original


    # Se importan las imagenes del jugador
    # Nota: Mantener los nombres de las carpetas de las imagenes del jugador para que
    # coincidan con los nombres de las animaciones



    def importar_imagenes_jugador(self):
        ruta = os.path.join(RUTA_IMAGENES, 'movimiento_jugador')  # Cambiada la ruta
        self.animaciones = {'up': [], 'down': [], 'left': [], 'right': [],
                            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animacion in self.animaciones.keys():
            ruta_completa = os.path.join(ruta, animacion)  # Cambiada la ruta
            self.animaciones[animacion] = importar_carpeta(ruta_completa)

    # Se definen los controladores de movimiento del jugador, ataque y cambio de arma
    def input(self):
        if not self.atacando:
            tecla = pygame.key.get_pressed()

            # Se definen teclas para los movimientos del jugador
            if tecla[pygame.K_UP]:
                self.direccion.y = -1
                self.status = 'up'
            elif tecla[pygame.K_DOWN]:
                self.direccion.y = 1
                self.status = 'down'
            else:
                self.direccion.y = 0

            if tecla[pygame.K_RIGHT]:
                self.direccion.x = 1
                self.status = 'right'
            elif tecla[pygame.K_LEFT]:
                self.direccion.x = -1
                self.status = 'left'
            else:
                self.direccion.x = 0

            # Teclear espacio para atacar
            if tecla[pygame.K_SPACE]:
                self.atacando = True
                self.tiempo_de_ataque = pygame.time.get_ticks()
                self.crear_ataque()
                self.sonido_de_arma.play()

    # Se definen los movimientos del jugador
    # Nota: mantener el nombre de las etiquettas para que coincidan con el nombre de las
    # animacionesy las carpetas de las imagenes del jugador
    def estado(self):

        if self.direccion.x == 0 and self.direccion.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.atacando:
            self.direccion.x = 0
            self.direccion.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    # Se definen los bloqueos del jugador
    def bloqueos(self):
        current_time = pygame.time.get_ticks()

        if self.atacando:
            if current_time - self.tiempo_de_ataque >= self.bloqueo_ataque + ataque[self.arma][
                'tiempo_de_espera_bloqueo']:
                self.atacando = False
                self.destruir_ataque()


        if not self.vulnerabilidad:
            if current_time - self.tiempo_de_herida >= self.duracion_de_invulnerabilidad:
                self.vulnerabilidad = True

    # Se definen las animaciones del jugador
    def animar(self):
        animacion = self.animaciones[self.status]

        self.frame_index += self.animacion_velocidad
        if self.frame_index >= len(animacion):
            self.frame_index = 0

        self.imagen = animacion[int(self.frame_index)]
        self.rect = self.imagen.get_rect(center=self.impacto.center)

        if not self.vulnerabilidad:
            alpha = self.valor_entidad()
            self.imagen.set_alpha(alpha)
        else:
            self.imagen.set_alpha(255)

    # Se define el daño que hace el jugador
    def danio_total_arma(self):
        danio_inicial = self.danio_ataque
        danio_arma = ataque[self.arma]['danio']
        return danio_inicial + danio_arma




    def update(self):
        self.input()
        self.bloqueos()
        self.estado()
        self.animar()
        self.mover(self.velocidad)
        self.actualizar_temporizador_velocidad()
        self.actualizar_temporizador_ataque()




        # Verificar si la vida del jugador ha llegado a cero
        if self.vida <= 0:
            pygame.mixer.music.pause()
            pantalla_eleccion = Menu()
            pantalla_eleccion.mostrar_pantalla_dead()

        if self.enemigos_derrotados >= self.contador_goblins_derrotados:
            pygame.mixer.music.pause()
            pantalla_eleccion = Menu()
            pantalla_eleccion.mostrar_pantalla_win()

       #if self.score >= self.score_para_ganar:
            pygame.mixer.music.pause()
         #   pantalla_eleccion = Menu()
          #  pantalla_eleccion.mostrar_pantalla_win()

        # Lee el archivo CSV os.path.join(RUTA_CSV, 'BASE2_personajes.csv')),



