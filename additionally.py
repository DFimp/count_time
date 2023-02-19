days_in_month = [31, [28, 29], 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
title_month = ['янв', 'фев', 'март', 'апр', 'май', 'июнь', 'июль', 'авг', 'сен', 'окт', 'ноя', 'дек']
title_day_in_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
full_title_day_in_week = ['Понедельник',
                          'Вторник',
                          'Среда',
                          'Четверг',
                          'Пятница',
                          'Суббота',
                          'Воскресенье']


def check_leap_year(month, year):
    if month == 1:
        if year % 4 == 0:
            return days_in_month[month][1]
        else:
            return days_in_month[month][0]
    else:
        return days_in_month[month]