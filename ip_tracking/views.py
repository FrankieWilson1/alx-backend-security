from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from ratelimit.decorators import ratelimit

# @ratelimit(key='ip', rate='5/m', block=True)
# @ratelimit(key='user_or_ip', rate='10/m', method='POST', block=True)
def login_view(request):
    """
    A simple view to simulate a login page.
    """
    if request.method == "POST":
        # Simulate a login attempt
        return HttpResponse("Login attempt simulated.")
