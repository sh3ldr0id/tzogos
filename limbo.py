from stable_baselines3 import PPO
from env import LimboEnv

env = LimboEnv()

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100)

model.save("./model")

obs, _ = env.reset()

rewards = 0

for _ in range(10):
    action, _ = model.predict(obs)
    obs, reward, dones, info = env.step(action)

    rewards += reward

    print(f"Total: {rewards} | Reward: {reward}")