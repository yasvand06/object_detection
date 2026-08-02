import pygame

pygame.init()
pygame.mixer.music.load("Alarm/alarm2.wav")

def trigger_alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
