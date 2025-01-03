import random
from random import randrange
from datetime import timedelta, datetime


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


d1 = datetime.strptime('1/1/2023 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('5/23/2024 4:50 AM', '%m/%d/%Y %I:%M %p')

for i in range(100):
    print(random.randint(0, 392))