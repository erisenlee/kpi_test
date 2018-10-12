import pandas as pd
from collections import namedtuple


class BasicIndicators:
    def __init__(self,df,noon_peak,moon_peak,**kwargs):
        self.df = df
        self.noon_peak = noon_peak
        self.moon_peak=moon_peak
        if kwargs:
            for name, value in kwargs.items():
                setattr(self, name, value)

    def _get_peak_indicators(self,df):
        is_noon_peak = (df['order_time'] >= pd.to_datetime(self.noon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.noon_peak.end))
        is_moon_peak = (df['order_time'] >= pd.to_datetime(self.moon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.moon_peak.end))
        return is_noon_peak,is_moon_peak
                
    def _get_indicators(self,df):
        is_normal_waybill=df['waybill_type']=='普通单'
        is_booked_waybill = df['waybill_type'] == '预定单'
        is_complete_waybill = df['delivery_status'] == '配送成功'
        is_valid_waybill = df['fraud_flag'] == '非欺诈单'
        is_timeout_waybill=df['timeout_flag']=='超时'
        is_exception_cancel = df['excption_cancel_flag'] == '异常取消'
        # is_noon_peak = (df['order_time'] >= pd.to_datetime(self.noon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.noon_peak.end))
        # is_moon_peak = (df['order_time'] >= pd.to_datetime(self.moon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.moon_peak.end))
        is_noon_peak,is_moon_peak=self._get_peak_indicators(df)
        BasicIndicators = namedtuple('BasicIndicators', [
            'is_normal_waybill',
            'is_booked_waybill',
            'is_complete_waybill',
            'is_valid_waybill',
            'is_exception_cancel',
            'is_timeout_waybill',
            'is_noon_peak',
            'is_moon_peak'
        ])
        indicators= BasicIndicators(
                is_normal_waybill,
                is_booked_waybill,
                is_valid_waybill,
                is_complete_waybill,
                is_exception_cancel,
                is_timeout_waybill,
                is_noon_peak,
                is_moon_peak
        )
        return indicators

    def get_indicators_value(self):
        indicators = self._get_indicators(self.df)
        total_waybill = self.df
        complete_waybill =self.df[indicators.is_complete_waybill]
        valid_waybill= complete_waybill[indicators.is_valid_waybill]
        normal_waybill = self.df[indicators.is_normal_waybill]
        booked_waybill = self.df[indicators.is_booked_waybill]
        exception_waybill = self.df[indicators.is_exception_cancel]
        timeout_waybill = self.df[indicators.is_timeout_waybill]
        noon_peak = valid_waybill[indicators.is_noon_peak]
        moon_peak=valid_waybill[indicators.is_moon_peak]
        
        BasicIndicatorsValue = namedtuple('BasicIndicatorsValue',[
            'total_waybill',
            'complete_waybill',
            'valid_waybill',
            'normal_waybill',
            'booked_waybill',
            'exception_waybill',
            'timeout_waybill',
            'noon_peak_waybill',
            'moon_peak_waybill',
        ])
        basic_indicators_value = BasicIndicatorsValue(
            total_waybill.shape[0],
            complete_waybill.shape[0],
            valid_waybill.shape[0],
            normal_waybill.shape[0],
            booked_waybill.shape[0],
            exception_waybill.shape[0],
            timeout_waybill.shape[0],
            noon_peak.shape[0],
            moon_peak.shape[0],
        )
        return basic_indicators_value



if __name__ == '__main__':
    from config import filepath, moon_peak, noon_peak

    s = ScoreRate(filepath, '2018-07-08')
    # df=s.df
    # is_val = df['配送状态'] == '已完成'
    # print(df[is_val].shape[0])
    print(s.get_rate(), s.get_peak(moon_peak, noon_peak))
