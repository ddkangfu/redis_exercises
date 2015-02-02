from django.views.generic import TemplateView

from redis_exercises.settings import redis_con


class  MainView(TemplateView):
    template_name = "main/main.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        if name:
            redis_con.set('name', name)
        return super(MainView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MainView, self).get_context_data(**kwargs)
        ctx['name'] = redis_con.get('name')
        return ctx

class RegisterView(TemplateView):
    template_name = 'main/register.html'
