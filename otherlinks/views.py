from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from .models import Contact


def about_us(request):
    """View to return shipping and returns info page"""
    return render(request, 'about/about_us.html')


def contact_us(request):
    """View to return contact us page"""
    # Help from Scottish Coder YouTube Tutorial - link in README
    if request.method == 'POST':
        # Send contact form to Gmail Account
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        instance = Contact(name=name, email=email, subject=subject,
                           message=message)
        instance.save()

        message_data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        message = '''
        From: {}
        New message: {}
        '''.format(message_data['email'], message_data['message'])

        send_mail(
            message_data['subject'], message, '', ['jcfahey007@gmail.com'])

        messages.info(request, (
            f'Thanks, your message has been received, we will contact you \
                via { email } as soon as possible.'))
        return render(request, 'home/index.html')

    return render(request, 'contact/contact_us.html')
