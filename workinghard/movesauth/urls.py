from django.conf.urls import url
from workinghard.movesauth import views

urlpatterns = [
    url(r'^$', 'workinghard.movesauth.views.index', name='index'),
    url(r'^redirect/$', 'workinghard.movesauth.views.redirect_view', name='redirect'),
    url(r'^workplace/$', 'workinghard.movesauth.views.select_work_place', name='select_work_place'),
]
