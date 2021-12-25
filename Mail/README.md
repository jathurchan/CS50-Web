# Mail

Designed a front-end for an email client that makes API calls to send and receive emails.

> *Everything I added to the distribution code is only in `inbox.js` and `index.html`*.

## Used

- Javascript
- HTML
- CSS

## Running Locally

1. Download the folder `Mail`.
2. In your terminal, `cd` into the `Network` directory.
3. Run `python manage.py makemigrations network` to make migrations for the `network` app.
4. Run `python manage.py migrate` to apply migrations to your database.
5. Run `python manage.py runserver` to start up the Django web server.
6. Visit the website in your browser.

## Features

- [x] **Send Mail**: When a user submits the email composition form, add JavaScript code to actually send the email.
- [x] **Mailbox**: When a user visits their Inbox, Sent mailbox, or Archive, load the appropriate mailbox.
- [x] **View Email**: When a user clicks on an email, the user should be taken to a view where they see the content of that email.
- [x] **Archive and Unarchive**: Allow users to archive and unarchive emails that they have received.
- [ ] **Reply**: Allow users to reply to an email.

