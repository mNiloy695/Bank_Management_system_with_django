from django.shortcuts import render,redirect
from django.views.generic import FormView,UpdateView
from django.urls import reverse_lazy
from .forms import UserAccountForm
from django.contrib.auth  import login
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeView
from .forms import UserAccountForm,UserUpdateForm
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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

# def Password_change(request):
#     if request.method=='POST':
#         form=PasswordChangeForm(request,instance=request.POST)
#         if form.is_valid():
#             user=form.save()
#             update_session_auth_hash(request,user)
#             messages.success(request,'your password is sucessfully updated')
#             return redirect('profile')
#         else:
#             messages.success(request,'please enter the correct information')
#     else:
#         form=PasswordChangeForm(request.user)
#     return render(request,'pass_word.html',{'form':form})
class Passs_Word_Change(LoginRequiredMixin,PasswordChangeView):
    template_name='pass_word.html'
    form_class=PasswordChangeForm
    success_url=reverse_lazy('profile')



    



