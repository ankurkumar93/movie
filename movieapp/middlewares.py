from itertools import count
from .models import RequestCount


class RequestCountMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        count = RequestCount.objects.all()
        if not count:
            RequestCount.objects.create(count=0)
        count = RequestCount.objects.values('count').first()['count']
        RequestCount.objects.values('count').update(count=count + 1)
        response = self.get_response(request)
        return response