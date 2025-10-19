import cv2
import pygame
import numpy as np

class VideoBackground:
    def __init__(self, video_path, screen_size, loop=True):
        self.cap = cv2.VideoCapture(video_path)
        self.width, self.height = screen_size
        self.loop = loop

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            if self.loop:
                # Reiniciar el video al finalizar
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    return None
            else:
                # Sin loop: señal de fin de video
                return None

        frame = cv2.resize(frame, (self.width, self.height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)
        return frame_surface

    def release(self):
        self.cap.release()
