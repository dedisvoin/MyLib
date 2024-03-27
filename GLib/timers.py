class TimerManager:
    def __init__(self) -> None:
        self.timers = []

    def add(self, timer):
        self.timers.append(timer)

    def update(self, delta):
        for timer in self.timers:
            timer.update(delta)

    def get(self, id):
        for timer in self.timers:
            if timer.id == id:
                return timer.ticked

class TimerTick:
    def __init__(self, tick, id) -> None:
        self.tick = tick
        self.timer = 0
        self.ticked = False
        self.id = id

    def update(self, delta):
        self.timer += delta
        if self.timer>self.tick:
            self.ticked = True
            self.timer = 0
        else:
            self.ticked = False

        