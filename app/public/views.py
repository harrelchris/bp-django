from django.template.response import TemplateResponse

from . import selectors


def index(request):
    return TemplateResponse(
        request=request,
        template="public/index.html",
    )


def privacy(request):
    return TemplateResponse(
        request=request,
        template="public/privacy.html",
    )


def terms(request):
    return TemplateResponse(
        request=request,
        template="public/terms.html",
    )


def about(request):
    return TemplateResponse(
        request=request,
        template="public/about.html",
    )


def contact(request):
    return TemplateResponse(
        request=request,
        template="public/contact.html",
        context={
            "form": selectors.get_contact_form(request=request),
        },
    )


def faq(request):
    return TemplateResponse(
        request=request,
        template="public/faq.html",
        context={
            "questions": selectors.get_frequent_questions(),
        },
    )
