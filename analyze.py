import decimal
import psycopg2

conn = psycopg2.connect('dbname=maksimovs_budget user=pavel password=gibbson')
cur = conn.cursor()

cur.execute("select s.time, s.amount, s.category, u.name from spends as s join users as u on u.id=s.user_id order by s.time;")
records = cur.fetchall()
cur.close()
conn.close()
result = []
result.append(('|{:^19} | {:^13}  | {:^30} | {:^20}|'.format('дата и время', 'сумма', 'категория', 'имя')))
result.append('----------------------------------------------------------------------------------------------')
sum = 0
for i in records:
    result.append('|{} | {:^13}т.| {:^30} | {:^20}|'.format(*i))
    sum += decimal.Decimal(i[1])
result.append('----------------------------------------------------------------------------------------------')
result.append('|{:^19} | {:^13}т.| {:^30} | {:^20}|'.format('Итого', sum, '', ''))
result.append('----------------------------------------------------------------------------------------------')
with open('spends.txt', 'w') as f:
    f.write('\n'.join(result))
# cur.execute("select date_trunc('day', s.time) as date, sum(s.amount), s.category, u.name from spends as s join users as u on u.id=s.user_id group by date order by s.time;")

