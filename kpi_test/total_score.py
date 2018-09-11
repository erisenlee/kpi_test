from score_compute import KpiScore
from kpi_indicator import ScoreRate
from config import filepath, kpi_list, caculate_date, noon_peak, moon_peak
from collections import namedtuple


class Total:
    def __init__(self, filepath, caculate_date):
        self.score_rate = ScoreRate(filepath, caculate_date)

    def get_indicators_value(self):
        return self.score_rate.get_indicators_value()

    def get_indicators_rate(self):
        return self.score_rate.get_indicators_rate()

    def get_peak_result(self, moon_peak, noon_peak):
        return self.score_rate.get_peak(moon_peak, noon_peak)

    def get_rate_score(self):
        Kpi = namedtuple(typename='Kpi', field_names=[
                         'min', 'mid', 'max', 'flags'])
        kpi_tuple = (Kpi(*t) for t in kpi_list)
        delay_score, badbill_score, cancel_score, positiv_score = (
            KpiScore(i) for i in kpi_tuple)
        IndicatorScore = namedtuple(
            'IndicatorScore', ('bad_bill_score', 'unnormal_cancel_score', 'delay_score', 'postive_score'))

        indicators_rate = self.get_indicators_rate()

        indicator_score_tuple = IndicatorScore(
            bad_bill_score=badbill_score.get_score(
                indicators_rate.bad_bill_rate),
            unnormal_cancel_score=cancel_score.get_score(
                indicators_rate.abnormal_cancel_rate),
            delay_score=delay_score.get_score(
                indicators_rate.delay_rate),
            postive_score=positiv_score.get_score(
                indicators_rate.positive_rate)
        )
        return indicator_score_tuple

    def get_total_score(self):
        delay_score, bad_bill_score, cancel_score, positive_score = self.get_rate_score()
        return round(delay_score * 0.1 + cancel_score * 0.4 + bad_bill_score * 0.3 + positive_score * 0.2, 2)


if __name__ == '__main__':
    t = Total(filepath, caculate_date)

    print(t.get_indicators_value())
    print(t.get_indicators_rate())
    print(t.get_rate_score())
    print(t.get_peak_result(moon_peak, noon_peak))
