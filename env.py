from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np

from sklearn.preprocessing import StandardScaler

from webbrowser import open as start_web
from pyautogui import locateCenterOnScreen, leftClick, screenshot, typewrite, moveTo
import pytesseract

from time import sleep
import re

from json import loads

with open("config.json", "r") as file:
    config = file.read()

config = loads(config)

pytesseract.pytesseract.tesseract_cmd = config["tesseract"]

class LimboEnv(Env):
    def __init__(self):
        super(LimboEnv, self).__init__()

        self.win_size = 5

        self.action_space = Discrete(2)
        self.observation_space = Box(low=0, high=1, shape=(1, self.win_size), dtype=np.float16)

        self.URL = "https://stake.com/casino/games/limbo"

        self.locations = config["locations"]

        start_web(self.URL)

        sleep(10)
        
        self.scaler = StandardScaler()
        self.state = []

        with open("targets.dat", "r") as file:
            data = file.read().split("\n")

        self.nonce = 0
        self.multipliers = []

        for target in data:
            if target:
                self.nonce += 1
                self.multipliers.append(float(target))        

        self.set_multiplier(2)

        while len(self.multipliers) < self.win_size:
            self.play_random()

        self.get_obs()

    def reset(self, seed=None):
        self.get_obs()

        return self.state, {}
    
    def get_obs(self):
        self.state = self.scaler.fit_transform(
            np.array(
                self.multipliers[-self.win_size:]
            ).reshape(1, -1)
        )

    def set_amount(self, amount):
        leftClick(
            self.locations["amount"]
        )

        typewrite(str(amount))

    def set_multiplier(self, multiplier):
        leftClick(
            self.locations["multiplier"]
        )

        typewrite(str(multiplier))
    
    def wait(self):
        while True:
            try:
                locateCenterOnScreen(image="components/bet.png")

                sleep(0.2)

                break

            except:
                sleep(0.1)
    
    def bet(self):
        self.wait()

        leftClick(
            self.locations["bet"]
        )

        moveTo((10, 10))

        self.nonce += 1

        self.wait()

    def save_target(self, multiplier):
        with open("targets.dat", "a") as file:
            file.write(f"{multiplier}\n")

    def get_multiplier(self):
        img = screenshot(region=self.locations["game"]).convert("RGB")
        text = pytesseract.image_to_string(img)
        multiplier = float(''.join(re.findall(r'[-+]?\d*\.\d+|\d+', text)))

        self.multipliers.append(multiplier)

        self.save_target(multiplier)

        return multiplier

    def play_random(self):
        self.bet()
        
        self.get_multiplier()

    def step(self, action):
        self.bet()

        actual = self.get_multiplier()

        if actual >= 2:
            reward = 1

        else: 
            reward = -1

        self.get_obs()
        
        return self.state, reward, False, {}, {}