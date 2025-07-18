import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pomodoro Timer 🍅")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Timer state
timer_running = False
paused = False
time_left = 0
end_time = 0
current_color = (128, 0, 32)  # bordo

# Click debounce variables
last_click_time = 0
click_delay = 0.3  # seconds

# Draw button on screen
def draw_button(text, x, y, width, height, color, action=None):
    global last_click_time
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255)
        ), rect)
        if click[0] == 1 and action:
            current_time = time.time()
            if current_time - last_click_time > click_delay:
                action()
                last_click_time = current_time
    else:
        pygame.draw.rect(screen, color, rect)

    btn_text = font.render(text, True, (255, 255, 255))
    text_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, text_rect)

# Start the timer
def start_timer():
    global timer_running, paused, time_left, end_time
    if not timer_running:
        timer_running = True
        paused = False
        time_left = 25 * 60  # 25 minutes
        end_time = time.time() + time_left

# Pause or resume the timer
def pause_timer():
    global paused, end_time, time_left, timer_running
    if timer_running:
        if not paused:
            time_left = end_time - time.time()
            paused = True
        else:
            end_time = time.time() + time_left
            paused = False

# Reset the timer
def reset_timer():
    global timer_running, paused, time_left, end_time
    timer_running = False
    paused = False
    time_left = 0
    end_time = 0  # Clear end_time on reset

# Main app loop
def timer_loop():
    global time_left, timer_running, paused

    while True:
        screen.fill(current_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update timer
        if timer_running and not paused:
            time_left = max(0, int(end_time - time.time()))
            if time_left == 0:
                timer_running = False

        # Draw timer text
        total_seconds = int(time_left)
        mins = total_seconds // 60
        secs = total_seconds % 60
        timer_text = font.render(f"Timer: {mins:02d}:{secs:02d}", True, (255, 255, 255))
        text_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(timer_text, text_rect)

        # Draw buttons
        draw_button("Start", 50, HEIGHT - 80, 80, 40, (0, 150, 0), start_timer)
        draw_button("Pause", 160, HEIGHT - 80, 80, 40, (200, 150, 0), pause_timer)
        draw_button("Reset", 270, HEIGHT - 80, 80, 40, (150, 0, 0), reset_timer)

        pygame.display.flip()
        clock.tick(60)

# Start the program
if __name__ == "__main__":
    timer_loop()
