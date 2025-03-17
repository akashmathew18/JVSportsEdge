from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('player', 'Player'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='player')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    dob = models.DateField(default="2000-01-01")
    sport = models.CharField(max_length=10, choices=[('cricket', 'Cricket'), ('football', 'Football')])

class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    sport = models.CharField(max_length=10, choices=[('cricket', 'Cricket'), ('football', 'Football')])

    # Cricket-Specific Fields
    batting_style = models.CharField(max_length=50, blank=True, null=True)
    bowling_style = models.CharField(max_length=50, blank=True, null=True)
    cricket_role = models.CharField(max_length=50, blank=True, null=True)

    # Football-Specific Fields
    playing_position = models.CharField(max_length=50, blank=True, null=True)
    preferred_foot = models.CharField(max_length=10, blank=True, null=True)
    playing_style = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.sport}"

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    manager = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'manager'})

    def __str__(self):
        return self.name

# Payment Model (For Registration Fees)
class Payment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=50, default="Registration Fee")

    def __str__(self):
        return f"{self.player.user.username} - {self.amount}"

# Fine Model (For Players)
class Fine(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fine for {self.player.user.username} - {self.amount}"
