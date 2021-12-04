from collections import deque

from cv2 import setNumThreads

class MovingAvg:

    def __init__(self, max_vals = 10, threshold = .1):
        self.values = deque()
        self.max_vals = max_vals
        self._avg = 0.0
        self.sum = 0
        self.threshold = threshold
        
    def push(self, val):
        if len(self.values) == self.max_vals:
            if not self.withinBounds(val):
                return
            self.sum -= self.values.popleft()
        
        self.values.append(val)
        self.sum += val
        if len(self.values) > 0:
            self.avg = self.sum / len(self.values)

        return self.avg

    @property
    def avg(self):
        return self._avg

    @avg.setter
    def avg(self, a):
        self._avg = a

    
    def full(self):
        return len(self.values) == self.max_vals

    def withinBounds(self, val):
        return True
        return self.avg * (1 + self.threshold) >= val and self.avg * (1 - self.threshold) <= val