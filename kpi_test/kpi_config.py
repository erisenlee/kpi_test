from collections import namedtuple

Peak = namedtuple('Peak', ['begin', 'end'])
noon_peak = Peak(begin='2018-07-08 11:30:00', end='2018-07-08 13:30:00')
moon_peak = Peak(begin='2018-07-08 17:30:00', end='2018-07-08 18:30:00')


delay_kpi = (0, 0.0083, 0.036, 1)
badbill_kpi = (0, 0.0018, 0.0039, 1)
cancel_kpi = (0, 0.0006, 0.0037, 1)
positive_kpi = (0.1, 0.1475, 0.2, 0)

kpi_list = [delay_kpi, badbill_kpi, cancel_kpi, positive_kpi]
caculate_date = '2018-07-22'
