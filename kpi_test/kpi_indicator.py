import pandas as pd
# from utils import col_timestamp, col_format, col_date
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
        is_valid_waybill = df['delivery_status'] == '配送成功'
        is_exception_cancel = df['excption_cancel_flag'] == '异常取消'
        is_noon_peak = (df['order_time'] >= pd.to_datetime(self.noon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.noon_peak.end))
        is_moon_peak = (df['order_time'] >= pd.to_datetime(self.moon_peak.begin)) & (df['order_time'] <= pd.to_datetime(self.moon_peak.end))
        BasicIndicators = namedtuple('BasicIndicators', [
            'is_normal_waybill',
            'is_booked_waybill',
            'is_valid_waybill',
            'is_exception_cancel',
            'is_noon_peak',
            'is_moon_peak'
        ])
        indicators= BasicIndicators(
                is_normal_waybill,
                is_booked_waybill,
                is_valid_waybill,
                is_exception_cancel,
                is_noon_peak,
                is_moon_peak
        )
        return indicators

    def get_indicators_value(self):
        indicators = self._get_indicators(self.df)
        total_waybill = self.df
        valid_waybill=self.df[indicators.is_valid_waybill]
        normal_waybill = self.df[indicators.is_normal_waybill]
        booked_waybill = self.df[indicators.is_booked_waybill]
        exception_waybill = self.df[indicators.is_exception_cancel]
        noon_peak = valid_waybill[indicators.is_moon_peak]
        moon_peak=valid_waybill[indicators.is_moon_peak]
        
        BasicIndicatorsValue = namedtuple('BasicIndicatorsValue',[
            'total_waybill',
            'valid_waybill',
            'normal_waybill',
            'booked_waybill',
            'exception_waybill',
            'noon_peak',
            'moon_peak',
        ])
        basic_indicators_value = BasicIndicatorsValue(
            total_waybill.shape[0],
            valid_waybill.shape[0],
            normal_waybill.shape[0],
            booked_waybill.shape[0],
            exception_waybill.shape[0],
            noon_peak.shape[0],
            moon_peak.shape[0],
        )
        return basic_indicators_value



    # def get_peak(self, moon_peak, noon_peak):
    #     # self.df['用户下单时间'] = col_str(self.df['用户下单时间'])
    #     # self.df['用户下单时间'] = col_timestamp(self.df['用户下单时间'])
    #     # print(self.df['用户下单时间'])
    #     self.df = self.df.set_index('用户下单时间')

    #     moon_peak = \
    #         self.df.loc[(self.df.index >= pd.to_datetime(moon_peak.begin)) & (
    #             self.df.index <= pd.to_datetime(moon_peak.end))]
    #     noon_peak = \
    #         self.df.loc[(self.df.index >= pd.to_datetime(noon_peak.begin)) & (
    #             self.df.index <= pd.to_datetime(noon_peak.end))]

    #     noon_peak_val = noon_peak[noon_peak['配送状态'] == '已完成'].shape[0]
    #     moon_peak_val = moon_peak[moon_peak['配送状态'] == '已完成'].shape[0]
    #     PeakResult = namedtuple(
    #         'PeakResult', ('noon_peak_val', 'moon_peak_val'))
    #     peakresult = PeakResult(noon_peak_val, moon_peak_val)

    #     return peakresult

    # def get_indicators_value(self):
    #     is_val = self.df['配送状态'] == '已完成'
    #     is_preorder = self.df['运单类型'] == '预订单'
    #     is_order = self.df['运单类型'] == '普通单'
    #     is_delay = self.df['超时状态'] == '是'
    #     is_positive = self.df['用户评价'] == '非常满意'
    #     is_negative = self.df['用户评价'] == '吐槽'
    #     is_user_complaint = self.df['用户投诉状态'] == '是'
    #     is_seller_complaint = self.df['商户投诉状态'] == '是'
    #     is_abnormal_cancel = self.df['异常取消状态'] == '异常取消'

    #     total = self.df.shape[0]
    #     val = self.df[is_val].shape[0]

    #     order = self.df[is_order].shape[0]
    #     pre_order = self.df[is_preorder].shape[0]
    #     delay = self.df[is_delay].shape[0]
    #     positive = self.df[is_positive].shape[0]
    #     negative = self.df[is_negative].shape[0]
    #     user_complaint = self.df[is_user_complaint].shape[0]
    #     seller_complaint = self.df[is_seller_complaint].shape[0]
    #     abnormal_cancel = self.df[is_abnormal_cancel].shape[0]
    #     bad_bill = negative + user_complaint + seller_complaint
    #     IndicatorValue = namedtuple('IndicatorValue', [
    #         'total_bill',
    #         'valid_bill',
    #         'pre_order',
    #         'order',
    #         'delay',
    #         'positive',
    #         'negative',
    #         'abnormal_cancel',
    #         'user_complaint',
    #         'bad_bill'
    #     ])

    #     IndicatorValueResult = IndicatorValue(
    #         total_bill=total,
    #         valid_bill=val,
    #         pre_order=pre_order,
    #         order=order,
    #         delay=delay,
    #         positive=positive,
    #         negative=negative,
    #         abnormal_cancel=abnormal_cancel,
    #         user_complaint=user_complaint,
    #         bad_bill=bad_bill
    #     )
    #     return IndicatorValueResult

    # def get_indicators_rate(self):
    #     value = self.get_indicators_value()
    #     total = value.total_bill
    #     abnormal_cancel_rate = round(value.abnormal_cancel / total, 4)
    #     bad_bill_rate = round(value.bad_bill / total, 4)
    #     delay_rate = round(value.delay / total, 4)
    #     positive_rate = round(value.positive / total, 4)

    #     ScoreRate = namedtuple('ScoreRate', [
    #         'abnormal_cancel_rate',
    #         'bad_bill_rate',
    #         'delay_rate',
    #         'positive_rate',

    #     ])

    #     indicator_rate = ScoreRate(
    #         abnormal_cancel_rate=abnormal_cancel_rate,
    #         bad_bill_rate=bad_bill_rate,
    #         delay_rate=delay_rate,
    #         positive_rate=positive_rate
    #     )

    #     return indicator_rate


if __name__ == '__main__':
    from config import filepath, moon_peak, noon_peak

    s = ScoreRate(filepath, '2018-07-08')
    # df=s.df
    # is_val = df['配送状态'] == '已完成'
    # print(df[is_val].shape[0])
    print(s.get_rate(), s.get_peak(moon_peak, noon_peak))
