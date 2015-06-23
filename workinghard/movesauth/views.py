from os import environ
from datetime import datetime

from django.shortcuts import render, redirect, render_to_response
from django.views.generic import FormView, ListView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .movesclient import Moves, InvalidGrant, MovesSegmentList
from .models import Token
from .forms import WorkplaceForm


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


def select_work_place(request):
    if 'place_list' in request.session:
        place_list = request.session['place_list']
        print 'Placelist from session'
    else:
        res = request.user.token.query(moves.DAILY, pastDays=7)
        places = MovesSegmentList(res)
        place_list = [(place['place_id'], place['name'])\
                      for place in places]

        print 'setting placelist to session'

        request.session['place_list'] = place_list

    if 'POST' == request.method:
        form = WorkplaceForm(request.POST, places=place_list)

        if form.is_valid():
            print form.cleaned_data

    else:
        form = WorkplaceForm(places=place_list)

    return render_to_response('form_select_workplace.html', {
        'form': form
    })
