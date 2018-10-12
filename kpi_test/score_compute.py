
class IndicatorScore:
    def __init__(self, indicator_score_config):
        self.indicator = indicator_score_config

    #非好评
    def get_score_1(self, value):
        if value >= self.indicator.min and value < self.indicator.mid:
            score = (value - self.indicator.mid) / (self.indicator.min - self.indicator.mid) * 55 + 45
            return round(score, 2)
        elif value >= self.indicator.mid and value < self.indicator.max:
            score = (value - self.indicator.max) / (self.indicator.mid - self.indicator.max) * 45
            return round(score, 2)
        elif value >= self.indicator.max:
            return 0
    #好评
    def get_score_0(self, value):
        if value > self.indicator.min and value < self.indicator.mid:
            score = (value - self.indicator.min) / (self.indicator.mid - self.indicator.min) * 45
            return round(score, 2)
        elif value >= self.indicator.mid and value < self.indicator.max:
            score = (value - self.indicator.mid) / (self.indicator.max - self.indicator.mid) * 55 + 45
            return round(score, 2)
        elif value >= self.indicator.max:
            return 100
        elif value <= self.indicator.min:
            return 0

    def get_score(self, value):
        if self.indicator.flags == 1:
            return self.get_score_1(value)
        else:
            return self.get_score_0(value)
