import pygame
from src.video_background import VideoBackground

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Configuración del video
        self.background = VideoBackground("assets/escenario.mp4", screen.get_size())

        # Cargar tipografía personalizada
        self.title_font = pygame.font.Font("util/HauntingEleanor-Regular.ttf", 100)
        self.menu_font = pygame.font.Font("util/HauntingEleanor-Regular.ttf", 48)

        # Colores
        self.white = (255, 255, 255)
        self.red = (200, 0, 0)

        # Opciones del menú
        self.options = ["Start", "History", "Option", "About"]
        self.selected_index = 0

    def draw_text_centered(self, text, font, y, color):
        render = font.render(text, True, color)
        rect = render.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(render, rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.handle_selection()

            # Dibujar fondo animado
            frame_surface = self.background.get_frame()
            self.screen.blit(frame_surface, (0, 0))

            # Título
            self.draw_text_centered("DEADLY OUTBREAK", self.title_font, 120, self.red)

            # Opciones del menú
            start_y = 350
            for i, option in enumerate(self.options):
                color = self.red if i == self.selected_index else self.white
                self.draw_text_centered(option, self.menu_font, start_y + i * 80, color)

            pygame.display.flip()
            self.clock.tick(30)

        self.background.release()

    def handle_selection(self):
        selected = self.options[self.selected_index]
        print(f"Seleccionado: {selected}")
        # Aquí más adelante se podrán conectar las pantallas de juego, historia, etc.
