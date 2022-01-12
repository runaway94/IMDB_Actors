# IMDB Actors
## Description
In this application you can scrape information about the top 50 most popular actors and actresses from a IMDb website.
Afterwards you can analyze the information about each actor, their movies and awards.

## Technologies
The project is created with:
* Python version: 3.8

## Modules
The following modules are used in this project and need to be installed eventually

* MySQL 
  * Please make sure MySQL is installed on your computer [Download MySQL database](https://www.mysql.com/downloads/)
  
  * install MySQL Driver `` pip install mysql-connector-python``

* hashlib `` pip install hashlib ``

* BeautifulSoup ``pip install beautifulsoup4``
* request ``pip install requests``
* pandas ``pip install pandas``
* pylab ``pip install pylab``
* matplotlib ``pip install matplotlib``
* wordcloud ``pip install wordcloud``
* flask ``pip install flask``

## Setup
Start the application by starting the IMDb.py module.
You can use the following commands:
* ``--start`` Starts from scratch. Tells you exactly what you need to do next step by step.
* ``--help`` Shows help and all possible commands
* ``--configure`` Configure the database connection
* ``--scrape`` Starts scraping the data from the imdb page
* ``--show`` Starts web application on http://127.0.0.1:5000/
* ``--exit`` Ends the application

Please make sure that you configure your database connection and scrape the information before you start the web application.
To start from scratch, just use the ``--start`` command.

