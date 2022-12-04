import json


days_in_month = {
    1: 31,
    2: [28, 29],
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def fill_past_date(date):
    with open('data_time.json') as file:
        try:
            data_file = json.load(file)

            # for key, val in data_file.items():
            #     if val is None:
            #         data_file[key] = {}

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
                                day = days_in_month[month][1]
                            else:
                                day = days_in_month[month][0]
                        else:
                            day = days_in_month[month]
                    else:
                        year -= 1
                        month = 12
                        day = days_in_month[month]

                date = str(year) + '-' + '0' * (2 - len(str(month))) + str(month) + '-' + '0' * (2 - len(str(day))) + str(day)

            data_file = dict(sorted(data_file.items(), key=lambda x: x))

        except:
            data_file = dict()
            data_file[date] = {}

    with open('data_time.json', 'w') as file:
        file.write(json.dumps(data_file, indent=4))