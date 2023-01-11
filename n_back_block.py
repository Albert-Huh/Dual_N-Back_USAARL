import pygame
import random
import time
import os
import textwrap

class Game(object):
    def __init__(self):
        # settings
        self.corner_radius = 0
        self.board_size = (600, 600)
        self.cell_size = (200,200)
        self.board_color = (5,5,5)
        self.cell_color = (255,255,255)
        self.results = {}
        self.positions = {i+1: (self.corner_radius + 200*(i % 3),
                                self.corner_radius + 200*(int(i/3)))
                            for i in range(9)}

    def start(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 2000)
        pygame.font.init()

# TODO implement full screen mode
# TODO randomize 12 n blocks (0,1,2) (4 each) for complete session

class N_Back(object):
    def __init__(self, n=0):
        self.n = n
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.screen = pygame.display.set_mode(self.game.board_size, pygame.RESIZABLE)
        self.screen.fill(self.game.board_color)
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Arial', 100)
        self.myfont2 = pygame.font.SysFont('Arial', 30)
        self.myfont3 = pygame.font.SysFont('Arial', 30)
        self.myfont4 = pygame.font.SysFont('Arial', 60)

        self.current = 0
        self.num = 0
        self.pos_seq = []
        self.alpha_seq = []
        self.answer_alpha = []
        self.answer_pos = []
        if self.n >= 1:
            self.plan_sequence()
        self.input_alpha = ["" for _ in range(20)]
        self.input_pos = ["" for _ in range(20)]
        self.results = {
            "correct": 0,
            "missed": 0,
            "false": 0,
        }
        self.path_good = os.path.join(os.getcwd(),"Dual_N-Back_Test", "good.mp3")
        self.path_bad = os.path.join(os.getcwd(),"Dual_N-Back_Test", "bad.mp3")

    def plan_sequence(self):
        alphabets = list(range(0, 26))
        for _ in range(self.n):
            pos = random.randint(1,9)
            alpha = random.randint(0,25)
            self.pos_seq.append(pos)
            self.alpha_seq.append(alpha)

        for i in range(self.n,20):
            target_prob = random.randint(15,25)
            alpha_probs = [(100-target_prob)/25 for _ in range(26)]
            alpha_probs[self.alpha_seq[i-self.n]] = target_prob
            next_alpha = random.choices(alphabets, alpha_probs, k=1)
            self.alpha_seq.append(next_alpha[0])
            self.pos_seq.append(random.randint(1,9))

        for _ in range(self.n):
            self.answer_pos.append(False)
            self.answer_alpha.append(False)

        for i in range(self.n, len(self.alpha_seq)):
            if self.pos_seq[i] == self.pos_seq[i-self.n]:
                self.answer_pos.append(True)
            else:
                self.answer_pos.append(False)

            if self.alpha_seq[i] == self.alpha_seq[i-self.n]:
                self.answer_alpha.append(True)
            else:
                self.answer_alpha.append(False)

    def zeroBack(self):
        self.target_alpha = random.randint(0,25)
        print(self.target_alpha)
        self.target_pos = random.randint(1,9)
        alphabets = list(range(0, 26))

        for i in range(20):
            target_prob = random.randint(15,25)
            alpha_probs = [(100-target_prob)/25 for _ in range(26)]
            alpha_probs[self.target_alpha] = target_prob
            next_alpha = random.choices(alphabets, alpha_probs, k=1)
            next_pos = random.randint(1,9)
            self.alpha_seq.append(next_alpha[0])
            self.pos_seq.append(next_pos)
            if next_alpha[0] == self.target_alpha:
                self.answer_alpha.append(True)
            else:
                self.answer_alpha.append(False)
            if next_pos == self.target_pos:
                self.answer_pos.append(True)
            else:
                self.answer_pos.append(False)
        print(self.alpha_seq)
        print(self.answer_alpha)
        print(self.pos_seq)
        print(self.answer_pos)

        start_time = time.time()
        instruction_time = time.time()
        # instructions
        self.game.start()

        xpos, ypos = self.game.positions[self.target_pos]
        pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(xpos, ypos, self.game.cell_size[0],
                                                                        self.game.cell_size[1]), self.game.corner_radius)

        title = self.myfont4.render('Instructions', True, (255, 255, 255))
        self.screen.blit(title, (125, 0))
        pygame.event.get()
        description = "If you see '" + str(chr(self.target_alpha + 65)) + "', you leftclick with the mouse. If you see " \
            "the square in the location indicated in this page, you rightclick with the mouse. If correct, you will hear 'good'. " \
            "If you missed or your response is incorrect, you will hear 'bad'."
        self.displayText(description, 'Arial', (255, 255, 255), 40, 45, 100)
        pygame.display.flip()

        i = 0
        while i < 10:
            pygame.event.get()
            self.clock.tick(1)
            i += 1

        self.screen.fill(self.game.board_color)
        print("Instruction: " + str(time.time() - instruction_time))
        start = time.time()

        # generate alphabets
        idx = 0
        while idx < 20:
            self.respond(idx)
            self.generate(idx)
            idx += 1

        for i in range(len(self.input_alpha)):
            if self.input_alpha[i] == "":
                self.input_alpha[i] = False
            if self.input_pos[i] == "":
                self.input_pos[i] = False
        print(self.input_alpha)
        print(self.input_pos)
        print("Stimuli:" + str(time.time() - start) + " seconds")

        # stabilization
        stab_time = time.time()
        self.screen.fill(self.game.board_color)
        pygame.display.flip()
        self.calculate_results()
        self.clock.tick(1 / 5)
        print("Stabilization: " + str(time.time() - stab_time))

        # results
        results_time = time.time()
        text = self.myfont.render('Results:', False, (255, 255, 255))
        self.screen.blit(text, (150, 0))
        correct = self.myfont2.render('Correct: ' + str(self.results["correct"]), False, (255, 255, 255))
        self.screen.blit(correct, (0, 100))
        missed = self.myfont2.render('Missed: ' + str(self.results["missed"]), False, (255, 255, 255))
        self.screen.blit(missed, (0, 200))
        false = self.myfont2.render('False Alarm: ' + str(self.results["false"]), False, (255, 255, 255))
        self.screen.blit(false, (0, 300))

        pygame.display.flip()
        self.clock.tick(1 / 5)

        print("Results: " + str(time.time() - results_time))
        print("Overall: " + str(time.time() - start_time))



    def run(self):
        pygame.event.get()
        if self.n == 0:
            self.zeroBack()
            return
        print(self.alpha_seq)
        print(self.answer_alpha)
        print(self.pos_seq)
        print(self.answer_pos)
        start_time = time.time()
        instruction_time = time.time()
        # instructions
        self.game.start()
        title = self.myfont4.render('Instructions', True, (255,255,255))
        self.screen.blit(title, (125,0))
        pygame.event.get()
        description = "If you saw the same letter N trials ago, you leftclick with the mouse. If you saw the same " \
                      "location N trials ago, you rightclick with the mouse. If correct, you will hear 'good'. If you " \
                      "missed or your response is incorrect, you will hear 'bad'."
        self.displayText(description, 'Arial', (255,255,255), 30, 45, 100)
        pygame.display.flip()
        i = 0
        while i < 100:
            pygame.event.get()
            self.clock.tick(10)
            i+=1

        self.screen.fill(self.game.board_color)
        print("Instruction: " + str(time.time()-instruction_time))
        start = time.time()

        # generate alphabets
        idx = 0
        while idx < 20:
            self.respond(idx)
            self.generate(idx)
            idx += 1

        for i in range(len(self.input_alpha)):
            if self.input_alpha[i] == "":
                self.input_alpha[i] = False
            if self.input_pos[i] == "":
                self.input_pos[i] = False
        print(self.input_alpha)
        print(self.input_pos)
        print("Stimuli:" + str(time.time() - start) + " seconds")

        # stabilization
        stab_time = time.time()
        self.screen.fill(self.game.board_color)
        pygame.display.flip()
        self.calculate_results()
        self.clock.tick(1/5)
        print("Stabilization: " + str(time.time()-stab_time))

        # results
        results_time = time.time()
        text = self.myfont.render('Results:', False, (255, 255, 255))
        self.screen.blit(text, (150, 0))
        correct = self.myfont2.render('Correct: ' + str(self.results["correct"]), False, (255, 255, 255))
        self.screen.blit(correct, (0, 100))
        missed = self.myfont2.render('Missed: ' + str(self.results["missed"]), False, (255, 255, 255))
        self.screen.blit(missed, (0, 200))
        false = self.myfont2.render('False Alarm: ' + str(self.results["false"]), False, (255, 255, 255))
        self.screen.blit(false, (0, 300))

        pygame.display.flip()
        self.clock.tick(1/5)

        print("Results: " + str(time.time() - results_time))
        print("Overall: " + str(time.time() - start_time))

    def displayText(self, text, font_name, color, size, posx, posy):
        myfont = pygame.font.SysFont(font_name, size)
        numtext = self.game.board_size[0] // size * 2
        lines = textwrap.wrap(text, numtext)
        for idx, line in enumerate(lines):
            display = myfont.render(line, False, color)
            self.screen.blit(display, (posx, posy + (idx * size)))

    def generate(self,i):
        self.num = random.randint(1,9)
        xpos, ypos = self.game.positions[self.pos_seq[i]]

        pygame.draw.rect(self.screen, self.game.cell_color, pygame.Rect(xpos,
                                                  ypos, self.game.cell_size[0],
                                                  self.game.cell_size[1]), self.game.corner_radius)
        text = self.myfont.render(str(chr(self.alpha_seq[i]+65)), True, (0, 0, 0))
        text_rect = text.get_rect(center=(xpos+self.game.board_size[0]//6, ypos+self.game.board_size[1]//6))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        self.clock.tick(1/0.6)
        self.respond(i)

        self.screen.fill(self.game.board_color)
        pygame.display.flip()
        self.clock.tick(1/1.4)
        self.respond(i)
        if (self.answer_alpha[i] and self.input_alpha[i] == "") or (self.answer_pos[i] and self.input_pos[i] == ""):
            pygame.mixer.music.load(self.path_bad)
            pygame.mixer.music.play()

    def respond(self,i):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.input_alpha[i] = True
                    if self.answer_alpha[i]:
                        pygame.mixer.music.load(self.path_good)
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(self.path_bad)
                        pygame.mixer.music.play()

                elif event.button == 3:
                    self.input_pos[i] = True
                    if self.answer_pos[i]:
                        pygame.mixer.music.load(self.path_good)
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(self.path_bad)
                        pygame.mixer.music.play()

    def calculate_results(self):
        for i in range(len(self.answer_alpha)):
            if self.answer_alpha[i] and self.input_alpha[i]:
                self.results["correct"] += 1
            elif self.answer_alpha[i] and self.input_alpha[i] == False:
                self.results["missed"] += 1
            elif self.answer_alpha[i] == False and self.input_alpha[i]:
                self.results["false"] += 1

            if self.answer_pos[i] and self.input_pos[i]:
                self.results["correct"] += 1
            elif self.answer_pos[i] and self.input_pos[i] == False:
                self.results["missed"] += 1
            elif self.answer_pos[i] == False and self.input_pos[i]:
                self.results["false"] += 1

