import logging

from django.views.generic import TemplateView

logger = logging.getLogger("app")


class IndexView(TemplateView):
    template_name = "public/index.html"

    def get(self, request, *args, **kwargs):
        logger.debug("Debug log")
        logger.error("Error log")
        return super().get(request, *args, **kwargs)
