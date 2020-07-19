from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.generic import ListView, CreateView, FormView
from .decorators import unauthenticated_user, authenticated_user
from .models import Cat, Ad, Sub, Pic, TagLink, Tag
from .forms import AdForm, CreateUserForm, FileFieldForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files import File


class Upload(FormView):
    form_class = AdForm, Pic
    template_name = 'upload.html'  # Replace with your template.
    success_url = '/user/'  # Replace with your URL or reverse().

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            usr = "Бүртгэлгүй"
        else:
            usr = request.user
        cts = Cat.objects.all()
        sbs = Sub.objects.all()
        form = AdForm()
        context = {'form': form, 'cts': cts, 'sbs': sbs, 'usr': usr}
        return render(request, 'upload.html', context)

    def post(self, request, *args, **kwargs):
        form = AdForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('url')
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user.id
            post.saved()
            for f in files:
                file = Pic.objects.create(url=f, ad=post)
                file.saved()
        return render(request, 'index.html')


def index(request):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    cts = Cat.objects.all()
    uds = Ad.objects.all().order_by('-date')
    sbs = Sub.objects.all()
    upp = Pic.objects.all()
    paginator = Paginator(uds, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'usr': usr, 'cts': cts, 'uds': uds, 'sbs': sbs, 'upp': upp, 'page_obj': page_obj}
    return render(request, 'index.html', context)


@authenticated_user
def login_page(request):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username Password incorrect')
            return render(request, 'login.html')

    return render(request, 'login.html', {
        'usr': usr})


def logout_page(request):
    logout(request)
    return redirect('login')


@authenticated_user
def register_page(request):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for' + user)
            return redirect('login')
    context = {'form': form, 'usr': usr}
    return render(request, 'register.html', context)


def details(request, pk):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    cts = Cat.objects.all()
    sbs = Sub.objects.all()
    ups = Pic.objects.filter(ad=pk)
    uds = Ad.objects.get(pk=pk)
    if request.method == 'GET':
        uds.count += 1
        uds.save()
        return render(request, 'details.html', {'ups': ups, 'uds': uds, 'cts': cts, 'sbs': sbs, 'usr': usr})


@unauthenticated_user
def user_page(request):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    uid = request.user.id
    cts = Cat.objects.all()
    sbs = Sub.objects.all()
    uds = Ad.objects.filter(user_id=uid)
    paginator = Paginator(uds, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user.html', {'usr': usr, 'uds': uds, 'cts': cts, 'sbs': sbs, 'page_obj': page_obj})


def search(request, ctl_id="", sbl_id=""):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    if sbl_id == "":
        cts = Cat.objects.all()
        uds = Ad.objects.filter(pk=ctl_id)
        sbs = Sub.objects.filter(cat_id=ctl_id)
        obj = Cat.objects.get(pk=ctl_id)
        tag = obj.tag.all()
        paginator = Paginator(uds, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'tag': tag, 'usr': usr, 'cts': cts, 'uds': uds, 'sbs': sbs, 'page_obj': page_obj})
    else:
        cts = Cat.objects.all()
        uds = Ad.objects.filter(pk=sbl_id)
        sbs = Sub.objects.all()
        obj = Sub.objects.get(pk=sbl_id)
        tag = obj.tag.all()
        paginator = Paginator(uds, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'tag': tag, 'usr': usr, 'cts': cts, 'uds': uds, 'sbs': sbs, 'page_obj': page_obj})


def contact_page(request):
    if not request.user.is_authenticated:
        usr = "Бүртгэлгүй"
    else:
        usr = request.user
    return render(request, 'contact.html', {'usr': usr})
