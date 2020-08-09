from datetime import datetime
from random import randint
year_of_passing = []
possible_year = range(1990,int(datetime.now().strftime("%Y")) + 1)
def year_of_passing_fun():
    for years in possible_year:
        year = str(years),str(years)
        year_of_passing.append(year)
    return year_of_passing

def otp_generate():
    return str(randint(1000,9999))