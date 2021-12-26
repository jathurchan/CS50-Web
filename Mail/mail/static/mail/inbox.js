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
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
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

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Print emails
    console.log(emails);

    // Show emails

    emails.forEach(email => {
      
      // element = representation of an email
      const element = document.createElement('button');
      element.classList.add('list-group-item', 'list-group-item-action');

      // View mail by clicking on the element
      element.onclick = () => view_mail(email.id, mailbox);

      // Determine the background color of the element (read or not?)
      if (email.read === true) {
        console.log(email.read);
        element.style.backgroundColor = '#f5f5f5';
      } else {
        element.style.backgroundColor = '#fff';
      }

      // Filling up the element with sender, subject and timestamp

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

function view_mail(email_id, mailbox) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear email-view
  document.querySelector('#email-view').innerHTML = '';

  // Mail
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Print email
    console.log(email);

    // Show elements (UI)

    const sender = document.createElement('p');
    sender.innerHTML = `<b>From:</b> ${email.sender}`;
    
    const recipients = document.createElement('p');
    recipients.innerHTML = `<b>To:</b> ${email.recipients}`;

    const subject = document.createElement('p');
    subject.innerHTML = `<b>Subject:</b> ${email.subject}`;;

    const timestamp = document.createElement('p');
    timestamp.innerHTML = `<b>Timestamp:</b> ${email.timestamp}`;

    const emV = document.querySelector('#email-view');
    emV.append(sender, recipients, subject, timestamp);

    // Reply

    const replyB = document.createElement('button');
    replyB.classList.add('btn', 'btn-sm', 'btn-outline-primary');
    replyB.innerHTML = 'Reply'
    replyB.style.marginRight = "5px";
    replyB.onclick = () => reply_email(email);
    emV.append(replyB);

    // Archive / Unarchive

    if (mailbox != 'sent') {
      const archiveB = document.createElement('button');
      archiveB.classList.add('btn', 'btn-sm', 'btn-outline-primary');
      if (email.archived) {
        archiveB.innerHTML = 'Unarchive'
      } else {
        archiveB.innerHTML = 'Archive'
      }
      archiveB.onclick = () => toggle_archive(email.id, email.archived);
      emV.append(archiveB);
    }

    const line = document.createElement('hr');
    emV.append(line);

    const body = document.createElement('p');
    body.innerHTML = email.body;

    emV.append(body);

    // Mark as read

    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

  })

}

function toggle_archive(email_id, archived) {
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !archived
    })
  })

  load_mailbox('inbox');
}

function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Fill up composition fields for reply

  document.querySelector('#compose-recipients').value = email.sender;

  subject = email.subject;
  if (!subject.startsWith("Re: ")) {
    subject = "Re: ".concat(subject);
  }
  document.querySelector('#compose-subject').value = subject;

  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`;

}