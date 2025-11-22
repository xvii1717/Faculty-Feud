import json
import os
import sys
import pygame

# Faculty Feud MVP Game
# Main game logic and UI using Pygame


DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "questions.json")  # Path to questions data

# Assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # Path to assets folder
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")  # Path to sounds folder


class Team:
    """Represents a team in the game."""
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.strikes = 0


def load_data(path=DATA_PATH):
    """Load questions and answers from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """Main entry point for the game."""
    # Initialize Pygame and mixer
    pygame.init()
    mixer_available = True
    try:
        pygame.mixer.init()
    except Exception:
        mixer_available = False  # If mixer fails, disable sound

    # Set up main window
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Faculty Feud - MVP")
    clock = pygame.time.Clock()
    ###

    
    # Load board, answer box, and strike images from assets
    board_img = None
    answer_box_img = None
    strike_img = None
    try:
        board_img = pygame.image.load(os.path.join(ASSETS_DIR, "family-feud-board.jpg")).convert()
    except Exception:
        try:
            board_img = pygame.image.load(os.path.join(ASSETS_DIR, "family-feud-board.jpg")).convert()
        except Exception:
            board_img = None
    try:
        answer_box_img = pygame.image.load(os.path.join(ASSETS_DIR, "background-for-answer-box.png")).convert_alpha()
    except Exception:
        try:
            answer_box_img = pygame.image.load(os.path.join(ASSETS_DIR, "box_0.png")).convert_alpha()
        except Exception:
            answer_box_img = None
    try:
        strike_img = pygame.image.load(os.path.join(ASSETS_DIR, "fam-feud-x.png")).convert_alpha()
    except Exception:
        strike_img = None

    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 48)

    # --- Team setup screen ---
    # Allows user to enter team names before starting
    team_names = ["", ""]
    active_input = 0
    input_font = pygame.font.SysFont(None, 64)
    setup_running = True
    while setup_running:
        for event in pygame.event.get():
            # Handle team name input events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_TAB:
                    active_input = 1 - active_input  # Switch input box
                elif event.key == pygame.K_RETURN:
                    if all(n.strip() for n in team_names):
                        setup_running = False  # Start game if both names entered
                elif event.key == pygame.K_BACKSPACE:
                    team_names[active_input] = team_names[active_input][:-1]
                else:
                    ch = event.unicode
                    if ch.isprintable():
                        team_names[active_input] += ch

        # Draw team setup UI
        screen.fill((30, 30, 60))
        title = big_font.render("Enter Team Names", True, (255, 255, 0))
        screen.blit(title, (size[0] // 2 - title.get_width() // 2, 80))
        for i in range(2):
            label = input_font.render(f"Team {i+1}: ", True, (200, 200, 255))
            name = input_font.render(team_names[i] or "_", True, (255, 255, 255) if active_input == i else (180, 180, 180))
            y = 200 + i * 120
            screen.blit(label, (size[0] // 2 - 320, y))
            screen.blit(name, (size[0] // 2 - 80, y))
        instr = font.render("Tab: Switch | Enter: Confirm | ESC: Quit", True, (220, 220, 220))
        screen.blit(instr, (size[0] // 2 - instr.get_width() // 2, 500))
        pygame.display.flip()
        clock.tick(30)

    team1 = Team(team_names[0].strip())
    team2 = Team(team_names[1].strip())

    # --- Head-to-head buzzer round ---
    # Lets teams buzz in to decide who answers first
    data = load_data()
    round_idx = 0
    round_data = data["rounds"][round_idx]
    answers = [dict(a) for a in round_data["answers"]]

    buzzer_winner = None
    buzzer_active = True
    buzzer_msg = "Press A for Team 1, L for Team 2!"
    while buzzer_active:
        for event in pygame.event.get():
            # Handle buzzer key events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_a:
                    buzzer_winner = 1
                    buzzer_active = False
                    if buzzer_sound:
                        try:
                            buzzer_sound.play()
                        except Exception:
                            pass
                elif event.key == pygame.K_l:
                    buzzer_winner = 2
                    buzzer_active = False
                    if buzzer_sound:
                        try:
                            buzzer_sound.play()
                        except Exception:
                            pass
        # Draw buzzer UI
        if board_img:
            screen.blit(pygame.transform.scale(board_img, size), (0, 0))
        else:
            screen.fill((24, 24, 24))
        title = big_font.render("Head-to-Head Buzzer!", True, (255, 255, 0))
        screen.blit(title, (size[0] // 2 - title.get_width() // 2, 120))
        instr = big_font.render(buzzer_msg, True, (220, 220, 220))
        screen.blit(instr, (size[0] // 2 - instr.get_width() // 2, 220))
        pygame.display.flip()
        clock.tick(30)

    # Winner selection screen
    # Lets host select which team won the buzzer
    active_team = None
    select_running = True
    while select_running:
        for event in pygame.event.get():
            # Handle winner selection events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_1:
                    active_team = team1
                    select_running = False
                elif event.key == pygame.K_2:
                    active_team = team2
                    select_running = False
        # Draw winner selection UI
        if board_img:
            screen.blit(pygame.transform.scale(board_img, size), (0, 0))
        else:
            screen.fill((24, 24, 24))
        title = big_font.render("Who won the buzzer?", True, (255, 255, 0))
        screen.blit(title, (size[0] // 2 - title.get_width() // 2, 120))
        instr = big_font.render(f"Press 1 for {team1.name}, 2 for {team2.name}", True, (220, 220, 220))
        screen.blit(instr, (size[0] // 2 - instr.get_width() // 2, 220))
        pygame.display.flip()
        clock.tick(30)

    # Load sounds if available
    # Used for buzzer, reveal, and wrong answer effects
    buzzer_sound = None
    reveal_sound = None
    wrong_sound = None
    if mixer_available and os.path.isdir(SOUNDS_DIR):
        def try_load(filename):
            path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(path):
                try:
                    return pygame.mixer.Sound(path)
                except Exception:
                    return None
            return None

        # Preferred candidates (fallbacks)
        buzzer_sound = try_load("family-feud-done.mp3") or try_load("family-feud-theme-main.mp3")
        reveal_sound = try_load("family-feud-good-answer.mp3") or try_load("family-feud-done.mp3")
        wrong_sound = try_load("extremely-loud-incorrect-buzzer_0cDaG20.mp3") or try_load("family-feud-bad-answer.mp3")

    def reveal_answer(i):
        """Reveal an answer and award points to active team."""
        if not answers[i]["revealed"]:
            answers[i]["revealed"] = True
            pts = answers[i].get("points", 0)
            if active_team:
                active_team.score += pts
            # play reveal/correct sound
            if 'reveal_sound' in locals() and reveal_sound:
                try:
                    reveal_sound.play()
                except Exception:
                    pass

    running = True
    while running:
        for event in pygame.event.get():
            # Handle main game events
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_a:
                    active_team = team1
                    if 'buzzer_sound' in locals() and buzzer_sound:
                        try:
                            buzzer_sound.play()
                        except Exception:
                            pass
                elif event.key == pygame.K_l:
                    active_team = team2
                    if 'buzzer_sound' in locals() and buzzer_sound:
                        try:
                            buzzer_sound.play()
                        except Exception:
                            pass
                elif event.key == pygame.K_x:
                    if active_team:
                        active_team.strikes += 1
                        if 'wrong_sound' in locals() and wrong_sound:
                            try:
                                wrong_sound.play()
                            except Exception:
                                pass
                elif event.key == pygame.K_r:
                    # Reset round reveals and scores
                    for a in answers:
                        a["revealed"] = False
                    team1.score = 0
                    team2.score = 0
                    team1.strikes = 0
                    team2.strikes = 0

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Check if an answer box was clicked
                left = 100
                top = 180
                w = 600
                h = 60
                gap = 10
                for i, a in enumerate(answers):
                    rect = pygame.Rect(left, top + i * (h + gap), w, h)
                    if rect.collidepoint(mx, my):
                        reveal_answer(i)

        # Draw board background
        if board_img:
            screen.blit(pygame.transform.scale(board_img, size), (0, 0))
        else:
            screen.fill((24, 24, 24))

        # Draw header: question
        qsurf = big_font.render(round_data["question"], True, (240, 240, 240))
        screen.blit(qsurf, (100, 80))

        # Draw answers as boxes (hidden or revealed)
        left = 100
        top = 180
        w = 600
        h = 60
        gap = 10
        for i, a in enumerate(answers):
            rect = pygame.Rect(left, top + i * (h + gap), w, h)
            if answer_box_img:
                ab_img = pygame.transform.scale(answer_box_img, (w, h))
                screen.blit(ab_img, rect.topleft)
            else:
                color = (60, 60, 60) if not a.get("revealed") else (20, 120, 20)
                pygame.draw.rect(screen, color, rect, border_radius=6)
            if a.get("revealed"):
                text = f"{a.get('text')} — {a.get('points')}"
            else:
                text = "(hidden)"
            tsurf = font.render(text, True, (240, 240, 240))
            screen.blit(tsurf, (rect.x + 12, rect.y + (h - tsurf.get_height()) // 2))

        # Draw team panels
        def draw_team(team, x):
            # Draw team info and strikes
            pygame.draw.rect(screen, (40, 40, 80), (x, 80, 420, 80), border_radius=6)
            name = big_font.render(team.name, True, (240, 240, 240))
            score = big_font.render(str(team.score), True, (240, 240, 240))
            screen.blit(name, (x + 12, 86))
            screen.blit(score, (x + 12, 130))
            # Draw strikes visually
            for s in range(team.strikes):
                if strike_img:
                    sx = x + 300 + s * 50
                    sy = 130
                    simg = pygame.transform.scale(strike_img, (40, 40))
                    screen.blit(simg, (sx, sy))
                else:
                    strikes = font.render("X", True, (220, 180, 180))
                    screen.blit(strikes, (x + 300 + s * 30, 130))

        draw_team(team1, 760)
        draw_team(team2, 760)

        # Active team indicator and instructions
        if active_team:
            at = font.render(f"Active: {active_team.name}", True, (240, 240, 0))
            screen.blit(at, (100, 40))
        instr = [
            "Controls:",
            "A = Team A buzz | L = Team B buzz | Click answers to reveal (adds points)",
            "X = give active team a strike | R = reset round | ESC = quit"
        ]
        for i, s in enumerate(instr):
            screen.blit(font.render(s, True, (200, 200, 200)), (100, 620 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
