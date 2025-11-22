import json
import os
import sys
import pygame
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "questions.json")  # Path to questions data
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # Path to assets folder
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")  # Path to assets folder

class Team:
    """Represents a team in the game."""
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.strikes = 0

def main():
    pygame.init()

    # initialize mixer (may fail on some systems; handle gracefully)
    mixer_available = True
    try:
        pygame.mixer.init()
    except Exception:
        mixer_available = False


    pygame.display.set_caption("Faculty Feud")
    
    #size = (1280, 720)
    #screen = pygame.display.set_mode(size)
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    #welcome screen
    ##set screen 
    stage_image = pygame.image.load(os.path.join(ASSETS_DIR, "family-feud-stage.jpg")).convert()
    stage_image = pygame.transform.smoothscale(stage_image, (screen.get_width(), screen.get_height()))
    main_image = pygame.image.load(os.path.join(ASSETS_DIR, "fam-feud-home-screen.jpg")).convert()
    main_image = pygame.transform.smoothscale(main_image, (screen.get_width(), screen.get_height()))
    theme_audio = os.path.join(SOUNDS_DIR, "family-feud-theme-main.mp3")
    game_font = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None, 28)
    input_font = pygame.font.SysFont(None, 64)
    question_font = pygame.font.SysFont(None, 84)

    size = screen.get_size()
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    question_counter = 1
    screencounter = 0
    ##for typing names on intro screen
    active_input = 0
    ##list of team names
    team_names = ["", ""]
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and screencounter == 0:
                screencounter+=1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif screencounter == 1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    active_input = 1 - active_input  # Switch input box
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if all(n.strip() for n in team_names):
                        team1 = Team(team_names[0].strip())
                        team2 = Team(team_names[1].strip())
                        screencounter+=1  # Start game if both names entered
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    team_names[active_input] = team_names[active_input][:-1]
                elif event.type == pygame.KEYDOWN:
                    ch = event.unicode
                    if ch.isprintable():
                        team_names[active_input] += ch
    
        if screencounter == 0:
            #Clear the screen (e.g., fill with a color or blit a background image)
            screen.fill((0, 0, 0)) # Fills with black
            #Set steve harvey screen
            screen.blit(main_image, (0, 0))

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(theme_audio)
                pygame.mixer.music.play()

            #Main screen text
            main_screen_text = game_font.render("Press space for next screen!", True, (255, 255, 255)) # White text
            screen.blit(main_screen_text, (screen.get_width()*(0.6), screen.get_height()*(0.9)))

        if screencounter == 1:
            screen.fill((0, 0, 0)) # Fills with black
            #Set stage screen
            screen.blit(stage_image, (0, 0))

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(theme_audio)
                pygame.mixer.music.play()
            
            title = input_font.render("Enter Team Names:", True, (255, 255, 255))
            screen.blit(title, (screen.get_width()*0.5 - title.get_width()*0.5, screen.get_height()*0.05))
            for i in range(2):
                label = input_font.render(f"Team {i+1}: ", True, (65,105,245))
                name = input_font.render(team_names[i] or "_", True, (255, 255, 255) if active_input == i else (180, 180, 180))
                y = 115 + i * 90
                screen.blit(label, (size[0] // 2 - 320, y))
                screen.blit(name, (size[0] // 2 - 80, y))
            instr = game_font.render("Tab: Switch | Enter: Confirm | ESC: Quit", True, (255, 255, 220))
            screen.blit(instr, (screen.get_width()*0.5 - instr.get_width()*0.5,screen.get_height()*0.96))
            pygame.display.flip()
            clock.tick(30)
        if screencounter > 1:
            if(screencounter % 2 == 0):
                screen.fill((0, 0, 0)) 
                screen.blit(stage_image, (0, 0))
                round = data["rounds"][question_counter - 1]
                question_text = round["question"]

                box_width = (len(question_text) * 20)
                    
                ##Draw question box + add questions
                pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - box_width*0.5, screen.get_height()*0.3 - 100, box_width, 200))
                question_name = question_font.render("Question " + str(question_counter) + ":", True, (255, 255, 255))
                screen.blit(question_name, (screen.get_width()*0.5 - question_name.get_width()*0.5, screen.get_height()*0.4 - 170))

                question_text_box = game_font.render(question_text, True, (255, 255, 255))
                screen.blit(question_text_box, (screen.get_width()*0.5 - question_text_box.get_width()*0.5, screen.get_height()*0.4 - 100))

                ##Draw team boxes
                pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.18 -50, screen.get_height()*0.65, 400, 150))
                pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.65 -50, screen.get_height()*0.65, 400, 150))

                team1_fontsize = 40 
                team2_fontsize = 40
                team1_font = pygame.font.SysFont(None, team1_fontsize)
                team2_font = pygame.font.SysFont(None, team2_fontsize)

                team1_name_text = team1_font.render(team_names[0], True, (255, 255, 255))
                team2_name_text = team2_font.render(team_names[1], True, (255, 255, 255))

                screen.blit(team1_name_text, (screen.get_width()*0.18 + 150 - team1_name_text.get_width()*0.5, screen.get_height()*0.65 +50 - team1_name_text.get_height()*0.85))
                screen.blit(team2_name_text, (screen.get_width()*0.65 + 150 - team2_name_text.get_width()*0.5, screen.get_height()*0.65 +50 - team2_name_text.get_height()*0.85))

                score_font = pygame.font.SysFont(None, 85)
                team1_score_text = score_font.render(str(team1.score), True, (225, 225, 225))
                team2_score_text = score_font.render(str(team2.score), True, (225, 225, 225))
                
                screen.blit(team1_score_text, (screen.get_width()*0.18 + 150 - team1_score_text.get_width()*0.5, screen.get_height()*0.65 + 75))
                screen.blit(team2_score_text, (screen.get_width()*0.65 + 150 - team2_score_text.get_width()*0.5, screen.get_height()*0.65 + 75))
       
        # 3. Update the display to show changes
        pygame.display.flip() # or pygame.display.update()




    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
