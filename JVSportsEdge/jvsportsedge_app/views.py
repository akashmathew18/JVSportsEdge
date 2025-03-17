from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PlayerRegistrationForm, TeamForm, PaymentForm, FineForm, PasswordResetRequestForm
from .models import CustomUser, Player, Payment, Fine, Team
from django.http import HttpResponse

def index(request):
    return render(request, "jvsportsedge_app/index.html")

# 1️⃣ Player Registration View
def register(request):
    if request.method == "POST":
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'jvsportsedge_app/register.html', {'form': form})

# 2️⃣ Login View
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'jvsportsedge_app/login.html')

# 3️⃣ Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# 4️⃣ Dashboard View
@login_required
def dashboard(request):
    return render(request, 'jvsportsedge_app/dashboard.html')

# 5️⃣ Team Creation View (Managers Only)
@login_required
def create_team(request):
    if request.user.role != 'manager':
        return redirect('dashboard')

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_teams')
    else:
        form = TeamForm()
    return render(request, 'jvsportsedge_app/create_team.html', {'form': form})

# 6️⃣ List Teams (Managers & Players)
@login_required
def list_teams(request):
    teams = Team.objects.all()
    return render(request, 'jvsportsedge_app/list_teams.html', {'teams': teams})

# 7️⃣ Player Profile View
@login_required
def player_profile(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'jvsportsedge_app/player_profile.html', {'player': player})

# 8️⃣ Payments Page
@login_required
def payments(request):
    payments = Payment.objects.all()
    return render(request, 'jvsportsedge_app/payments.html', {'payments': payments})

# 9️⃣ Fines Page
@login_required
def fines(request):
    fines = Fine.objects.all()
    return render(request, 'jvsportsedge_app/fines.html', {'fines': fines})

# 🔟 Assign Fine (Managers Only)
@login_required
def assign_fine(request):
    if request.user.role != 'manager':
        return redirect('dashboard')

    if request.method == "POST":
        form = FineForm(request.POST)
        if form.is_valid():
            fine = form.save(commit=False)
            fine.issued_by = request.user  
            fine.save()
            return redirect('list_fines')
    else:
        form = FineForm()
    
    return render(request, 'jvsportsedge_app/assign_fine.html', {'form': form})

# 1️⃣1️⃣ List Fines (Managers & Players)
@login_required
def list_fines(request):
    if request.user.role == 'manager':
        fines = Fine.objects.all()
    else:
        fines = Fine.objects.filter(player=request.user.player)
    
    return render(request, 'jvsportsedge_app/list_fines.html', {'fines': fines})

# 1️⃣2️⃣ Password Reset Request View
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, "Password reset email has been sent.")
            return redirect('login')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'jvsportsedge_app/password_reset.html', {'form': form})
