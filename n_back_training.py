import pygame
import random
import time
import os
import textwrap
from datetime import datetime

class Game(object):
    def __init__(self):
        # settings
        self.corner_radius = 0
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.border = 100
        self.lborder = (self.monitor_size[0] - self.monitor_size[1]) // 2 + self.border
        self.cell_size = ((self.monitor_size[1]-2*self.border)//3,(self.monitor_size[1]-2*self.border)//3)
        self.board_color = (5,5,5)
        self.cell_color = (255,255,255)
        self.results = {}
        self.positions = {i+1: (self.corner_radius + self.lborder + (self.cell_size[0]) * (i % 3),
                                self.corner_radius + self.border + (self.cell_size[1])*(int(i/3)))
                            for i in range(9)}

    def start(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 2000)
        pygame.font.init()
        pygame.init()


class N_Back(object):
    def __init__(self, filename, filename2, n=0):
        self.n = n
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.game.start()
        self.filename = filename
        self.filename2 = filename2

        self.screen = pygame.display.set_mode(self.game.monitor_size, pygame.FULLSCREEN)
        self.screen.fill(self.game.board_color)
        self.clock = pygame.time.Clock()
        self.myfont = pygame.font.SysFont('Arial', 100)
        self.myfont2 = pygame.font.SysFont('Arial', 30)
        self.myfont3 = pygame.font.SysFont('Arial', 45)
        self.myfont4 = pygame.font.SysFont('Arial', 60)

        self.current = 0
        self.num = 0
        self.pos_seq = []
        self.alpha_seq = []
        self.answer_alpha = []
        self.answer_pos = []
        self.response_time_alpha = [0 for _ in range(20)]
        self.response_time_pos = [0 for _ in range(20)]
        if self.n >= 1:
            self.plan_sequence()
        else:
            self.zeroBack()
        self.input_alpha = ["" for _ in range(20)]
        self.input_pos = ["" for _ in range(20)]
        self.results = {
            "correct": 0,
            "missed": 0,
            "false": 0,
            "rate": 0.0
        }
        self.path_good = os.path.join(os.getcwd(), "good.mp3")
        self.path_bad = os.path.join(os.getcwd(), "bad.mp3")

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

    def run(self):
        pygame.event.get()
        print(self.alpha_seq)
        print(self.answer_alpha)
        print(self.pos_seq)
        print(self.answer_pos)
        self.filename.write("Alpha Sequence " + str(self.alpha_seq) + "\n")
        self.filename.write("Alpha Answer " + str(self.answer_alpha) + "\n")
        self.filename.write("Position Sequence " + str(self.pos_seq) + "\n")
        self.filename.write("Position Answer " + str(self.answer_pos) + "\n")

        start_time = time.time()
        instruction_time = time.time()

        # instructions
        title = self.myfont4.render("{}-Back".format(self.n), True, (255,255,255))
        title_rect = title.get_rect(center=(self.game.monitor_size[0] / 2, self.game.monitor_size[1] / 2))
        self.screen.blit(title, title_rect)

        if self.n == 0:
            xpos, ypos = self.game.positions[self.target_pos]
            pygame.draw.rect(self.screen, (255,0,0), (xpos, ypos, self.game.cell_size[0], self.game.cell_size[1]), 2)
            text_right = self.myfont3.render("Right Click: Location [Target: Displyed location]", True, (255,255,255))
            text_r_rect = text_right.get_rect(center=(self.game.monitor_size[0] / 2, self.game.monitor_size[1] / 2 + 60))
            self.screen.blit(text_right, text_r_rect)
            
            text_left = self.myfont3.render("Left Click: Alphabet [Target: "+chr(self.target_alpha+65)+"]", True, (255,255,255))
            text_l_rect = text_left.get_rect(center=(self.game.monitor_size[0] / 2, self.game.monitor_size[1] / 2 + 105))
            self.screen.blit(text_left, text_l_rect)

        else:
            text_right = self.myfont3.render("Right Click: Location", True, (255,255,255))
            text_r_rect = text_right.get_rect(center=(self.game.monitor_size[0] / 2, self.game.monitor_size[1] / 2 + 60))
            self.screen.blit(text_right, text_r_rect)

            text_left = self.myfont3.render("Left Click: Alphabet", True, (255,255,255))
            text_l_rect = text_left.get_rect(center=(self.game.monitor_size[0] / 2, self.game.monitor_size[1] / 2 + 105))
            self.screen.blit(text_left, text_l_rect)

        pygame.event.get()

        pygame.display.flip()
        i = 0
        while i < 50:
            pygame.event.get()
            self.clock.tick(10)
            i+=1

        self.screen.fill(self.game.board_color)
        print("Instruction: " + str(time.time()-instruction_time))
        self.filename.write("Instruction:  " + str(time.time()-instruction_time) + "\n")
        start = time.time()
        self.filename.write("Timestamp before stimuli: " + str(datetime.now().time()) + "\n")

        # fixation 1
        self.fixation(5)

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
        self.filename.write("User Input Alpha: " + str(self.input_alpha) + "\n")
        self.filename.write("User Input Position: " + str(self.input_pos) + "\n")

        print("Stimuli:" + str(time.time() - start) + " seconds")
        self.filename.write("Stimuli " + str(time.time() - start) + " seconds" + "\n")

        # fixation 2
        self.fixation(5)

        self.calculate_results()
        self.writeResults()

        # results
        results_time = time.time()
        text = self.myfont4.render('Results:', False, (255, 255, 255))
        self.screen.blit(text, (650, self.game.border))
        correct = self.myfont2.render('Correct: ' + str(self.results["correct"]), False, (255, 255, 255))
        self.screen.blit(correct, (self.game.lborder, self.game.border + 70))
        missed = self.myfont2.render('Missed: ' + str(self.results["missed"]), False, (255, 255, 255))
        self.screen.blit(missed, (self.game.lborder, self.game.border + 120))
        false = self.myfont2.render('False Alarm: ' + str(self.results["false"]), False, (255, 255, 255))
        self.screen.blit(false, (self.game.lborder, self.game.border + 170))
        rate = self.myfont2.render('Success Rate: ' + "{:.2f}%".format(self.results["rate"]), False, (255, 255, 255))
        self.screen.blit(rate, (self.game.lborder, self.game.border + 220))

        pygame.display.flip()
        self.clock.tick(1/5)

        self.filename.write("Correct, Missed, False Alarm \n")
        self.filename.write(str(self.results["correct"]) + ", " + str(self.results["missed"]) + ", " + str(self.results["false"]) + "\n")

        print("Results: " + str(time.time() - results_time))
        self.filename.write("Results: " + str(time.time() - results_time) + "\n")
        print("Overall: " + str(time.time() - start_time))
        self.filename.write("Overall: " + str(time.time() - start_time) + "\n")


    def generate(self,i):
        self.num = random.randint(1,9)
        xpos, ypos = self.game.positions[self.pos_seq[i]]

        pygame.draw.rect(self.screen, self.game.cell_color, pygame.Rect(xpos,
                                                  ypos, self.game.cell_size[0],
                                                  self.game.cell_size[1]), self.game.corner_radius)
        text = self.myfont.render(str(chr(self.alpha_seq[i]+65)), True, (0, 0, 0))
        text_rect = text.get_rect(center=(xpos+self.game.cell_size[0]//2, ypos+self.game.cell_size[1]//2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        loop = 0
        while loop < 6:
            self.clock.tick(1/0.1)
            self.respond(i)
            loop += 1

        self.screen.fill(self.game.board_color)
        pygame.display.flip()

        loop = 0
        while loop < 10:
            self.clock.tick(1 / 0.1)
            self.respond(i)
            loop += 1

        self.clock.tick(1/0.4)

    def respond(self,i):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.input_alpha[i] = True
                    self.response_time_alpha[i] = str(datetime.now().time())

                elif event.button == 3:
                    self.input_pos[i] = True
                    self.response_time_pos[i] = str(datetime.now().time())

    def fixation(self, t):
        """
        generates fixation
            t: fixation time in seconds
        """
        self.screen.fill(self.game.board_color)
        fix_img = pygame.image.load("img/fixation.png")
        fix_img = pygame.transform.scale(fix_img, (self.game.monitor_size[1], self.game.monitor_size[1]))
        fix_rect = fix_img.get_rect()
        fix_rect.center = ((self.game.monitor_size[0] / 2), self.game.monitor_size[1] / 2)
        self.screen.blit(fix_img, fix_rect)

        fix_time = time.time()

        pygame.display.flip()

        i=0
        while i < t * 10:
            pygame.event.get()
            self.clock.tick(10)
            i+=1

        print("Fixation: " + str(time.time()-fix_time))
        self.filename.write("Fixation " + str(time.time() - fix_time) + " seconds" + "\n")
        
        self.screen.fill(self.game.board_color)
        pygame.display.flip()

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

        self.results["rate"] = 100 * self.results["correct"] / (self.results["correct"] + self.results["missed"] + self.results["false"])

    def writeResults(self):
        for i in range(len(self.answer_alpha)):
            if self.answer_alpha[i] == self.input_alpha[i] and self.answer_pos[i] == self.input_pos[i]:
                correct = 1
            else:
                correct = 0
            self.filename2.write(str(self.response_time_alpha[i]) + "," + str(self.response_time_pos[i]) + "," +
                                 str(self.n) + "," + chr(self.alpha_seq[i] + 65) + "," + str(self.pos_seq[i]) + "," +
                                 str(correct) + "\n")


class Session(object):
    def __init__(self, num_blocks, filename, filename2, n):
        self.num_blocks = num_blocks
        self.n = n
        self.sequence = [self.n, self.n]
        self.filename = filename
        self.filename2 = filename2

    def run_session(self):
        for i, n in enumerate(self.sequence):
            self.filename.write(str(n) + "-Back" + "\n")
            n_back = N_Back(self.filename, self.filename2, n)
            n_back.run()
            self.filename.write("\n")

        self.filename.write("Sequence: " + str(self.sequence) + "\n")


