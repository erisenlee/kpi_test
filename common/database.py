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
    import time
    t1=time.time()
    db = Db(host="59.63.222.206", port="33666", user="develop", password="develop+123456", db="fns")
   
    sql = """
    SELECT
	a.waybill_no,
	b.created_at,
	b.star 
FROM
	t_waybill AS a
	JOIN t_evaluate_detail AS b ON a.waybill_no = b.tracking_id 
WHERE
	a.finish_time >= '2018-09-19 00:00:00' 
	AND a.finish_time <= '2018-09-19 23:59:59' 
	AND a.point_name = '江西蜂鸟-金牛万达站' 
	AND b.star =3
    """
    rows = db.query(sql)
    print(len(rows))
    t2=time.time()
    print(t2-t1)
