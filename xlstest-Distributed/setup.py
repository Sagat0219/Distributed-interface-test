# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='xlstest-Distributed',
    version='1.0',
    packages = find_packages(),
    package_data = {'':['case/*.xlsx']},
    entry_points = {'scrapy':['settings=xlstest.settings']},
)