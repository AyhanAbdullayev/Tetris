import pygame
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
Tile = 35
Game_RES = W * Tile, H * Tile
Fps = 60
RES = 800, 1000
pygame.init()
display = pygame.display.set_mode(Game_RES)

pygame.display.set_caption("Tetris")
figure_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]

myfont = pygame.font.Font('images/txt.ttf', 70)
myfont2 = pygame.font.Font('images/txt.ttf', 50)

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figure_pos]
figure_rect = pygame.Rect(0, 0, Tile - 2, Tile - 2)
field = [[0 for _ in range(W)] for _ in range(H)]
figure = deepcopy(choice(figures))
get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
color = get_color()
clock = pygame.time.Clock()

def check_boarders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > W - 1:
            return False
        if figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
            return False 
    return True

anim_count, anim_speed, anim_limit = 0, 60, 2000
running = True
grid = [pygame.Rect(x * Tile, y * Tile, Tile, Tile) for x in range(W) for y in range(H)]

while running:
    dx, rotate = 0, False
    display.fill(pygame.Color("black"))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx -= 1
            if event.key == pygame.K_RIGHT:
                dx += 1
            if event.key == pygame.K_DOWN:
                anim_limit = 50
            if event.key == pygame.K_UP:
                rotate = True

    figure_old = deepcopy(figure)

    for i in range(4):
        figure[i].x += dx
        if not check_boarders():
            figure = deepcopy(choice(figures))
            break

    for i in range(4):
        figure[i].x += dx
        if not check_boarders():
            figure = deepcopy(figure_old)
            break

    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_boarders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                color = get_color()
                figure = deepcopy(choice(figures))
                anim_limit = 1000
                break

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_boarders():
                figure = deepcopy(figure_old)
                break

    line = H - 1
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
                field[line][i] = field[row][i]
        if count < W:
            count -= 1

    [pygame.draw.rect(display, (40, 40, 40), i_rect, 1) for i_rect in grid]

    for i in range(4):
        figure_rect.x = figure[i].x * Tile
        figure_rect.y = figure[i].y * Tile
        pygame.draw.rect(display, color, figure_rect)

    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * Tile, y * Tile
                pygame.draw.rect(display, col, figure_rect)

    text_tetris = myfont.render("Tetris", False, "yellow")
    display.blit(text_tetris, (-485, 10))
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)for i in range(H)]]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0

    pygame.display.flip()
    clock.tick(Fps)

pygame.quit()