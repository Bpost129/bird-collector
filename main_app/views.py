from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bird, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def bird_index(request):
  birds = Bird.objects.filter(user=request.user)
  return render(request, 'birds/index.html', { 'birds': birds })

@login_required
def bird_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  toys_bird_doesnt_have = Toy.objects.exclude(id__in = bird.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', { 'bird': bird, 'feeding_form': feeding_form, 'toys': toys_bird_doesnt_have })

@login_required
def add_feeding(request, bird_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('bird-detail', bird_id=bird_id)

class BirdCreate(LoginRequiredMixin, CreateView):
  model = Bird
  fields = ['name', 'description', 'age']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class BirdUpdate(LoginRequiredMixin, UpdateView):
  model = Bird
  fields = ['description', 'age']

class BirdDelete(LoginRequiredMixin, DeleteView):
  model = Bird
  success_url = '/birds/'

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

@login_required
def assoc_toy(request, bird_id, toy_id):
  Bird.objects.get(id=bird_id).toys.add(toy_id)
  return redirect('bird-detail', bird_id=bird_id)

class Home(LoginView):
  template_name = 'home.html'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('bird-index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)