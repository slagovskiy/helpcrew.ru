def getUserHostAddress(request):
    ip = ''
    if request.META.get('HTTP_X_REAL_IP'):  # check ip from share internet
        ip = request.META.get('HTTP_X_REAL_IP')
    elif request.META.get('HTTP_CLIENT_IP'):    # check ip from share internet
        ip = request.META.get('HTTP_CLIENT_IP')
    elif request.META.get('HTTP_X_FORWARDED_FOR'):  # to check ip is pass from proxy
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
