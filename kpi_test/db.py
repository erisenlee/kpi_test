from common.database import Db
from common.readConfig import ReadConfig
import pandas as pd

def get_data(sql):
    config = ReadConfig()
    data = config.get_section('db')
    con = Db(
        host=data['host'],
        port=data['port'],
        user=data['user'],
        password=data['password'],
        db=data['db']
    )
    return con.get_df(sql)

def main():
    sql="SELECT*FROM t_waybill AS a WHERE a.finish_time>='2018-07-30 00:00:00' AND a.finish_time<='2018-07-30 23:59:59' AND a.point_name='蜂鸟BOD（金牛万达站）' AND a.delivery_status='配送成功'"
    df = get_data(sql)
    is_valid=df['delivery_status']=='配送成功'
    noon_peak_begin = pd.to_datetime('2018-07-30 11:30:00')
    noon_peak_end = pd.to_datetime('2018-07-30 13:30:00')
    # r=pd.to_datetime(finish_time_begin)
    valid_waybill=df[is_valid]
    is_noon_peak = (df['order_time'] >= noon_peak_begin) & (df['order_time'] <= noon_peak_end)
    r=valid_waybill[is_noon_peak].shape

    print(r)
if __name__ == '__main__':
    main()

