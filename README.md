dummy
=====

coding tasks and exercises

1) "As an exercise to show your abilities we would like to see the following. 
You can use Ruby or Python (or something else if you see fit but considerable credit will be deducted for using PHP)
Write a small dummy web server that returns search results - url, date, some example metadata. 
These can be "pre canned" ie. the search results are hardwired into the code. 
There is no need for any actual search behaviour to take place - just that a query returns a list of results.
Produce a client for displaying the results. 
The client should run in an ordinary web browser (assume we will be using latest chrome to avoid cross platform issues). 
The user should be able to enter a search term and get a list of results back. 
The results should be able to be re-ordered (ie. sort by date, sort by the ranking etc.). 
The display of the results should implement proper paging behaviour. 
An extension - in place of a simple search form, put an "Advanced" query builder to construct more complex queries 
(see Google for example). 
As the user builds the query, update a text box showing what the query would look like in the query language.
-------------------------------------------------------------------------------------------------------------------

I realized this task using a django project called "dummy" and an application called "search".
-------------------------------------------------------------------------------------------------------------------
Requirements:
django 1.4,
mysql-server 5.5,
python-mysqldb 1.2,
python 2.7,
django_tables2
-------------------------------------------------------------------------------------------------------------------

It might work with different versions.

Install everything than create a database "dummy" in mysql; 
then mysql -u user -p < dummy.sql; 
configure dummy/settings.py with your db credentials; 
start server with python manage.py runserver 8080 or whatever port and url you like; 
access via browser http://localhost:8080/search to start; 
actually only a few fake websites has been inserted in db. 
you can test the functionalities with keywords like python, news.... 
try searching something strange to have a list of all configured sites. 
rank will be calculated adding a rank value for every keyword configured for each site. 
A working server is running @ http://199.175.51.240:8080/search/ 
