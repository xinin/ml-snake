import os

class Score:

    def __init__(self, folder, snake_number):
        self.score = 0
        self.score_folder = folder
        self.snake_number = snake_number
        return

    def add_score(self,points,data):
        self.score += points
        f = open(self.score_folder+'/temp_'+str(self.snake_number),'a')
        #data.append(self.score)
        f.write(','.join(map(str,data))+'\n')
        f.close()

    def reset(self):
        self.score = 0

    def close(self):
        os.rename(self.score_folder+'/temp_'+str(self.snake_number), self.score_folder+'/'+str(self.score).zfill(8)+'_snake'+str(self.snake_number)+'.csv')
