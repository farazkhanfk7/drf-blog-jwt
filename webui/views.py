from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import View, ListView,DetailView,CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Blog
from django.core.exceptions import PermissionDenied
from .forms import UserRegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib import auth


# Create your views here.
class BlogView(ListView):
    model = Blog
    template_name = "home.html"
    ordering = ['-created_on']

class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog_detail.html"

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title','content']
    template_name = "blog_create.html"

    # to change author to request.user
    # just like i did in api
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title','content']
    template_name = "blog_create.html"

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url ='/'
    template_name = "item_confirm_delete.html"

    # did this bcoz I want only author to delete his blog
    def user_passes_test(self, request):
        if request.user.is_authenticated:
            self.object = self.get_object()
            return self.object.author == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            raise PermissionDenied
        return super(BlogDeleteView, self).dispatch(request, *args, **kwargs)
    

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'auth/register.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your account has been created! Your are now able to login.")
                return redirect('/')
            else:
                messages.warning(request, "Error while registering. Please signup again.")
                return redirect('register/')

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username_ = form.cleaned_data.get('username')
                password_ = form.cleaned_data.get('password')
                user = authenticate(username=username_,password=password_)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, "Your have been logged in !")
                    return redirect('/')
                else:
                    messages.warning(request, "Oops! Invalid credentials.")
                    return redirect('login')
            else:
                messages.warning(request, "Oops! Invalid Input.")
                return redirect('/')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out.")
            return redirect('/')
        return redirect('login/')
            
