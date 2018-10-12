import pymysql
import pandas as pd
pymysql.install_as_MySQLdb()


class Db:
    def __init__(self, host, port, user, password, db):
        self.con = pymysql.connect(host=host, port=int(port), user=user,
                                   password=password, db=db, cursorclass=pymysql.cursors.DictCursor)

    def query(self, sql):
        try:
            with self.con.cursor() as cur:
                cur.execute(sql)
                result = cur.fetchall()
                return result
        finally:
            self.con.close()

    def get_df(self, sql):
        try:
            dict_data = self.query(sql)    
        except expression as identifier:
            print("{}".format(identifier))
        if dict_data:
            return pd.DataFrame(dict_data)



if __name__ == '__main__':
    from config import HOST, USERNAME, PASSWORD, PORT, DB

    def main(sql):
        con = Db(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, db=DB)
        result = con.get_df(sql)
        return result

    sql = """SELECT
	*
    FROM
	t_waybill AS a
    WHERE
	a.finish_time >= '2018-07-30 00:00:00'
    AND a.finish_time <= '2018-07-30 23:59:59'
    AND a.point_name = '蜂鸟BOD（金牛万达站）'
    """
    df = main(sql)
    is_positive = df['user_rate'] == '非常满意'
    print(df[is_positive].shape)
