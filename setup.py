from setuptools import setup, find_packages

install_requires = [
	'requests'
]

setup(
	name='pymeal',
	version='0.3',
	description='초중고 급식 Python 라이브러리',
	author='Son Minseok',
	author_email='tom20001229@gmail.com',
	url='https://github.com/tom5079/pymeal',
	install_requires=install_requires,
	packages=find_packages(exclude=['tests']),
	python_requires='>=3',
	zip_safe=False
)