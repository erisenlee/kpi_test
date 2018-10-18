import pandas as pd
# import numpy as np
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
        return is_noon_peak, is_moon_peak
        
    def _get_active_courier(self, df):
        if not hasattr(self, 'active_courier_no'):
            setattr(self, 'active_courier_no', 1)
        
        s = df.groupby('courier_name').size()
        return s[s>=self.active_courier_no]


    def _get_basic_indicators(self,df):
        is_normal_waybill=df['waybill_type']=='普通单'
        is_booked_waybill = df['waybill_type'] == '预定单'
        is_complete_waybill = df['delivery_status'] == '配送成功'
        is_valid_waybill = df['fraud_flag'] == '非欺诈单'
        is_timeout_waybill=df['timeout_flag']=='超时'
        is_exception_cancel = df['excption_cancel_flag'] == '异常取消'
        is_noon_peak, is_moon_peak = self._get_peak_indicators(df)
        
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
                is_complete_waybill,
                is_valid_waybill,
                is_exception_cancel,
                is_timeout_waybill,
                is_noon_peak,
                is_moon_peak
        )
        return indicators

    def get_indicators_value(self):
        indicators = self._get_basic_indicators(self.df)
        total_waybill = self.df
        complete_waybill =self.df[indicators.is_complete_waybill]
        valid_waybill= complete_waybill[indicators.is_valid_waybill]
        normal_waybill = self.df[indicators.is_normal_waybill]
        booked_waybill = self.df[indicators.is_booked_waybill]
        exception_waybill = self.df[indicators.is_exception_cancel]
        timeout_waybill = self.df[indicators.is_timeout_waybill]
        noon_peak = valid_waybill[indicators.is_noon_peak]
        moon_peak=valid_waybill[indicators.is_moon_peak]
        active_courier=self._get_active_courier(valid_waybill)
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
            'active_courier'
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
            active_courier.size
        )
        return basic_indicators_value

def _to_datetime(time):
    from datetime import datetime
    time = int(str(time)[:-3])
    return datetime.fromtimestamp(time)


class ServiceIndicator(object):
    """docstring for ServiceIndicator."""
    def __init__(self, evaluate,feedback):
        self.evaluate = evaluate
        self.feedback = feedback
            
    def _get_valid_time(self,df):
        df['created_at'] = df['created_at'].apply(_to_datetime)
        df['time'] = df['created_at'] - df['finish_time']
        # print(df['created_at'].dtype, df['finish_time'].dtype)
        df['time'] = df['time'].map(lambda x: x.seconds)
        is_valid = df['time'] <= 48 ** 3600
        valid_time=df[is_valid]
        # print(valid_time.shape)
        return valid_time

    def get_evaluate_indicators(self):
        """评价"""
        valid_time = self._get_valid_time(self.evaluate)
        is_positive = valid_time['star'] == 3
        is_negtive = valid_time['star'] == 1
        positive = valid_time[is_positive].shape[0]
        negetive = valid_time[is_negtive].shape[0]
        return positive, negetive
       
    def get_feedback_indicators(self):
        """投诉"""
        valid_time = self._get_valid_time(self.feedback)
        is_feedback = valid_time['status'] == 90
        feedback = valid_time[is_feedback].shape[0]
        return feedback

    def get_indicators_value(self):
        positive, negetive = self.get_evaluate_indicators()
        complain=self.get_feedback_indicators()
        ServiceIndicatorValue=namedtuple('ServiceIndicatorValue',[
            'positive',
            'negetive',
            'complain'
        ])
        indicator_value = ServiceIndicatorValue(
            positive,
            negetive,
            complain
        )
        return indicator_value 


if __name__ == '__main__':
    from config import filepath, moon_peak, noon_peak

    s = ScoreRate(filepath, '2018-07-08')
    # df=s.df
    # is_val = df['配送状态'] == '已完成'
    # print(df[is_val].shape[0])
    print(s.get_rate(), s.get_peak(moon_peak, noon_peak))
