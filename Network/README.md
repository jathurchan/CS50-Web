# Network

Designed a Twitter-like social network website for making posts and following users.

## Used

- Python
- Javascript
- HTML
- CSS

## Running Locally

1. Download the folder `Network`.
2. In your terminal, `cd` into the `Network` directory.
3. Run `python manage.py makemigrations network` to make migrations for the `network` app.
4. Run `python manage.py migrate` to apply migrations to your database.
5. Run `python manage.py runserver` to start up the Django web server.
6. Visit the website in your browser.

## Features

- [x] **New Post**: Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
- [x] **All Posts**: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
- [x] **Profile Page**: Clicking on a username should load that user’s profile page. This page should:
- [x] **Following**: The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.
- [x] **Pagination**: On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.
- [x] **Edit Post**: Users should be able to click an “Edit” button or link on any of their own posts to edit that post.
- [x] **“Like” and “Unlike”**: Users should be able to click a button or link on any post to toggle whether or not they “like” that post.

