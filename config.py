from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    custom_ip: str
    
env = Env.read_env()
    
config = Config(custom_ip="")