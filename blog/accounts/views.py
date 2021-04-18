from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index_login(request):
    return render(request, 'accounts/login.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha) #se usuario e senha estiver incorreto retorna None
    if not user:
        messages.error(request, 'Usuario ou senha invalidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request,'Logado com sucesso')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def cadastrar(request):
    if request.method != 'POST':
        return render(request, 'accounts/cadastrar.html')
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/cadastrar.html')
    try:
        validate_email(email)
    except:
        messages.error(request, 'Nenhum campo pode estar vazio')
        return render(request, 'accounts/cadastrar.html')
    if senha != senha2:
        messages.error(request, 'Senhas não conferem')
        return render(request, 'accounts/cadastrar.html')
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario já cadastrado')
        return render(request, 'accounts/cadastrar.html')
    if User.objects.filter(email=email).exists():
        messages.error(request, 'email já cadastrado')
        return render(request, 'accounts/cadastrar.html')
    messages.success(request,'Cadastrado com sucesso! Efetue o login')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')
