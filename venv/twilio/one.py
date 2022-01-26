from datetime import datetime

def strip_date(date):
    return date.replace('-','')
def update_date(date):
    return datetime.strptime(date, '%Y%m%d').strftime('%d%m%Y')
def actual_date(date):
    return str(date[0:2]+'/'+date[2:4]+'/'+date[4:])

begin = '2022-01-15'
end = '2022-01-16'

def date(date):
    date = strip_date(date)
    date = update_date(date)
    return actual_date(date)

begin = date(begin)
end = date(end)

print(begin)
print(end)