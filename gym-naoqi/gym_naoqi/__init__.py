from gym.envs.registration import register

register(
    id='naoqi-v0',
    entry_point='gym_naoqi.envs:NaoqiEnv',
)