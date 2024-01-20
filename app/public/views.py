import logging

from django.template.response import TemplateResponse

logger = logging.getLogger("app")


def index(request):
    logger.debug("Debug log")
    logger.error("Error log")
    return TemplateResponse(
        request=request,
        template="public/index.html",
        context={},
    )
