from django.http import HttpResponse


def test_session_incr(request):
    request.session.setdefault('counter', 0)
    request.session['counter'] += 1
    # del request.session['counter']
    return HttpResponse("Hello %d" % request.session['counter'])


def test_server(request):
    raise ValueError


def get(request):
    f = open('colleges.html', 'r')
    return HttpResponse(f)
