dummy
=====

coding tasks and exericises

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

I realized this task using a django application which I called search.
Requirements are:
django 1.4\n
mysql-server 5.5
python-mysqldb 1.2
python 2.7
django_tables2
