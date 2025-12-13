import json
import os
import sys
import shutil
import pygame

# Always use a user-writable location for questions.json
def get_writable_questions_path():
    data_dir = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "questions.json")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# On first run, copy bundled questions.json to writable location if not present
def ensure_questions_json():
    writable_path = get_writable_questions_path()
    if not os.path.exists(writable_path):
        bundled_path = resource_path(os.path.join("data", "questions.json"))
        if os.path.exists(bundled_path):
            shutil.copy(bundled_path, writable_path)
        else:
            with open(writable_path, 'w') as f:
                json.dump({"rounds": []}, f, indent=4)
    return writable_path

DATA_PATH = ensure_questions_json()
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # Path to assets folder
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sounds")  # Path to assets folder

class Team:
    """Represents a team in the game."""
    def __init__(self, name):
        self.name = name
        self.score = 0
def manual_score_screen(screen, team1, team2, font, input_font):
    """Display a visually centered and appealing screen to manually edit team scores (with typing support)."""
    editing = True
    active_input = None  # None, "team1", or "team2"
    input_text = {"team1": str(team1.score), "team2": str(team2.score)}
    W, H = screen.get_size()
    panel_w, panel_h = 320, 320
    panel_y = H // 2 - panel_h // 2
    gap = 80
    panel1_x = W // 2 - panel_w - gap // 2
    panel2_x = W // 2 + gap // 2

    while editing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    editing = False
                elif active_input:
                    if event.key == pygame.K_RETURN:
                        try:
                            val = int(input_text[active_input])
                            if val < 0: val = 0
                            if active_input == "team1":
                                team1.score = val
                            else:
                                team2.score = val
                        except ValueError:
                            pass
                        active_input = None
                    elif event.key == pygame.K_BACKSPACE:
                        input_text[active_input] = input_text[active_input][:-1]
                    elif event.unicode.isdigit():
                        input_text[active_input] += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Team 1 +/-
                if panel1_x + 30 <= mx <= panel1_x + 90 and panel_y + 220 <= my <= panel_y + 280:
                    team1.score += 1
                    input_text["team1"] = str(team1.score)
                if panel1_x + 230 <= mx <= panel1_x + 290 and panel_y + 220 <= my <= panel_y + 280 and team1.score > 0:
                    team1.score -= 1
                    input_text["team1"] = str(team1.score)
                # Team 2 +/-
                if panel2_x + 30 <= mx <= panel2_x + 90 and panel_y + 220 <= my <= panel_y + 280:
                    team2.score += 1
                    input_text["team2"] = str(team2.score)
                if panel2_x + 230 <= mx <= panel2_x + 290 and panel_y + 220 <= my <= panel_y + 280 and team2.score > 0:
                    team2.score -= 1
                    input_text["team2"] = str(team2.score)
                # Click on score to type
                if panel1_x + 110 <= mx <= panel1_x + 210 and panel_y + 120 <= my <= panel_y + 200:
                    active_input = "team1"
                    input_text["team1"] = ""
                if panel2_x + 110 <= mx <= panel2_x + 210 and panel_y + 120 <= my <= panel_y + 200:
                    active_input = "team2"
                    input_text["team2"] = ""
                # Done button
                done_rect = pygame.Rect(W//2 - 100, panel_y + panel_h + 40, 200, 60)
                if done_rect.collidepoint(mx, my):
                    editing = False

        screen.fill((40, 60, 120))

        # Title
        title = input_font.render("Edit Team Scores", True, (255,255,255))
        screen.blit(title, (W//2 - title.get_width()//2, panel_y - 70))

        # Team 1 Panel
        pygame.draw.rect(screen, (65,105,245), (panel1_x, panel_y, panel_w, panel_h), border_radius=30)
        t1_name = font.render(team1.name, True, (255,255,255))
        screen.blit(t1_name, (panel1_x + panel_w//2 - t1_name.get_width()//2, panel_y + 30))
        # Score input box
        score_box1 = pygame.Rect(panel1_x + 110, panel_y + 120, 100, 80)
        pygame.draw.rect(screen, (255,255,255) if active_input=="team1" else (220,220,220), score_box1, border_radius=15)
        t1_score = input_font.render(input_text["team1"] if active_input=="team1" else str(team1.score), True, (40,40,40))
        screen.blit(t1_score, (score_box1.x + score_box1.width//2 - t1_score.get_width()//2, score_box1.y + score_box1.height//2 - t1_score.get_height()//2))
        # +/-
        plus_rect1 = pygame.Rect(panel1_x + 30, panel_y + 220, 60, 60)
        minus_rect1 = pygame.Rect(panel1_x + 230, panel_y + 220, 60, 60)
        pygame.draw.rect(screen, (0,200,0), plus_rect1, border_radius=15)
        pygame.draw.rect(screen, (200,0,0), minus_rect1, border_radius=15)
        plus = font.render("+", True, (255,255,255))
        minus = font.render("-", True, (255,255,255))
        screen.blit(plus, (plus_rect1.x + plus_rect1.width//2 - plus.get_width()//2, plus_rect1.y + plus_rect1.height//2 - plus.get_height()//2))
        screen.blit(minus, (minus_rect1.x + minus_rect1.width//2 - minus.get_width()//2, minus_rect1.y + minus_rect1.height//2 - minus.get_height()//2))

        # Team 2 Panel
        pygame.draw.rect(screen, (65,105,245), (panel2_x, panel_y, panel_w, panel_h), border_radius=30)
        t2_name = font.render(team2.name, True, (255,255,255))
        screen.blit(t2_name, (panel2_x + panel_w//2 - t2_name.get_width()//2, panel_y + 30))
        # Score input box
        score_box2 = pygame.Rect(panel2_x + 110, panel_y + 120, 100, 80)
        pygame.draw.rect(screen, (255,255,255) if active_input=="team2" else (220,220,220), score_box2, border_radius=15)
        t2_score = input_font.render(input_text["team2"] if active_input=="team2" else str(team2.score), True, (40,40,40))
        screen.blit(t2_score, (score_box2.x + score_box2.width//2 - t2_score.get_width()//2, score_box2.y + score_box2.height//2 - t2_score.get_height()//2))
        # +/-
        plus_rect2 = pygame.Rect(panel2_x + 30, panel_y + 220, 60, 60)
        minus_rect2 = pygame.Rect(panel2_x + 230, panel_y + 220, 60, 60)
        pygame.draw.rect(screen, (0,200,0), plus_rect2, border_radius=15)
        pygame.draw.rect(screen, (200,0,0), minus_rect2, border_radius=15)
        screen.blit(plus, (plus_rect2.x + plus_rect2.width//2 - plus.get_width()//2, plus_rect2.y + plus_rect2.height//2 - plus.get_height()//2))
        screen.blit(minus, (minus_rect2.x + minus_rect2.width//2 - minus.get_width()//2, minus_rect2.y + minus_rect2.height//2 - minus.get_height()//2))

        # Done button
        done_rect = pygame.Rect(W//2 - 100, panel_y + panel_h + 40, 200, 60)
        pygame.draw.rect(screen, (100,180,255), done_rect, border_radius=20)
        done = font.render("Done", True, (255,255,255))
        screen.blit(done, (done_rect.x + done_rect.width//2 - done.get_width()//2, done_rect.y + done_rect.height//2 - done.get_height()//2))

        # Instructions
        instr = font.render("ESC or Done to return | Click score to type", True, (255,255,255))
        screen.blit(instr, (W//2 - instr.get_width()//2, done_rect.y + done_rect.height + 20))

        pygame.display.flip()
        pygame.time.Clock().tick(30)






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
    board_image = pygame.image.load(os.path.join(ASSETS_DIR, "family-feud-board.jpg")).convert()
    board_image = pygame.transform.smoothscale(board_image, (screen.get_width(), screen.get_height()))
    blank_box = pygame.image.load(os.path.join(ASSETS_DIR, "box_0.png")).convert()
    blank_box = pygame.transform.smoothscale(blank_box, (540, 153))

    ##Cover boxes
    box_one = pygame.image.load(os.path.join(ASSETS_DIR, "box_1.png")).convert()
    box_one = pygame.transform.smoothscale(box_one, (540, 153))
    box_two = pygame.image.load(os.path.join(ASSETS_DIR, "box_2.png")).convert()
    box_two = pygame.transform.smoothscale(box_two, (540, 153))
    box_three = pygame.image.load(os.path.join(ASSETS_DIR, "box_3.png")).convert()
    box_three = pygame.transform.smoothscale(box_three, (540, 153))
    box_four = pygame.image.load(os.path.join(ASSETS_DIR, "box_4.png")).convert()
    box_four = pygame.transform.smoothscale(box_four, (540, 153))
    box_five = pygame.image.load(os.path.join(ASSETS_DIR, "box_5.png")).convert()
    box_five = pygame.transform.smoothscale(box_five, (540, 153))
    box_six = pygame.image.load(os.path.join(ASSETS_DIR, "box_6.png")).convert()
    box_six = pygame.transform.smoothscale(box_six, (540, 153))
    box_seven = pygame.image.load(os.path.join(ASSETS_DIR, "box_7.png")).convert()
    box_seven = pygame.transform.smoothscale(box_seven, (540, 153))
    box_eight = pygame.image.load(os.path.join(ASSETS_DIR, "box_8.png")).convert()
    box_eight = pygame.transform.smoothscale(box_eight, (540, 153))

    x_box = pygame.image.load(os.path.join(ASSETS_DIR, "fam-feud-x.png")).convert_alpha()
    x_box = pygame.transform.smoothscale(x_box, (540, 400))

    end_screen = pygame.image.load(os.path.join(ASSETS_DIR, "happy_steve.jpg")).convert()
    end_screen = pygame.transform.smoothscale(end_screen, (screen.get_width(), screen.get_height()))
    

    round_points = 0
    
    theme_audio = os.path.join(SOUNDS_DIR, "family-feud-theme-main.mp3")
    
    game_font = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None, 28)
    input_font = pygame.font.SysFont(None, 64)
    question_font = pygame.font.SysFont(None, 84)
    point_font = pygame.font.SysFont(None, 200)


    size = screen.get_size()
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    question_counter = 1
    activeTeam = 0
    screencounter = 0
    
    ##for typing names on intro screen
    active_input = 0
    steal = False
    wrongs = 0
    sinceWrong = 100
    correctcounter = 0
    ##list of team names
    team_names = ["", ""]
    running = True 
    edit = False
    manual_rect = pygame.Rect(screen.get_width() - 300, 0, 300, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if manual_rect.collidepoint(mx, my):
                    # Example: switch to manual editing screen
                    edit = True

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and screencounter == 0:
                screencounter+=1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if screencounter != 1000:
                    screencounter = 1000
                else:
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
            elif screencounter > 1 and  screencounter % 2 == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                screencounter += 1
                activeTeam = 1
                round_points = 0
                wrongs = 0
            elif screencounter > 1 and  screencounter % 2 == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                screencounter += 1
                activeTeam = 0
                wrongs = 0
                round_points = 0
            elif screencounter > 1 and screencounter % 2 == 1:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and steal == False:
                    mx, my = event.pos
                    round = data["rounds"][question_counter - 1]
                    num_answers = len(round["answers"])
                    for i in range(num_answers):
                        # Calculate box position
                        if i < 4:
                            x = screen.get_width()*0.2 - 10
                            y = 290 + i*172
                        else:
                            g = i - 4
                            x = screen.get_width()*0.515
                            y = 290 + g*172
                        w, h = 540, 153
                        if x <= mx <= x + w and y <= my <= y + h:
                            if(not round["answers"][i]["revealed"]):   
                                round["answers"][i]["revealed"] = True
                                correctDing()
                                round_points += round["answers"][i]["points"] * (1 if "multiplier" not in round else round["multiplier"])
                                correctcounter += 1
                                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and steal == True:
                    mx, my = event.pos
                    round = data["rounds"][question_counter - 1]
                    num_answers = len(round["answers"])
                    for i in range(num_answers):
                        # Calculate box position
                        if i < 4:
                            x = screen.get_width()*0.2 - 10
                            y = 290 + i*172
                        else:
                            g = i - 4
                            x = screen.get_width()*0.515
                            y = 290 + g*172
                        w, h = 540, 153
                        if x <= mx <= x + w and y <= my <= y + h:
                            if(not round["answers"][i]["revealed"]):   
                                round["answers"][i]["revealed"] = True
                                correctDing()  
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_x and correctcounter < len(data["rounds"][question_counter - 1]["answers"]):
                    wrongs += 1
                    if wrongs >= 3:
                        steal = True
                    if wrongs == 3 or wrongs == 4:
                        activeTeam = 1 - activeTeam
                    if(wrongs < 5):
                        wrongBuzzer()
                        sinceWrong = 0
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if steal == True or wrongs == 3 or correctcounter == len(data["rounds"][question_counter - 1]["answers"]):    
                        team1.score += round_points if activeTeam == 0 else 0
                        team2.score += round_points if activeTeam == 1 else 0
                        if(question_counter >= len(data["rounds"])):
                            screencounter = 1000
                        else: 
                            question_counter += 1
                            round_points = 0
                            screencounter += 1
                            correctcounter = 0
                            steal = False
                        
                    


        
        pygame.display.flip()
        clock.tick(60)


    
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

            ###Box to manually fix points
            


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
            if(edit == True):
                manual_score_screen(screen, team1, team2, game_font, input_font)
                edit = False
            elif screencounter == 1000:   
                screen.fill((0, 0, 0)) 
                screen.blit(end_screen, (0, 0))
                end_text = question_font.render("Game Over!", True, (255, 255, 255))
                screen.blit(end_text, (screen.get_width()*0.5 - end_text.get_width()*0.5, screen.get_height()*0.6))
                
                if team1.score > team2.score:
                    winner_text = question_font.render(f"{team1.name} Wins!", True, (255, 255, 255))
                elif team2.score > team1.score:
                    winner_text = question_font.render(f"{team2.name} Wins!", True, (255, 255, 255))
                else:
                    winner_text = question_font.render("It's a Tie!", True, (255, 255, 255))
                
                screen.blit(winner_text, (screen.get_width()*0.5 - winner_text.get_width()*0.5, screen.get_height()*0.7))
                
                final_score_text = question_font.render(f"Final Scores - {team1.name}: {team1.score} | {team2.name}: {team2.score}", True, (255, 255, 255))
                screen.blit(final_score_text, (screen.get_width()*0.5 - final_score_text.get_width()*0.5, screen.get_height()*0.8))
                
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(theme_audio)
                    pygame.mixer.music.play()
            
            elif(screencounter % 2 == 0):
                screen.fill((0, 0, 0)) 
                screen.blit(stage_image, (0, 0))
                round = data["rounds"][question_counter - 1]
                question_text = round["question"]

                box_width = (len(question_text) * 20)


                pygame.draw.rect(screen, (255, 255, 255), manual_rect)
                manual_edit = input_font.render("Edit Points", True, (65,105,245))
                screen.blit(manual_edit, (manual_rect.x + 30, manual_rect.y + 30))

                    
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

                ##Go to next screen
                
            else:
                ## Playing screen (with the eight boxes)
                screen.fill((0, 0, 0)) 
                screen.blit(board_image, (0, 0))
                
                
                pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - 435*0.5, 0, 435, 250))
                points_display = point_font.render(str(round_points), True, (255, 255, 255))
                screen.blit(points_display, (screen.get_width()*0.5 - points_display.get_width()*0.5, screen.get_height()*0.07))
                
                ## left: 0.2 -10  right: 0.515
                num_answers = len(round["answers"])
                

                multiplier = round.get("multiplier", 1)

                if multiplier == 1:
                    color = (255, 255, 255)
                elif multiplier == 2:
                    color = (255, 230, 0)
                elif multiplier == 3:
                    color = (255, 140, 0)
                else:
                    color = (220, 0, 0)
                # Draw circle in top right
                circle_radius = 60
                circle_x = screen.get_width() - circle_radius - 40
                circle_y = 40 + circle_radius
                pygame.draw.circle(screen, color, (circle_x, circle_y), circle_radius)
                # Draw multiplier text
                mult_text = f"x{multiplier}"
                mult_font = pygame.font.SysFont(None, 64)
                text_surf = mult_font.render(mult_text, True, (0, 0, 0) if multiplier != 1 else (40, 40, 40))
                screen.blit(
                    text_surf,
                    (circle_x - text_surf.get_width() // 2, circle_y - text_surf.get_height() // 2)
                )



                ##Make boxes with answers
                for i in range(num_answers):
                    answer_text = round["answers"][i]["text"]
                    score_text = str(round["answers"][i]["points"])
                    answer_display = game_font.render(answer_text, True, (255, 255, 255))
                    score_display = input_font.render(score_text, True, (255, 255, 255))
                    if i < 4:
                        pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - 435*0.5, 0, 160, 40))
                        screen.blit(blank_box, (screen.get_width()*0.2 - 10, 290 + i*172))
                        
                        screen.blit(answer_display, (screen.get_width()*0.22, 340 + i*172))
                        screen.blit(score_display, (screen.get_width()*0.45, 340 + i*172))
                    else:
                        g = i - 4
                        pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - 435*0.5, 0, 160, 40))
                        screen.blit(blank_box, (screen.get_width()*0.515, 290 + g*172))
                        
                        screen.blit(answer_display, (screen.get_width()*0.545, 340 + g*172))
                        screen.blit(score_display, (screen.get_width()*0.77, 340 + g*172))


                for i in range(num_answers):
                    number_box = blank_box
                    match i:
                            case 0: number_box = box_one
                            case 1: number_box = box_two    
                            case 2: number_box = box_three
                            case 3: number_box = box_four
                            case 4: number_box = box_five
                            case 5: number_box = box_six
                            case 6: number_box = box_seven
                            case 7: number_box = box_eight
                    if not round["answers"][i]["revealed"]:
                        if i < 4:
                            pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - 435*0.5, 0, 160, 40))
                            screen.blit(number_box, (screen.get_width()*0.2 - 10, 290 + i*172))
                            
                        else:
                            g = i - 4
                            pygame.draw.rect(screen, (65,105,245), (screen.get_width()*0.5 - 435*0.5, 0, 160, 40))
                            screen.blit(number_box, (screen.get_width()*0.515, 290 + g*172))  

                pygame.draw.rect(screen, (65,105,245), (0, 0,400 + len(team_names[activeTeam])*13,100 ))
                active_team_display = game_font.render("Active Team: " + team_names[activeTeam], True, (255, 255, 255))
                screen.blit(active_team_display, (20, 35))

                ##Display Xs when wrong
                if(sinceWrong < 80):    
                    if(wrongs == 1):
                        screen.blit(x_box, (screen.get_width()*0.5 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                    elif(wrongs == 2):
                        screen.blit(x_box, (screen.get_width()*0.4 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                        screen.blit(x_box, (screen.get_width()*0.6 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                    elif(wrongs == 3):
                        screen.blit(x_box, (screen.get_width()*0.3 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                        screen.blit(x_box, (screen.get_width()*0.5 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                        screen.blit(x_box, (screen.get_width()*0.7 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))
                    else:
                        screen.blit(x_box, (screen.get_width()*0.5 - x_box.get_width()*0.5, screen.get_height()*0.5 - x_box.get_height()*0.5))   

                    sinceWrong += 1
        

def correctDing():
    correct_audio = os.path.join(SOUNDS_DIR,"family-feud-good-answer.mp3")
    pygame.mixer.music.load(correct_audio)
    pygame.mixer.music.play()

def wrongBuzzer():
    wrong_audio = os.path.join(SOUNDS_DIR,"family-feud-bad-answer.mp3")
    pygame.mixer.music.load(wrong_audio)
    pygame.mixer.music.play()




    


if __name__ == "__main__":
    main()
