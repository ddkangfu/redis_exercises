from django.views.generic import TemplateView

from redis_exercises.settings import redis_con


class  MainView(TemplateView):
    template_name = "main/main.html"

    #def dispatch(self, request, *args, **kwargs):
    #    self.redis_con = 
    #    return super(MainView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MainView, self).get_context_data(**kwargs)
        ctx['name'] = redis_con.get('name')
        return ctx

