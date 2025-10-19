import pygame
from pygame import Rect
from src.video_background import VideoBackground

class SceneK:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # --- Assets ---
        # OJO al nombre con espacio: "escenario k.png"
        self.bg_img = pygame.image.load("assets/escenario k.png").convert()
        self.bg_img = pygame.transform.smoothscale(self.bg_img, self.screen.get_size())

        # Personaje (recortado con alpha)
        self.char_img = pygame.image.load("assets/motocle.png").convert_alpha()
        # Escálalo si quieres (opcional):
        # self.char_img = pygame.transform.smoothscale(self.char_img, (420, 420))
        self.char_pos = self._char_pos_bottom_center(self.char_img, y_offset=-80)
        self.char_alpha = 255  # Para desvanecer al terminar diálogo

        # Tipografías (reusa tu TTF si quieres que combine con el menú)
        try:
            self.font_dialog = pygame.font.Font("util/HauntingEleanor-Regular.ttf", 36)
            self.font_name = pygame.font.Font("util/HauntingEleanor-Regular.ttf", 28)
        except:
            self.font_dialog = pygame.font.SysFont(None, 36)
            self.font_name = pygame.font.SysFont(None, 28)

        # Diálogo (edita estas líneas a tu gusto)
        self.speaker = "Motocle"
        self.dialog_lines = [
            "Llegamos. Mantén la calma… algo no cuadra en este lugar.",
            "¿Ves esas marcas en el suelo? No son recientes.",
            "…Silencio. Escucha.",
            "Está por empezar."
        ]
        self.dialog_index = 0

        # Estados: "dialogue" -> "fade_out" -> "video" -> "black"
        self.state = "dialogue"
        self.fade_speed = 12  # píxeles alfa por frame
        self.video = None
        self.black_timer_ms = 0

        # Colores
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.box_bg = (0, 0, 0, 180)  # semi-transparente
        self.box_border = (200, 0, 0)

        # Cuadro de diálogo
        w, h = self.screen.get_size()
        box_height = int(h * 0.28)
        self.dialog_rect = Rect(int(w * 0.05), h - box_height - int(h * 0.04),
                                int(w * 0.90), box_height)

        # Preparar surface para alpha del cuadro
        self.dialog_surface = pygame.Surface((self.dialog_rect.width, self.dialog_rect.height), pygame.SRCALPHA)

    def _char_pos_bottom_center(self, surf, y_offset=0):
        sw, sh = self.screen.get_size()
        w, h = surf.get_size()
        x = (sw - w) // 2
        y = sh - h + y_offset
        return (x, y)

    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def _draw_dialog_box(self, speaker, text):
        # Fondo semi-transparente
        self.dialog_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.dialog_surface, self.box_bg, Rect(0, 0, self.dialog_rect.width, self.dialog_rect.height), border_radius=16)
        # Borde
        pygame.draw.rect(self.dialog_surface, self.box_border, Rect(0, 0, self.dialog_rect.width, self.dialog_rect.height), width=3, border_radius=16)

        # Nombre del personaje
        name_surf = self.font_name.render(speaker, True, self.white)
        self.dialog_surface.blit(name_surf, (16, 12))

        # Texto envuelto
        max_text_width = self.dialog_rect.width - 32
        wrapped = self._wrap_text(text, self.font_dialog, max_text_width)
        y = 48
        line_spacing = 8
        for line in wrapped[:4]:  # máximo 4 líneas visibles
            line_surf = self.font_dialog.render(line, True, self.white)
            self.dialog_surface.blit(line_surf, (16, y))
            y += line_surf.get_height() + line_spacing

        # Sugerencia para continuar
        hint = self.font_name.render("Pulsa X para continuar…", True, (220, 220, 220))
        hint_rect = hint.get_rect(bottomright=(self.dialog_rect.width - 14, self.dialog_rect.height - 12))
        self.dialog_surface.blit(hint, hint_rect)

        # Blit al screen
        self.screen.blit(self.dialog_surface, self.dialog_rect.topleft)

    def _start_video(self):
        # OJO al nombre con espacio: "escenario k.mp4"
        self.video = VideoBackground("assets/escenario k.mp4", self.screen.get_size(), loop=False)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if self.state == "dialogue" and event.key == pygame.K_x:
                self.dialog_index += 1
                if self.dialog_index >= len(self.dialog_lines):
                    # Termina el diálogo, arrancamos fade out del personaje/cuadro
                    self.state = "fade_out"

    def update(self):
        if self.state == "fade_out":
            self.char_alpha = max(0, self.char_alpha - self.fade_speed)
            if self.char_alpha == 0:
                # Iniciar video
                self._start_video()
                self.state = "video"
        elif self.state == "video":
            # Nada que actualizar aquí; el avance lo controla get_frame()
            pass
        elif self.state == "black":
            self.black_timer_ms += self.clock.get_time()
            # Mantén negro; puedes salir a los 2s o esperar tecla si prefieres
            if self.black_timer_ms >= 2000:
                self.running = False

    def draw(self):
        if self.state in ("dialogue", "fade_out"):
            # Fondo estático
            self.screen.blit(self.bg_img, (0, 0))
            # Personaje
            char = self.char_img.copy()
            if self.state == "fade_out":
                char.set_alpha(self.char_alpha)
            self.screen.blit(char, self.char_pos)
            # Cuadro de diálogo (solo durante "dialogue")
            if self.state == "dialogue":
                self._draw_dialog_box(self.speaker, self.dialog_lines[self.dialog_index])

        elif self.state == "video":
            frame_surface = self.video.get_frame()
            if frame_surface is None:
                # Video terminó
                self.state = "black"
            else:
                self.screen.blit(frame_surface, (0, 0))

        elif self.state == "black":
            self.screen.fill(self.black)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.update()
            self.draw()
            self.clock.tick(30)

        # Limpieza
        if self.video:
            self.video.release()
