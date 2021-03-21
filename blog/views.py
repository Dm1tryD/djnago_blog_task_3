from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, FormView, DetailView, View, DeleteView, UpdateView
from django.forms import BaseFormSet
from django.views.generic.edit import FormMixin

from .forms import UserRegisterForm, PostForm, CommentForm
from .models import Post


class HomePage(ListView):

    model = Post
    paginate_by = 2
    context_object_name = 'posts'
    template_name = 'blog/home_blog.html'


class SignUp(CreateView):

    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'blog/signup.html'


class UserSignUpView(FormView):

    template_name = 'blog/signup.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=raw_password, email=email)
        login(self.request, user)
        return redirect('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(UserSignUpView, self).get(request, *args, **kwargs)


class UserLoginView(LoginView):

    template_name = 'blog/login.html'
    redirect_authenticated_user = True


class PostDetailView(FormMixin, DetailView):

    form_class = CommentForm
    model = Post
    template = 'blog/post_detail.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', args={self.get_object().slug})

    def get(self, request, slug):
        form = self.form_class
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj,'form':form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostCreate(LoginRequiredMixin, View):

    form_class = PostForm
    template_name = 'blog/post_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.author = self.request.user
            new_obj = form.save()
            return redirect(new_obj)
        return render(request, self.template_name, context={'form': form})


class PostDeleteView(LoginRequiredMixin, DeleteView):

    model = Post
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == self.request.user or self.request.user.is_superuser:
            return super(PostDeleteView, self).dispatch(request, *args, **kwargs)
        raise Http404("You are not allowed to edit this Post")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PostEditView(LoginRequiredMixin, UpdateView):

    model = Post
    template_name = 'blog/post_update.html'
    fields = ['title', 'body', 'image']
