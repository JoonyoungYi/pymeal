from pymeal import School
from datetime import date, timedelta

school = School('GYEONGGI', 'J100000833', '4')

print(school.getWeeklyMeal(date.today() + timedelta(weeks=1), replace='급식이 없어요ㅠㅠ', regex=r'[가-힣][가-힣\s\/]+'))