from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def bird_index(request):
  birds = Bird.objects.all()
  return render(request, 'birds/index.html', { 'birds': birds })

def bird_detail(request, bird_id):
  bird = Bird.objects.get(id=bird_id)
  feeding_form = FeedingForm()
  return render(request, 'birds/detail.html', { 'bird': bird, 'feeding_form': feeding_form })

def add_feeding(request, bird_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.bird_id = bird_id
    new_feeding.save()
  return redirect('bird-detail', bird_id=bird_id)

class BirdCreate(CreateView):
  model = Bird
  fields = ['name', 'description', 'age']

class BirdUpdate(UpdateView):
  model = Bird
  fields = ['description', 'age']

class BirdDelete(DeleteView):
  model = Bird
  success_url = '/birds/'

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'
