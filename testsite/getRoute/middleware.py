'''
Python Middleware to return all the nearest bus routes to your coordinates
'''


class GetRouteMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before view

        response = self.get_response(request)
        response['coords'] = 120
        print(response)
        # After View

        return response

    def getNearest(self, request):
        pass