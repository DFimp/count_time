import json


days_in_month = [31, [28, 29], 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def fill_past_date(date):
    try:
        with open('data_time.json') as file:
            data_file = json.load(file)

        while date not in data_file.keys():
            data_file[date] = {}

            year, month, day = list(map(int, date.split('-')))

            if day > 1:
                day -= 1
            else:
                if month > 1:
                    month -= 1
                    if month == 2:
                        if year % 4 == 0:
                            day = days_in_month[month - 1][1]
                        else:
                            day = days_in_month[month - 1][0]
                    else:
                        day = days_in_month[month - 1]
                else:
                    year -= 1
                    month = 12
                    day = days_in_month[month - 1]

            date = str(year) + '-' + '0' * (2 - len(str(month))) + str(month) + '-' + '0' * (2 - len(str(day))) + str(day)

        data_file = dict(sorted(data_file.items(), key=lambda x: x))

    except:
        data_file = dict()
        data_file['decoding'] = {}
        data_file[date] = {}

    with open('data_time.json', 'w') as file:
        file.write(json.dumps(data_file, indent=4))