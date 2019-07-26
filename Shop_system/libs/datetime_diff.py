import datetime

def month_diff(start, end):
    """
    计算两个date之间的月份差
    start: 开始date
    end: 结束date
    """
    # excel中，结束日期 = 开始日期+年/月-1天
    end = end + datetime.timedelta(days=1)
    return (end.year-start.year)*12+(end.month-start.month)


def season_diff(start, end):
    """
    计算两个date之间的季度差
    start: 开始date
    end: 结束date
    """
    return month_diff(start, end)//3


def year_diff(start, end):
    """
    计算两个date之间的年度差
    start: 开始date
    end: 结束date
    """
    return month_diff(start, end)//12