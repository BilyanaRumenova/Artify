from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


# def landing_page(request):
#     return render(request, 'landing_page.html')
