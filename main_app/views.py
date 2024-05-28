from django.shortcuts import render
from django.http import HttpResponse


# Add the Cat class & list and view function below the imports
class Bird:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, description, age):
    self.name = name
    self.description = description
    self.age = age

birds = [
  Bird('John', 'Kinda rude.', 3),
  Bird('Ron', 'Looks like a turtle.', 0),
  Bird('Bob', 'Happy fluff ball.', 4),
  Bird('Hector', 'Tweets loudly.', 6)
]


# Create your views here.
def home(request):
  return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')

def about(request):
  return render(request, 'about.html')

def bird_index(request):
  return render(request, 'birds/index.html', { 'birds': birds })
