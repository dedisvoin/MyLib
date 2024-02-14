from GLib.mathematics import *
from GLib.drawing import *

def collide_rect(r1_pos, r1_size, r2_pos, r2_size,):
        
        min_x = min(r1_pos[0], r2_pos[0])
        min_y = min(r1_pos[1], r2_pos[1])

        max_x = max(r1_pos[0] + r1_size[0], r2_pos[0] + r2_size[0])
        max_y = max(r1_pos[1] + r1_size[1], r2_pos[1] + r2_size[1])


        dist_w = distance([min_x, min_y], [max_x, min_y])
        dist_h = distance([min_x, min_y], [min_x, max_y])
        
        #Draw.draw_rect(win.surf, [min_x, min_y], [dist_w, dist_h], 'red',1)
        if dist_w < r1_size[0] + r2_size[0] and dist_h < r1_size[1] + r2_size[1]:
            return True
        
        
        return False


class Physics:
    GRAVITY = Vector2(0,0.5)
    
    class CollidingRect:
        def __init__(self, size, pos, statick=True, id=None, bounsing=Vector2(0,0), trenie=Vector2(1,1), air_resistance=Vector2(0.999,0.999), triggering=True) -> None:
            self._size = size
            self._pos = pos

            self._statick = statick
            
            self._id = id
            
            self._speed = Vector2(0,0)
            self.bounsing = bounsing
            self.trenie = trenie
            self.air_resistance = air_resistance
            self.triggering = triggering
            
            self.trigers = {
                'up':False,
                'down':False,
                'left':False,
                'right':False
            }
            
        def set_default_triggers(self):
            self.trigers = {
                'up':False,
                'down':False,
                'left':False,
                'right':False
            }
            
        def generate_id(self, id):
            if id is None:
                id = random.randint(0, 999999999999)
                return id
            else:
                return id
            
        @property
        def h(self):
            return self._size[0]
        
        @property
        def w(self):
            return self._size[1]
            
        @property
        def x(self):
            return self._pos[0]

        @property
        def y(self):
            return self._pos[1]
        
        @property
        def wh(self):
            return self._size
        
        @x.setter
        def x(self,x):
            self._pos[0] = x

        @y.setter
        def y(self,y):
            self._pos[1] = y
            
        @property
        def xy(self):
            return self._pos
        
        @xy.setter
        def xy(self, pos):
            self._pos = pos
            
        @property
        def center_x(self):
            return self._pos[0]+self._size[0]/2
        
        @property
        def center_y(self):
            return self._pos[1]+self._size[1]/2
        
        @property
        def center(self):
            return [
                self._pos[0]+self._size[0]/2,
                self._pos[1]+self._size[1]/2
            ]
            
            
        @property
        def up(self):
            return self._pos[1]
        
        @property
        def left(self):
            return self._pos[0]
        
        @property
        def down(self):
            return self._pos[1]+self._size[1]
        
        @property
        def right(self):
            return self._pos[0]+self._size[0]
        
    
        @up.setter
        def up(self, y):
            self._pos[1] = y
        
        @left.setter
        def left(self, x):
            self._pos[0] = x
        
        @down.setter
        def down(self, y):
            self._pos[1] = y-self._size[1]
        
        @right.setter
        def right(self, x):
            self._pos[0]= x-self._size[0]
            
    class CollidingSpace:
        def __init__(self) -> None:
            self.colliders = []
            
        def add(self, collider) -> None:
            self.colliders.append(collider)
            
        def adds(self, colliders) -> None:
            self.colliders+=colliders
            
        def create_collided_rect_list(self, collider):
            collided_rect_list = []
            for collider2 in self.colliders:
                if collider._id != collider2._id and collider2.triggering:

                    if collide_rect(collider._pos, collider._size, collider2._pos, collider2._size):
                        collided_rect_list.append(collider2)
            return collided_rect_list
        
        def get_rect(self, id):
            for rect in self.colliders:
                if rect._id == id: return rect
            
        def __simulate_attach_y__(self, collider, collide_objects) -> None:
            for collider_a in collide_objects:
                if collider_a._statick:
                    collider._speed.x *= collider_a.trenie.x
                    
                    if collider._speed.y > 0:
                            collider.down = collider_a.up
                            collider._speed.y *= -collider.bounsing.y
                            collider.trigers['down'] = True
                            break

                    elif collider._speed.y <= 0:
                            collider.up = collider_a.down
                            collider._speed.y *= -collider.bounsing.y
                            collider.trigers['up'] = True
                            break

                

        def __simulate_attach_x__(self, collider, collide_objects) -> None:
            for collider_a in collide_objects:
                if collider_a._statick:

                    
                    collider._speed.y *= collider_a.trenie.y
                    if collider._speed.x > 0:
                        collider.right = collider_a.left
                        collider._speed.x *= -collider.bounsing.x
                        collider.trigers['right'] = True
                        break

                    elif collider._speed.x <= 0:
                        collider.left = collider_a.right
                        collider._speed.x *= -collider.bounsing.x
                        collider.trigers['left'] = True
                        break


        def update(self):
            for i, collider in enumerate(self.colliders):
                if not collider._statick:
                    collider.set_default_triggers()


                    # collider._speed.x = round(collider._speed.x, 4)
                    # collider._speed.y = round(collider._speed.y, 4)
                    collider._speed.x*=collider.air_resistance.x
                    collider._speed.y*=collider.air_resistance.y

                    
                    collider._pos[1] += collider._speed.y
                    

                    collider._speed.y += Physics.GRAVITY.y

                    collide_objects = copy(self.create_collided_rect_list(collider))

                    self.__simulate_attach_y__(collider, collide_objects)

                    
                    collider._pos[0] += collider._speed.x

                    collider._speed.x += Physics.GRAVITY.x

                    collide_objects = copy(self.create_collided_rect_list(collider))

                    self.__simulate_attach_x__(collider, collide_objects)
            
        def view(self, surf):
            for collider in self.colliders:
                Draw.draw_rect(surf, collider._pos, collider._size, 'blue') 