import pygame
import random

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("简单射击游戏")

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
MENU_BG_COLOR = (33, 34, 35)  # 菜单背景颜色
MENU_TEXT_COLOR = (232, 232, 232)  # 菜单文本颜色
MENU_HOVER_COLOR = (132, 188, 230)  # 菜单选项悬停颜色

# 玩家飞船
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_lives = 3

# 子弹
bullet_width = 5
bullet_height = 15
bullet_speed = 10
bullets = []

# 敌人
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# 分数
score = 0
font = pygame.font.Font(None, 36)

# 音效
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.mp3")
explosion_sound = pygame.mixer.Sound("boom.mp3")
background_music = pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # 循环播放背景音乐

# 游戏状态
game_over = False
paused = False
menu_active = True

# 生成敌人
def create_enemy():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = -enemy_height
    enemy_type = random.choice(["normal", "fast", "heavy"])
    if enemy_type == "fast":
        enemy_speed = 5
        enemy_score = 50
    elif enemy_type == "heavy":
        enemy_speed = 2
        enemy_score = 100
    else:
        enemy_speed = 3
        enemy_score = 30
    enemies.append([enemy_x, enemy_y, enemy_speed, enemy_score])

# 检测碰撞
def check_collision():
    global score
    for bullet in bullets:
        for enemy in enemies:
            if (bullet[0] < enemy[0] + enemy_width and
                bullet[0] + bullet_width > enemy[0] and
                bullet[1] < enemy[1] + enemy_height and
                bullet[1] + bullet_height > enemy[1]):
                bullets.remove(bullet)
                score += enemy[3]
                enemies.remove(enemy)
                explosion_sound.play()

# 检测玩家与敌人碰撞
def check_player_collision():
    global player_lives
    for enemy in enemies:
        if (player_x < enemy[0] + enemy_width and
            player_x + player_width > enemy[0] and
            player_y < enemy[1] + enemy_height and
            player_y + player_height > enemy[1]):
            player_lives -= 1
            enemies.remove(enemy)
            explosion_sound.play()
            if player_lives <= 0:
                return True
    return False

# 游戏菜单
def show_menu():
    menu_font = pygame.font.Font(None, 48)
    title_text = menu_font.render("简单射击游戏", True, MENU_TEXT_COLOR)
    
    # 获取鼠标位置
    mouse_pos = pygame.mouse.get_pos()

    # 创建菜单选项文本
    start_text = menu_font.render("按 S 开始游戏", True, MENU_TEXT_COLOR)
    quit_text = menu_font.render("按 Q 退出游戏", True, MENU_TEXT_COLOR)

    # 获取菜单选项的矩形区域
    start_rect = start_text.get_rect(center=(screen_width // 2, 300))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, 400))

    # 检测鼠标悬停并改变颜色
    if start_rect.collidepoint(mouse_pos):
        start_text = menu_font.render("按 S 开始游戏", True, MENU_HOVER_COLOR)
    if quit_rect.collidepoint(mouse_pos):
        quit_text = menu_font.render("按 Q 退出游戏", True, MENU_HOVER_COLOR)

    # 绘制菜单背景和文本
    screen.fill(MENU_BG_COLOR)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()

# 游戏主循环
clock = pygame.time.Clock()
while not game_over:
    # 显示游戏菜单
    if menu_active:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_active = False
                elif event.key == pygame.K_q:
                    game_over = True
        continue

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
                shoot_sound.play()
            if event.key == pygame.K_p:
                paused = not paused

    if paused:
        continue

    # 获取按键状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # 更新子弹位置
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # 更新敌人位置
    for enemy in enemies:
        enemy[1] += enemy[2]
        if enemy[1] > screen_height:
            enemies.remove(enemy)
            player_lives -= 1
            if player_lives <= 0:
                game_over = True

    # 随机生成敌人
    if random.randint(1, 50) == 1:
        create_enemy()

    # 检测碰撞
    check_collision()

    # 检测玩家与敌人碰撞
    if check_player_collision():
        game_over = True

    # 绘制屏幕
    screen.fill(BLACK)
    # 绘制玩家飞船
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    # 绘制子弹
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))
    # 绘制敌人
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))
    # 绘制分数
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    # 绘制生命值
    lives_text = font.render(f"Lives: {player_lives}", True, GREEN)
    screen.blit(lives_text, (screen_width - 100, 10))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 游戏结束
pygame.quit()
print("游戏结束，你的得分是：", score)