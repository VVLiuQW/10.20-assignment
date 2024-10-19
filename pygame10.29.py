import pygame
import random
import time

pygame.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kill the Pumpkin")

WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
PINK = (255, 182, 193)
RED = (255, 0, 0)

base_path = "/Users/liuqianwei/10.20 assignment/"

mole_image = pygame.image.load('mole.PNG')  
mole_image = pygame.transform.scale(mole_image, (80, 80))  
mole2_image = pygame.image.load('mole2.PNG')  
mole2_image = pygame.transform.scale(mole2_image, (80, 80))  
background_image = pygame.image.load('background.jpg')  
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  
background2_image = pygame.image.load('background2.png')
background2_image = pygame.transform.scale(background2_image,(screen_width, screen_height))

score = 0
mole_position = None
mole_type = None  
mole_timer = 0
game_time = 15  
mole_visible_time = 1  
clock = pygame.time.Clock()

# 随机生成地鼠的位置
def random_mole_position():
    x = random.randint(0, screen_width - 80)
    y = random.randint(0, screen_height - 80)
    return (x, y)

def show_start_screen():
    running = True
    while running:
        screen.blit(background_image, (0, 0)) 

        font = pygame.font.Font(None, 48)
        title_text = font.render("Happy Halloween", True, PINK)
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_text, title_rect) 

        button_rect = pygame.Rect(200, 150, 200, 50) 
        pygame.draw.rect(screen, PINK, button_rect, border_radius=15)  
        button_text = font.render("Start", True, WHITE)
        text_rect = button_text.get_rect(center=button_rect.center)  
        screen.blit(button_text, text_rect)

        pygame.display.flip()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):  
                    running = False  

        clock.tick(60) 

def game_loop():
    global score, mole_position, mole_type, mole_timer
    running = True
    start_time = time.time()
    
  
    mole_position = random_mole_position()
    mole_type = random.choice(['normal', 'negative'])  
    mole_timer = time.time() + mole_visible_time

    while running:
        screen.blit(background_image, (0, 0)) 

       

       
        remaining_time = max(0, game_time - int(time.time() - start_time))
        
        
        mole1_image = pygame.image.load('mole2.PNG')  
        mole1_image = pygame.transform.scale(mole1_image, (80, 80))
        if mole_position:
            if mole_type == 'normal':
                screen.blit(mole_image, mole_position)  
            elif mole_type == 'negative':
                screen.blit(mole2_image, mole_position)  
        
        if time.time() > mole_timer:
            mole_type = 'normal' if random.random() < 0.7 else 'negative'  
            mole_position = random_mole_position()
            mole_timer = time.time() + mole_visible_time

        # 显示分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"YOU GOT: {score}", True, BROWN)
        screen.blit(score_text, (10, 10))

        # 显示倒计时
        timer_text = font.render(f"TIME: {remaining_time}", True, RED)
        screen.blit(timer_text, (screen_width - 200, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                if mole_position and (mole_position[0] <= mouse_pos[0] <= mole_position[0] + 80) and (mole_position[1] <= mouse_pos[1] <= mole_position[1] + 80):
                    if mole_type == 'normal':
                        score += 1  
                    else:
                        score -= 1 
                    mole_position = None  

        if time.time() > mole_timer:
            mole_position = random_mole_position()  
            mole_type = random.choice(['normal', 'negative'])  
            mole_timer = time.time() + mole_visible_time

        if remaining_time <= 0:
            running = False

        clock.tick(60)  

    return score

def show_congratulations(final_score):
    running = True
    while running:
        screen.blit(background2_image, (0, 0))

        font = pygame.font.Font(None, 48)
        congrats_text = font.render("Congratulations!", True, RED)
        score_text = font.render(f"You Got: {final_score}", True, BROWN)
        restart_text = font.render("Restart", True, PINK)

        bottom_margin = 50
        restart_rect = restart_text.get_rect(topright=(screen_width - 100, screen_height - bottom_margin - restart_text.get_height()))
        score_rect = score_text.get_rect(topright=(screen_width - 100, restart_rect.top - score_text.get_height()))
        congrats_rect = congrats_text.get_rect(topright=(screen_width - 100, score_rect.top - congrats_text.get_height()))

        screen.blit(congrats_text, congrats_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return  

        pygame.display.flip()
        clock.tick(60)

def main():
    show_start_screen()  
    while True:
        final_score = game_loop()
        show_congratulations(final_score)

if __name__ == "__main__":
    main()
    pygame.quit()

