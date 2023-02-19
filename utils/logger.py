import time

class Logger:
    def __init__(self, name) -> None:
        self.name = name
    
    def log(self, content):
        time_str = time.strftime("%d-%m-%Y|%H:%M:%S", time.localtime())
        return print(f"[{time_str}] <{self.name}> {content}")