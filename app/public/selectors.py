from django.contrib import messages

from . import forms, models


def get_frequent_questions():
    return models.FrequentlyAskedQuestion.objects.all()


def get_contact_form(request):
    if request.method == "POST":
        form = forms.ContactForm(data=request.POST)
        if form.is_valid():
            contact_form = form.save(commit=False)
            if request.user.is_authenticated:
                contact_form.user = request.user
            contact_form.save()
            messages.success(request, "Your message has been sent.")
    else:
        form = forms.ContactForm()
    return form
