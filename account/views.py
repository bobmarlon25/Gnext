from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


from .forms import LoginForm
# from .forms import LoginForm, UserRegistrationForm

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username = cd['username'],
                                password = cd['password']) # None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('El usuario no esta activo')
            else:
                return HttpResponse('La información no es correcta')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


def inicio(request):
    return redirect(reverse('inicio'))

    
@login_required
def dashboard(request):
    # return render(request, 
    # 'account/dashboard.html')
    return redirect(reverse('registrar'))


