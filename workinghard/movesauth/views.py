from os import environ

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy

from .movesclient import Moves
from .models import Token

MOVES_CLIENT_ID = environ.get('MOVES_CLIENT_ID')
MOVES_CLIENT_SECRET = environ.get('MOVES_CLIENT_SECRET')

moves = Moves(MOVES_CLIENT_ID, MOVES_CLIENT_SECRET)


def start(request):
    redirect_uri = request.build_absolute_uri(
            reverse('movesauth:redirect'))

    c = {
        'authorise_uri': moves.get_auth_uri(redirect_uri),
    }

    return render(request, 'movesauth/start.html', c)


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
        token = Token.objects.create(
            user=request.user,
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            moves_user_id=data.get('user_id'),
            expires=expires,
        )

        return render(request, 'movesauth/redirect.html')
