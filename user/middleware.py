import datetime

from django.http import HttpResponseForbidden
from datetime import datetime, time


class LogIPMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response



    def __call__(self, request):

        ip = request.META.get('REMOTE_ADDR', 'Noma’lum IP')

        now = datetime.datetime.now()

        print(f"[{now}] So‘rov IP: {ip}")
        print(request.META)


        response = self.get_response(request)

        return response



class LogUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        print(user_agent,"------------------usr")
        response = self.get_response(request)
        return response




class TimeRestrictedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = time(8, 0, 0)
        end_time = time(16, 0, 0)

        if not (start_time <= now <= end_time):
            return HttpResponseForbidden("Saytga faqat 08:00 dan 18:00 gacha kirishingiz mumkin.")

        response = self.get_response(request)
        return response


import time
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        now = time.time()

        if ip not in self.requests:
            self.requests[ip] = []

        # Faqat 10 soniyadan yangi so‘rovlarni saqlaymiz
        self.requests[ip] = [timestamp for timestamp in self.requests[ip] if now - timestamp < 10]

        if len(self.requests[ip]) >= 5:
            return HttpResponseForbidden("Siz juda ko'p so'rov yubordingiz. Iltimos, biroz kuting.")

        self.requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
