from common.readConfig import ReadConfig
from common.database import Db
from kpi_indicator import BasicIndicators
from core import get_nametuple

class Tester:
    def __init__(self):
        self.config = ReadConfig()

    def _get_db(self):
        data = self.config.get_section('db')
        con = Db(
        host=data['host'],
        port=data['port'],
        user=data['user'],
        password=data['password'],
        db=data['db']
        )
        return con
    def _get_peak(self):
        config=self.get_sql_data()
        Peak = get_nametuple('Peak', 'begin', 'end')
        noon_peak = Peak(begin=config['noon_peak_begin'], end=config['noon_peak_end'])
        moon_peak = Peak(begin=config['moon_peak_begin'], end=config['moon_peak_end'])
        # noon_peak=get_nametuple('Peak',begin=)
        return noon_peak,moon_peak
        
    def get_sql_data(self):
        config=self.config.get_section('basic')
        return config
    
    def get_df(self):
        config=self.get_sql_data()
        sql="SELECT*FROM t_waybill AS a WHERE a.finish_time>='{}' AND a.finish_time<='{}' AND a.point_name='{}'".format(config['finish_time_begin'],config['finish_time_end'],config['point_name'])
        db = self._get_db()
        return db.get_df(sql)
    def get_basic_indicators(self):
        df = self.get_df()
        noon_peak,moon_peak=self._get_peak()
        basic = BasicIndicators(df, noon_peak, moon_peak)
        return basic.get_indicators_value()



if __name__ == '__main__':
    t = Tester()
    print(t.get_basic_indicators())
    # print(t._get_peak())
