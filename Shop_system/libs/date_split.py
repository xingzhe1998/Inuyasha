import calendar
import datetime

MONTH = 1
SEASON = 3
YEAR = 12


def next_month(d):
    """
    返回月份比d多一个月的新日期
    d: date
    """
    # 每月天数
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # 到下一个月需要加的天数
    delta = days[d.month-1]
    # 闰年2月加一天
    if calendar.isleap(d.year) and d.month == 2:
        delta += 1
    return d+datetime.timedelta(days=delta)


def month_range(start, end, step=1):
    """
    返回[start, end)之间的date,每隔step月
    start, end : date
    step : int > 0
    """
    current_date = start
    while current_date < end:
        yield current_date
        for i in range(step):
            current_date = next_month(current_date)


def month_split(start, end, step=1):
    """
    将[start,end]时间分割成N个时间段，每个时间段有step月
    每个时间段是一个(时间段开始，时间段结束)的元组
    start,end : date
    step : int > 0
    """
    tmp = []
    for i in month_range(start, end, step):
        if len(tmp) == 1:
            tmp.append(i-datetime.timedelta(days=1))
            yield tuple(tmp)
            tmp.clear()
        tmp.append(i)
    if len(tmp) == 1:
        yield (tmp[0], end)
        
if __name__ == "__main__":

    start = datetime.date.today()
    print(type(start))
    end = start + datetime.timedelta(days=365)
    print(end)
    print(month_split(start, end,step=SEASON))
    # for item in month_split(start, end,step=SEASON):
    #     print(item)