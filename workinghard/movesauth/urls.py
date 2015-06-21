from django.conf.urls import url
from workinghard.movesauth import views

urlpatterns = [
    url(r'^$', 'workinghard.movesauth.views.start', name='start'),
    url(r'^redirect/$', 'workinghard.movesauth.views.redirect_view', name='redirect'),
]
