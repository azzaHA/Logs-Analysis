#!/usr/bin/python

import psycopg2


def run_query(cursor, query):
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def run():
    first_query = '''select title, views from article_views
order by views desc
limit 3;
'''
    second_query = '''select name, s
from authors, author_total_views
where authors.id = author_total_views.author
order by s desc;'''

    third_query = '''select day, to_char(to_timestamp (month::text, 'MM'),
'TMMonth') as month, year,
 round (error_percent, 2)||'%'  as error_percent
from daily_error_percent
where error_percent > 1.0;'''

    db = psycopg2.connect(database='news')
    cursor = db.cursor()

    popular_3_articles = run_query(cursor, first_query)
    most_popular_authors = run_query(cursor, second_query)
    error_stat = run_query(cursor, third_query)

    db.close()

    print('The most popular three articles of all time are:')
    for title, views in popular_3_articles:
        print('"%s" - %d views' % (title, views))
    print('')

    print('The most popular authors of all time are:')
    for name, views in most_popular_authors:
        print('"%s" - %d views' % (name, views))
    print('')

    print('On these days, more than 1% of requests led to errors:')
    for d, m, y, error in error_stat:
        print('%s %d, %d - %s errors' % (m, d, y, error))


run()
