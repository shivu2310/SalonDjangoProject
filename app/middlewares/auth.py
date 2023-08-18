from django.shortcuts import redirect


def auth_middleware(get_response):
    
    
    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        print(request.META['PATH_INFO'])     # in which url have visited
        if not request.session.get('customer_id'):    
            return redirect (f'/loginpage?return_url={returnUrl}')
        response = get_response(request)     # request will goto view 
        return response
    
    return middleware