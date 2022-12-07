def transformation(time_in_second):
    hours = str(time_in_second // 3600)
    minutes = str((time_in_second % 3600) // 60)
    seconds = str(time_in_second % 60)

    time = '0' * (2 - len(hours)) + hours + ':' + '0' * (2 - len(minutes)) + minutes + ':' + '0' * (2 - len(seconds)) + seconds

    return time
