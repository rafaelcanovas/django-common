from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator


def send_template_mail(subject, template, context, to, fail_silently=False):
    email = EmailMultiAlternatives(subject=subject, to=to)
    c = Context(context)

    if 'txt' in template:
        email.body = render_to_string(template, c)

    if 'html' in template:
        html = render_to_string(template, c)
        email.attach_alternative(html, 'text/html')

    return email.send(fail_silently=fail_silently)
