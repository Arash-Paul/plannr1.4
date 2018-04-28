from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
# from rest_framework import status
from django.shortcuts import render, redirect, render_to_response
# from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import SignUpForm, UserForm, EventForm
from .models import User, CreatedEvent
from .serializers import UserSerializer, UserMinFoSerializer, CreatedEventSerializer
from django.contrib.auth.views import logout
# from django.urls import reverse_lazy
# from django.views import generic
# from django.contrib.auth.mixins import LoginRequiredMixin


class Register(View):
    form_class = SignUpForm  # UserForm
    template_signup = 'register.html'

    @csrf_exempt
    def get(self, request):
        form = self.form_class(None)
        pass

    @csrf_exempt
    def post(self, request):
        # Data is here
        form = self.form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = authenticate(email=email)
            if user is None:
                form.save()
                msg = 'Saved successfully'
                return HttpResponse(msg)
            else:
                msg = 'User exists'
                return HttpResponse(msg)
        else:
            msg = 'Invalid data'
            return HttpResponse(msg)


class UserFormLogin(View):
    form_class = UserForm

    def get(self, request):
        pass

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                # can request user info here
                login(request, user)
                msg = 'Logged in'
                return HttpResponse(msg)
            else:
                if user is None:
                    msg = 'None username'
                    return HttpResponse(msg)
                else:
                    msg = 'Inactive'
                    return HttpResponse(msg)

        else:
            msg = 'Invalid data'
            return HttpResponse(msg)


# returns user data of all users
class UserList(APIView):
    # retrieve details of Users
    # URL ~/users/
    @staticmethod
    def get(request):
        # change per data requirement /query
        users = User.objects.all()
        serializer = UserMinFoSerializer(users, many=True)
        return Response(serializer.data)

    def post(self):
        pass


# Event creation url handler
class EventCreationForm(View):
    template_eventcreationform = 'eventcreationform.html'
    form_class = EventForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_eventcreationform, {'form': form})

    def post(self, request):
        # data is here
        form = self.form_class(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            user = request.user
            inst = CreatedEvent()
            inst.user = user
            inst.event_name = form.cleaned_data.get('event_name')
            inst.event_date_time = form.cleaned_data.get('event_date_time')
            inst.address = form.cleaned_data.get('address')
            inst.save()
            message = 'Event added'
            return redirect('api:home')
            # return render(request, 'base.html', {'message': message})
        else:
            message = 'Invalid form data, try again'
            form = self.form_class(None)
            return render(request, self.template_eventcreationform, {'message': message, 'form': form})


class CreatedEventList(APIView):
    @staticmethod
    def get(request):
        # change per data requirement /query
        events = CreatedEvent.objects.filter(user_id=request.user)
        serializer = CreatedEventSerializer(events, many=True)
        return HttpResponse(serializer.data)

    def post(self):
        pass


def userlogout(request):
    logout(request)
    msg = 'Logged out'
    return HttpResponse(msg)
