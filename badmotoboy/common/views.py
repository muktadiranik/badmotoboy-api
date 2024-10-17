from django.shortcuts import render, redirect
from badmotoboy.common.models import *
from django.contrib import messages
from .forms import ContactForm


def privacy_policy(request):
    privacy_policies = PrivacyPolicy.objects.all()
    return render(request, 'common/privacy_policy.html', {'privacy_policies': privacy_policies})


def terms_and_conditions(request):
    terms_and_conditions = TermsAndConditions.objects.all()
    return render(request, 'common/terms_and_conditions.html', {'terms_and_conditions': terms_and_conditions})


def contact_us(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully')
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'common/contact.html', {'form': form})
