from GLib.drawing import *
from GLib.mathematics import *

class LinePath:
    def __init__(self, points: list[list[int]]) -> "LinePath":
        self.points = points
        self.point_index = 0
        self.timer = 0
        self.point = [0, 0]
        self.pos = [0,0]

        self.speed = [0,0]

    def update(self, tick=50, lerp=2.5):

        self.point_count = len(self.points)
        if self.point_count>2:
            self.timer += 1
            if self.timer % tick == 0:
                self.point_index += 1
            

            if self.point_index > self.point_count-1:
                self.point_index = 0
            
            self.point = self.points[self.point_index]
            

            normal = [
                self.point[0]-self.pos[0], 
                self.point[1]-self.pos[1]
            ]
            normal[0]*=0.08
            normal[1]*=0.08

            self.speed[0]+=normal[0]
            self.speed[1]+=normal[1]
            self.speed[0]/=lerp
            self.speed[1]/=lerp

            self.pos[0]+=self.speed[0]
            self.pos[1]+=self.speed[1]

    def view(self, window):
        try:
            Draw.draw_lines(window.surf, self.points, 'gray', 1, True)
            for i, point in enumerate(self.points):
                if i == self.point_index:
                    Draw.draw_circle(window.surf, point, 10, 'orange', 2)
                else:
                    Draw.draw_circle(window.surf, point, 10, 'grey', 2)
        except:...
    