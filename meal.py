from pymeal.constants import REGION, PATH, WEEKDAY

import requests
import json

class School:
	__cookies = {
		'WMONID': '',
		'JSESSIONID': '',
		'schulCode': '',
		'schulCrseScCode': ''
	}
	def __init__(self, region, schoolCode, schoolCrseScCode):
		self.base_url = REGION[region]
		self.__cookies['schulCode'] = schoolCode
		self.__cookies['schulCrseScCode'] = schoolCrseScCode
		
		self.__newCookie()
	
	def __newCookie(self):
		cookies = requests.get(self.base_url + PATH.MAIN).cookies
		self.__cookies['WMONID'] = cookies['WMONID']
		self.__cookies['JSESSIONID'] = cookies['JSESSIONID']
	
	def getMonthlyDiet(self, date):
		diet = dict()
		
		payload = {
			'ay': date.strftime('%Y'),
			'mm': date.strftime('%m'),
			'schulCode': self.__cookies['schulCode'],
			'schulCrseScCode': self.__cookies['schulCrseScCode']
		}
		
		r = requests.post(self.base_url+PATH.MONTHLY_DIET, cookies=self.__cookies, json=payload)
		
		for mthDietList in r.json()['resultSVO']['mthDietList']:
			for weekday in WEEKDAY:
				temp = mthDietList[weekday].replace('<br />', '\n')
				
				if temp is ' ':
					continue
				
				temp = temp.split('\n', 1)
				
				diet[int(temp[0])] = temp[1] if len(temp) == 2 else ''
		
		return diet
	
	def getWeeklyDiet(self, date):
		diet = list()
		r = list()
		
		payload = {
			'schYmd': date.strftime('%Y%m%d'),
			'schMmealScCode': '',
			'schulCode': self.__cookies['schulCode'],
			'schulCrseScCode': self.__cookies['schulCrseScCode']
		}
		
		for i in range(3):
			payload['schMmealScCode'] = str(i+1)
			r.append(requests.post(self.base_url+PATH.WEEKLY_DIET, cookies=self.__cookies, json=payload).json())
		
		for weekday in WEEKDAY:
			temp = dict()
			menu = list()
			
			temp['date'] = r[0]['resultSVO']['weekDietList'][0][weekday]
			
			for i in range(3):
				_temp = dict()
				
				_temp['menu'] = r[i]['resultSVO']['weekDietList'][2][weekday].replace('<br />', '\n') if len(r[i]['resultSVO']['weekDietList']) is 3 else ''
				_temp['cal'] = r[i]['resultSVO']['dietNtrList'][0]['dy{}'.format(3 if weekday == 'sun' else WEEKDAY.index(weekday) + 4)]
				
				menu.append(_temp)
			
			temp['menu'] = menu
			
			diet.append(temp)
		
		return diet