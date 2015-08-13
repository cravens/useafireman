from django.shortcuts import render

# Create your views here.

from django.template import Context, loader

from django.shortcuts import render_to_response, RequestContext

import datetime
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import (HttpResponseRedirect, Http404,
                         HttpResponsePermanentRedirect)
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template

from django import forms
import UAF.models

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

#from apiclient import errors


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  #try:
  message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
  print 'Message Id: %s' % message['id']
  return message
  #except errors.HttpError, error:
    #print 'An error occurred: %s' % error


def CreateMessage(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.b64encode(message.as_string())}


def CreateMessageWithAttachment(sender, to, subject, message_text, file_dir,
                                filename):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject

  msg = MIMEText(message_text)
  message.attach(msg)

  path = os.path.join(file_dir, filename)
  content_type, encoding = mimetypes.guess_type(path)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(path, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(path, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(path, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(path, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()

  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.b64encode(message.as_string())}


class PostForm(forms.Form):
    content = forms.CharField(max_length=256)
    created_at = forms.DateTimeField()

def index(request, current_email):
    #your stuff goes here
    #form = ContactForm(request.post or None)

    #if form.is_valid():
    subject = "Thank you for your interest in Use A Fireman!"
    htmly = get_template('Landing.html')
    d = Context({ 'current_email': current_email })
    from_email = settings.EMAIL_HOST_USER
    to = current_email
    html_content = htmly.render(d)
    #msg.attach_alternative(html_content, "text/html")
    #msg.send()
    message = CreateMessage(from_email, to, subject, html_content)
    #send_mail(subject, msg, from_email, to, fail_silently=False)
    SendMessage()
    return HttpResponseRedirect("email.html")
    return render_to_response('Landing.html', locals(), context_instance = RequestContext(request))


def emailview(request):
    return render_to_response('email.html', locals(), context_instance = RequestContext(request))

def PrivPol(request):
        return render_to_response('privacypolicy.html', locals(), context_instance = RequestContext(request))
