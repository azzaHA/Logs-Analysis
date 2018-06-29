# Logs Analysis
Logs Analysis is a reporting tool for a newspaper site with an already built database. It uses information from the database to discover what kind of articles the site's readers like more.
# Prerequisites
1. [Python2.7](https://www.python.org/download/releases/2.7/)
2. [PostgreSQL](https://www.postgresql.org/download/)

# Installation & Run
1. Download/Clone the zip file.
2. Open the command-line shell, and navigate to the project directory
3. Run:
```
python logs-analysis.py
```

# Technical Details
Python code connects to the "news" database and runs the queries to fetch the answers to these questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

To have the answers in one query, views are created to help organize code.

### Views:
#### To answer 1st question:
###### article_views view:
create view article_views as  
select title, author, count(*) as views  
from articles, log  
where log.path = '/article/' || slug  
group by title, author;

#### To answer 2nd question:
###### author_total_views view:
create view author_total_views as  
select author, sum(views) as s  
from article_views  
group by author  
order by s desc;

#### To answer 3rd question:
###### success_stat view:
create view success_stat as  
select extract (day from time) as day,  
extract(month from time) as month,  
extract (year from time) as year,  
count(*) as success  
from log where status ='200 OK'  
group by year, month, day  
order by day;

###### error_stat view:
create view error_stat as  
select extract (day from time) as day,  
extract(month from time) as month,  
extract (year from time) as year,  
count(*) as error  
from log where status ='404 NOT FOUND'  
group by year, month, day, month  
order by day;

###### daily_error_percent view:
create view daily_error_percent as  
select success_stat.day, success_stat.month, success_stat.year,   error*100.0/(success+error) as error_percent  
from success_stat, error_stat  
where success_stat.day = error_stat.day  
and success_stat.month = error_stat.month  
and success_stat.year = error_stat.year;
