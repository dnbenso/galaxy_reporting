#!/usr/bin/env python3
"""Queries galaxy database for given month for Workflows, Jobs, Datasets"""

import argparse
import psycopg2

# Define set queries - second last item in query is tag for table heading
QALL = "SELECT x.id,"
QJ = "x.create_time FROM job x"
QW = "x.create_time FROM stored_workflow x"
QD = "x.create_time, x.total_size FROM dataset x"
QRY = [QJ, QW, QD]


def next_month(month, year):
    """Returns next month in format mm-yyyy"""
    if month == "12":
        return "{}-01".format(int(year) + 1)
    else:
        return "{1}-{0:02d}".format(int(month) + 1, year)

def db_connect(db_name, db_user, host, port):
    """Returns connection cursor to database"""
    dsn = "dbname={} user={} host={} port={}".\
        format(db_name, db_user, host, port)
    return psycopg2.connect(dsn)

def db_query(cursor, sql_query):
    """Modifies the cursor object after query: sql_query"""
    cursor.execute(sql_query)

def print_query_results(cursor):
    """Prints the results in cursor line by line"""
    for row in cursor:
        print(row)

def get_query_limit(month, year):
    """Returns SQL query limit for monthly stats given current month and year"""
    start_date = "{1}-{0:02d}-01".format(int(month), year)
    end_date = "{}-01".format(next_month(month, year))
    return "WHERE x.create_time >= '{0}' and x.create_time < '{1}'".\
        format(start_date, end_date)

def perform_queries_from_month(query_list, month, year):
    """Takes a list of SQL queries and performs them for given month"""
    conn = db_connect("galaxy", "galaxy", "localhost", "5930")
    cur = conn.cursor()
    qlmt = get_query_limit(month, year)
    results = ["{:<16}".format("-".join([year, month]))]
    for query in query_list:
        db_query(cur, "{} {} {}".format(QALL, query, qlmt))
        results.append("{:<16d}".format(cur.rowcount))
    print(''.join(results))
    cur.close()
    conn.close()

def print_heading(query_list):
    """Print column headings for output"""
    heading = ["{:<16}".format('month')]
    for item in query_list:
        heading.append("{:<16}".format(item.rsplit(None, 2)[-2]))
    print(''.join(heading))

def main():
    """Sets todays date and prints start and end date"""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command')
    month_parser = subparsers.add_parser(
        'month', help=perform_queries_from_month.__doc__)
    month_parser.add_argument('month')
    month_parser.add_argument('year')

    subparsers.add_parser('heading', help=print_heading.__doc__)

    args = parser.parse_args()

    if args.command == 'heading':
        print_heading(QRY)
    elif args.command == 'month':
        perform_queries_from_month(QRY, args.month, args.year)

if __name__ == '__main__':
    main()

