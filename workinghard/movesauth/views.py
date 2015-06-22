from os import environ
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .movesclient import Moves, InvalidGrant, MovesSegmentList
from .models import Token

moves = Moves(settings.MOVES_CLIENT_ID,
              settings.MOVES_CLIENT_SECRET)

@login_required
def index(request):
    redirect_uri = request.build_absolute_uri(
            reverse('movesauth:redirect'))

    if not hasattr(request.user, 'token'):
        return redirect(moves.get_auth_uri(redirect_uri))

    elif request.user.token.has_expired():
        try:
            request.user.token.refresh()
        except InvalidGrant, e:
            request.user.token.delete()
            return redirect(moves.get_auth_uri(redirect_uri))

    return render(request, 'index.html')


@login_required
def redirect_view(request):
    redirect_uri = request.build_absolute_uri(
            reverse('movesauth:redirect'))
    code = request.GET['code']
    try:
        data, expires = moves.request_token(code, redirect_uri)
    except:
        print 'Exception raised by Moves'
        return redirect(reverse('movesauth:start'))
    else:
        if hasattr(request.user, 'token'):
            print 'Deleting old token'
            request.user.token.delete()

        token = Token.objects.create(
            user=request.user,
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            moves_user_id=data.get('user_id'),
            expires=expires,
        )

        return render(request, 'movesauth/redirect.html')


class SelectWorkPlace(ListView):
    template_name = 'list.html'

    def get_queryset(self, **kwargs):
        """ Sort segments by dwell time, try to find likely workplace
        """
        res = self.request.user.token.query(
                moves.DAILY, pastDays=7)
        segment_list = MovesSegmentList(res)
        return segment_list


select_work_place = SelectWorkPlace.as_view()
