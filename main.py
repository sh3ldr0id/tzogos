from gymnasium import Env, spaces
from stable_baselines3 import PPO

from pyautogui import locateCenterOnScreen, leftClick, screenshot, moveTo, center
from webbrowser import open as start_web
from random import choice
from time import sleep
from matplotlib.pyplot import imshow, show

class DragonTowerEnv(Env):
    def __init__(self):
        self.observation_space = spaces.Box(0, 1, shape=(10, 3), dtype=int)

        self.action_space = spaces.MultiDiscrete([2, 3])

        self.URL = "https://stake.com/casino/games/dragon-tower"

        block_width = round(232/3)

        block1 = 0
        block2 = block_width
        block3 = 2*block_width

        self.level1 = [717, 472, 72, 20]
        self.level1_blocks = [
            self.level1.copy(),
            self.level1.copy(),
            self.level1.copy()
        ]
        
        self.level1_blocks[0][0] += block1
        self.level1_blocks[1][0] += block2
        self.level1_blocks[2][0] += block3
        
        self.level2 = [717, 444, 72, 20]
        self.level2_blocks = [
            self.level2.copy(),
            self.level2.copy(),
            self.level2.copy()
        ]
        self.level2_blocks[0][0] += block1
        self.level2_blocks[1][0] += block2
        self.level2_blocks[2][0] += block3

        start_web(self.URL)

        # input("press enter after turning off animations and resizing.")

        sleep(5)

    def _get_obs(self):
        while (107, 113, 115) not in screenshot(region=(717, 442, 232, 51)).getdata():
            sleep(.1)

        lvl1 = None
        lvl2 = None
        
        for index, block_location in enumerate(self.level1_blocks):
            if (140, 10, 36) in screenshot(region=block_location).getdata():
                lvl1 = index

                for index, block_location in enumerate(self.level2_blocks):
                    image = screenshot(region=block_location).getdata()
                    
                    if (27, 73, 74) not in image and (33, 129, 108) not in image:
                        lvl2 = index

                        return [lvl1, lvl2]
                    
                    print(image, block_location)
                    
                    imshow(image)
                    show()
            
        for index, block_location in enumerate(self.level2_blocks):
            if (140, 10, 36) in screenshot(region=block_location).getdata():
                lvl2 = index

                for index, block_location in enumerate(self.level1_blocks):
                    image = screenshot(region=block_location).getdata()

                    if (27, 73, 74) not in image and (33, 129, 108) not in image:
                        lvl1 = index

                        return [lvl1, lvl2]
                    
                    print(image, block_location)
                    
                    imshow(image)
                    show()

    def reset(self, seed=None, options=None):
        observation = self._get_obs()

        return observation

    def step(self, actions):
        choices = self.level1_blocks.copy()
        choices.pop(actions[0])
        lvl1 = choice(choices)

        choices = self.level2_blocks.copy()
        choices.pop(actions[1])
        lvl2 = choice(choices)

        while True:
            try:
                leftClick(
                    locateCenterOnScreen(image="components/bet.png")
                )
                sleep(1)
                
                break
            except:
                sleep(1)
                print("hi")
                pass

        reward = 1

        leftClick(lvl1)
        sleep(2)

        for block_location in self.level1_blocks:
            if (140, 10, 36) in screenshot(region=block_location).getdata():
                reward = -2

                return self._get_obs(), reward, False, False
            
        leftClick(lvl2)
        sleep(2)

        for block_location in self.level2_blocks:
            if (140, 10, 36) in screenshot(region=block_location).getdata():
                reward = -1

                return self._get_obs(), reward, False, False
            
        reward = 2

        while True:
            try:
                leftClick(
                    locateCenterOnScreen(image="components/cashout.png")
                )
                break

            except:
                print("cant find cashout")
                pass
        
        return self._get_obs(), reward, False, True if reward > 0 else False

    def close(self):
        return None

env = DragonTowerEnv()

for i in range(5):
    obs, _, _, won = env.step(env.action_space.sample())
    print(obs)
    sleep(1)

exit()

model = PPO("MlpPolicy", DragonTowerEnv, verbose=1)
model.learn(total_timesteps=5_000)

obs = DragonTowerEnv.reset()

for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = DragonTowerEnv.step(action)
    DragonTowerEnv.render()