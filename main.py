import pygame
from pathlib import Path

from src.video_background import VideoBackground
from src.scene_k import SceneK

# ------ Tu clase tal cual ------
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Rutas relativas al archivo, no al cwd
        base = Path(__file__).resolve().parent
        assets = base / "assets"
        util = base / "util"

        # Fondo de video (loop)
        self.background = VideoBackground(str(assets / "escenario.mp4"), screen.get_size())

        # Tipografías (con fallback si no existe el TTF)
        font_path = util / "HauntingEleanor-Regular.ttf"
        if font_path.exists():
            self.title_font = pygame.font.Font(str(font_path), 100)
            self.menu_font = pygame.font.Font(str(font_path), 48)
        else:
            self.title_font = pygame.font.SysFont(None, 100)
            self.menu_font = pygame.font.SysFont(None, 48)

        self.white = (255, 255, 255)
        self.red = (200, 0, 0)
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

            # Fondo animado del menú
            frame_surface = self.background.get_frame()
            if frame_surface is not None:
                self.screen.blit(frame_surface, (0, 0))
            else:
                self.screen.fill((0, 0, 0))  # por si no hay frame

            # Título
            self.draw_text_centered("DEADLY OUTBREAK", self.title_font, 120, self.red)

            # Opciones
            start_y = 350
            for i, option in enumerate(self.options):
                color = self.red if i == self.selected_index else self.white
                self.draw_text_centered(option, self.menu_font, start_y + i * 80, color)

            pygame.display.flip()
            self.clock.tick(30)

        # liberar recursos del video al salir
        self.background.release()

    def handle_selection(self):
        selected = self.options[self.selected_index]
        print(f"Seleccionado: {selected}")
        if selected == "Start":
            scene = SceneK(self.screen)
            scene.run()
# ------ fin de tu clase ------

if __name__ == "__main__":
    pygame.init()
    try:
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Deadly Outbreak")
        menu = MainMenu(screen)
        menu.run()
    finally:
        pygame.quit()
