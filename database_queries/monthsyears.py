#!/usr/bin/env python3
'''
Created on 21Aug.,2017
Performs query of galaxy database for this year and last year.
@author: derek
'''

from datetime import date
from database_queries import perform_queries_from_month
from database_queries import print_heading

# Define set queries - last item in query is tag for table heading
QALL = "SELECT x.id,"
QJ = "x.create_time FROM job x"
QW = "x.create_time FROM stored_workflow x"
QD = "x.create_time, x.total_size FROM dataset x"
QRY = [QJ, QW, QD]

def main():
    """Call functions to generate list of months and years and call query"""
    today = date.today()
    print_heading(QRY)
    last_year = today.year - 1
    for month in range(1, 13):
        perform_queries_from_month(QRY, str(month), str(last_year))
    for month in range(1, today.month):
        perform_queries_from_month(QRY, str(month), str(today.year))

if __name__ == '__main__':
    main()

