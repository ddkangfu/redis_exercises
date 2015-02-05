
import time

from django.views.generic import TemplateView, CreateView
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from redis_exercises.settings import redis_con

from .forms import CreateUserForm


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
        ctx['users'] = redis_con.hkeys('users:name')
        ten_minutes_ago = time.time() - (10 * 60)
        ctx['online_users'] = redis_con.zrangebyscore('users.online', ten_minutes_ago, '+inf')
        return ctx

class RegisterView(TemplateView):
    template_name = 'main/register.html'

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            #ID: users:count, Hash: {users:name:  #id}, Data: user:#id
            #print dir(redis_con)
            is_exist = redis_con.hexists('users:name', username)
            if not is_exist:
                #pipe =redis_con.pipeline()
                user_id = redis_con.incr('users:count')
                redis_con.hset('users:name', username, user_id)
                redis_con.hmset('user:%d' % user_id, {'password': form.cleaned_data['password1']})
                #result=pipe.execute()

            return HttpResponseRedirect(reverse('home'))
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(RegisterView, self).get_context_data(**kwargs)
        ctx['form'] = CreateUserForm
        return ctx