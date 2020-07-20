from django.urls import path
from .views import *

urlpatterns = [
    path('contacts/', Contacts.as_view()),
    path('signup/', Signup.as_view()),
    path('login/', Login.as_view()),
    path('spam/', Spam.as_view()),
    path('searchbyname/', SearchByName.as_view()),
    path('searchbyphone/', SearchByPhone.as_view())
]