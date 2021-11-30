# doobara online shop

![Twitter Follow](https://img.shields.io/twitter/follow/doobarashop?style=social)

A template for a online shop website, the site based design is for a home automation product site. 
The template is mobile responsive. 
The site is built with django framework, using html, css, sass, js for front end  and python and django fw for backend, 

# Requirements

to get started and edit, add or cutomize this web application locally, you need:

* Install [Python](https://www.python.org/downloads/) 3.9.2

Running Django applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with:

```bash
pip install -r requirements.txt
```

To run your application locally:

```bash
python manage.py runserver
```
 
 To run live reload 
 
 ```bash
 python manage.py livereload
 ```

Sass version is 1.38.2 and The sass codes include the `@use` syntax so the vcode sass plugin wont 
compile the `@use` the sass is included in the requirement file, the version most be 1.3+ so to run 
and watch sass type
```bash
cd doobarashop/static/doobarashop
```
then
```
sass --watch main.sass style.css
```
