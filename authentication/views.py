from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from django.template.loader import render_to_string

class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
    
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username exists'}, status=409)
        
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        
        # messages.success(request, "Success Whatsup")
        # messages.warning(request, "Success warning")
        # messages.info(request, "Success info")
        # messages.error(request, "Success success")
        
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        context={
            'fieldValues': request.POST
        }
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                if len(password) < 8:
                    messages.error(request, "Password too short")
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Account Successfully Created")
                # return render(request, 'authentication/register.html')
                return redirect('login')            
                
                    
        # return render(request, 'authentication/register.html')
    
class emailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
    
        if not validate_email(email):
            return JsonResponse({'email_error':'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email is in use'}, status=409)
        
        return JsonResponse({'email_valid': True})

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, "Welcome, " + user.username + ", You are now logged in")
                    
                    return redirect('expenses')
                    
                messages.error(request, 'Account Is Not Active, Contact Your Administrator')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid Credentials, Try Again')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please, Fill All Fields')
        return render(request, 'authentication/login.html')
    
    
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')