from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import  get_dealers_from_cf,get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.



# Create an `about` view to render a static about page
def about(request):
    return render(request, 'static/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
   return render(request, 'static/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')
    

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == 'GET' :
        return render(request, 'static/registration.html', context)
    
    elif request.method == 'POST' :

        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False
        try:
           
            User.objects.get(username=username)
            user_exist = True
        except:
            
            logger.debug("{} is new user".format(username))
       
        if not user_exist:
           
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            
            login(request, user)
            # might have to use redirect function
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(url, id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/75bcf489-4367-4f44-bc60-f2601af99c15/dealership-package/get-reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

