document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Update the style of emails-view
  document.querySelector('#emails-view').classList.add('list-group');

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

   // Mailbox
   fetch(`/emails/${mailbox}`)
   .then(response => response.json())
   .then(emails => {

     // Print emails
     console.log(emails);

     // Show mails

     emails.forEach(email => {

       document.querySelector('#emails-view').classList.add('list-group');

       const element = document.createElement('a');
       element.classList.add('list-group-item', 'list-group-item-action');
       element.href = '#'

       // Color the elements (Read?)
       if (email.read === true) {
         console.log(email.read);
         element.style.backgroundColor = '#f5f5f5';
       } else {
         element.style.backgroundColor = '#fff';
       }

       const innerEl = document.createElement('div');
       innerEl.classList.add('d-flex', 'w-100', 'justify-content-between');

       const left = document.createElement('div');
       left.classList.add('d-flex');

       const sender = document.createElement('b');
       sender.innerHTML = email.sender;
       sender.style.paddingRight = '10px';
       sender.bold 

       const subject = document.createElement('p');
       subject.innerHTML = email.subject;
       left.append(sender, subject)

       const timestamp = document.createElement('p');
       timestamp.innerHTML = email.timestamp;

       innerEl.append(left)
       innerEl.append(timestamp);
       element.append(innerEl);
       document.querySelector('#emails-view').append(element);

     });


   });
}

function send_mail() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  })
}