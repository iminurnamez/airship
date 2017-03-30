import os
import json


class Player(object):
    def __init__(self, info):
        self.points = info["points"]
        self.unlocked = info["unlocked"]
        self.high_scores = info["high scores"]
        
    def add_score(self, level_num, score):
        num = str(level_num)
        if num not in self.high_scores:
            self.high_scores[num] = 0
        to_beat = self.high_scores[num]    
        if score > to_beat:
            self.points += score - to_beat
            self.high_scores[num] = score
            
    def save(self):
        info = {
            "points": self.points,
            "unlocked": self.unlocked,
            "high scores": self.high_scores}
        with open(os.path.join("resources", "player.json"), "w") as f:
            json.dump(info, f)
            
            
    