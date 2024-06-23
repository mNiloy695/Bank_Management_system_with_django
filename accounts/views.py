from django.shortcuts import render,redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserAccountForm
from django.contrib.auth  import login
from django.contrib.auth.views import LogoutView,LoginView
from .forms import UserAccountForm,UserUpdateForm
from django.views import View
# Create your views here.
class UserCreationView(FormView):
    template_name='registration.html'
    form_class= UserAccountForm
    success_url=reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')  # Redirect to the home page or any other page
        return super().dispatch(self.request,*args, **kwargs)
    def form_valid(self,form):
        print(form.cleaned_data)
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
class UserLoginView(LoginView):
    template_name='user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
class UserLogOutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})

    