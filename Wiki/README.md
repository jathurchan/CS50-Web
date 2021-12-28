# Wiki

Designed a Wikipedia-like online encyclopedia.

## Used

- Python
- HTML
- CSS

## Demo (YouTube)

[Wiki - CS50-Web-Harvard](https://www.youtube.com/watch?v=xmsaLCAON20&feature=youtu.be)

## Running Locally

1. Download the folder `Wiki`.
2. In your terminal, `cd` into the `Wiki` directory.
3. Install [python-markdown2](https://github.com/trentm/python-markdown2) package (`pip3 install markdown2`).
4. Run `python manage.py makemigrations network` to make migrations for the `network` app.
5. Run `python manage.py migrate` to apply migrations to your database.
6. Run `python manage.py runserver` to start up the Django web server.
7. Visit the website in your browser.

## Features

- [x] **Entry Page**: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
- [x] **Index Page**: Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.
- [x] **Search**: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
- [x] **New Page**: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
- [x] **Edit Page**: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
- [x] **Random Page**: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
- [x] **Markdown to HTML Conversion**: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. (*python-markdown2 package*)

