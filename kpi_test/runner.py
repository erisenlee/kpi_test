from common.readConfig import ReadConfig
from common.database import Db
from kpi_indicator import BasicIndicators,ServiceIndicator
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
        config=self.get_config()
        Peak = get_nametuple('Peak', 'begin', 'end')
        noon_peak = Peak(begin=config['noon_peak_begin'], end=config['noon_peak_end'])
        moon_peak = Peak(begin=config['moon_peak_begin'], end=config['moon_peak_end'])
        return noon_peak,moon_peak

    def get_config(self):
        config=self.config.get_section('basic')
        return config
    
    def get_basic_df(self):
        config=self.get_config()
        sql="SELECT*FROM t_waybill AS a WHERE a.finish_time>='{}' AND a.finish_time<='{}' AND a.point_name='{}'".format(config['finish_time_begin'],config['finish_time_end'],config['point_name'])
        db = self._get_db()
        return db.get_df(sql)

    def get_basic_indicators(self):
        basic_df = self.get_basic_df()
        noon_peak, moon_peak = self._get_peak()
        active_courier_no=int(self.config.get_option('basic','active_courier_no'))
        basic = BasicIndicators(basic_df, noon_peak, moon_peak, active_courier_no=active_courier_no)
        return basic.get_indicators_value()

    def _get_service_df(self,tb):
        config=self.get_config()
        sql="""SELECT * FROM 
            t_waybill as a
            JOIN {} as b
            on a.waybill_no=b.tracking_id
            where a.finish_time >= '{}'
            AND a.finish_time <= '{}'
            AND a.point_name = '{}'
            """.format(tb,config['finish_time_begin'],config['finish_time_end'],config['point_name'])
        df = self._get_db().get_df(sql)
        return df
    
    def get_service_indicators(self):
        evaluate=self._get_service_df('t_evaluate_detail')
        appeal=self._get_service_df('t_feedback_detail')
        indicators = ServiceIndicator(evaluate, appeal)
        return indicators.get_indicators_value()

if __name__ == '__main__':
    t = Tester()
    print(t.get_basic_indicators())
    print(t.get_service_indicators())
    # print(t._get_peak())
