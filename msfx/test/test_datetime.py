from datetime import timedelta, datetime

time_difference = timedelta(hours=5, minutes=30, seconds=15)
time_of_day = (datetime.min + time_difference).time()
print(time_of_day)
# Output: 05:30:15
