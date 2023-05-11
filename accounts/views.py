from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, DetailView, UpdateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.


class SingupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('accounts:index')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    

class LogoutView(RedirectView):
    url = reverse_lazy('accounts:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'accounts/update.html'
    success_url = reverse_lazy('accounts:profile')
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        return self.request.user
    
