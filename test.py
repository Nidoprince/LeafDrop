import pygame
print(pygame.font.get_fonts())
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
pygame.mixer.music.load("test.ogg")
pygame.mixer.music.play(-1)
while 1:
	True
