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
Now we are ready to edit.

# Structure 

doobara django project includes doobarashop application where the web application lives.
doobara shop application serves the HTML pages structure and layout templates, the sass structure styling, the JS files and the python server modules.

## Main Contents
- [doobara](#doobara)
    - [doobarashop](#doobarashop)
        - [static](#static)
            - [sass](#sass)
            - [uploads](#uplads)
            - [css](#getting-started)
            - [libraries](#getting-started)
        - [templates](#getting-started)
            - [html layout](#layout)
            - [html pages template](#getting-started)
        - [urls](#getting-started)
        - [views](#getting-started)
        - [tests](#getting-started)

## doobara 
Is the main project container, currently there is one application which the website application doobarashop. (of course I wont mention the default django file which you should be familiar with. Also these file are updated and edited to fit the project requerment and settings, for example the urls and setttings file)

## doobarashop
The website application folder container. Here you can find the html templates, sass style, js file, and python codes in several files. 


## Static 
Static is the home folder of sass, css, js, files and media library.

## SASS
sass is the folder of sass files structures tree, the sass tree streams to one sass file which main.sass and the sass compiles main.sass to style.css, that way there is only one css file to load when the web application loads. 
the sass structure is of many layers explained as possible below 
- [abstracts]
    - [variables]
    - [mixins]
    - [extention]
- [componenets]
    - [folders for each page]
        - [compenents in each page]
- [core]
    - [reset]
    - [typography]
- [layout]
    - [each section in the page]
    - [grid layout]
- [pages]
    - [file for each page]
- [sections]
    - [hero]
- [single]
    - [single pages files]


## Uploads 
All media that are used in the webapplication, like:
Icons, Images, and videos

## css 
nothing is done in css because the sass is where all the work is, and the css file is being take cared by the sass compiler. though it is here :P. also most of the syntax used in sass are css syntax, though the sass help in organizing and break down the style in categories and componenet for better and easy maintenance.  

## Libraries 
Only useng the webfont fontawesome for icons.

## templates 
this folder contain the html templates structure and design layout

## layout
the layout file is where all the static components that are the same on all pages, 
the header, footer and the body style and properties, and the grid layout.

## pages
these the rest of the html files that extends the layout design, each page has different componenets 
and body layout structure, page are: index, shop, blog, video, contact, account, cart, checkout, resgiter and login, single product, single blog.

## urls 
this is django python file for the path and binding view of each page in the website

## views 
Is the main back end file where the moduler function of each page and any dynamic action in the backend, like database process from login to products and blogs. 


## Authentiaction 
user registration and login uses email address login and social media login specifically google and faceboo. 
for authentication will django-allauth. 

