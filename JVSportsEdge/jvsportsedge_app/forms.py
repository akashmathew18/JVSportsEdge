from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser, Team, Payment, Player, Fine

class PlayerRegistrationForm(UserCreationForm):
    # Basic Information
    full_name = forms.CharField(max_length=100, required=True, label="Full Name")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    dob = forms.DateField(required=True, label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    sport = forms.ChoiceField(choices=[('cricket', 'Cricket'), ('football', 'Football')], required=True, label="Select Sport")

    # Cricket-Specific Fields
    batting_style_choices = [('Right-Hand Bat', 'Right-Hand Bat'), ('Left-Hand Bat', 'Left-Hand Bat')]
    batting_style = forms.ChoiceField(choices=batting_style_choices, required=False, label="Batting Style")

    bowling_style_choices = [
        ('Right-Arm Fast', 'Right-Arm Fast'), ('Right-Arm Medium', 'Right-Arm Medium'),
        ('Right-Arm Off Spin', 'Right-Arm Off Spin'), ('Left-Arm Fast', 'Left-Arm Fast'),
        ('Left-Arm Medium', 'Left-Arm Medium'), ('Left-Arm Orthodox', 'Left-Arm Orthodox')
    ]
    bowling_style = forms.ChoiceField(choices=bowling_style_choices, required=False, label="Bowling Style")

    cricket_role_choices = [('Batsman', 'Batsman'), ('Bowler', 'Bowler'), ('All-Rounder', 'All-Rounder'), ('Wicket-Keeper', 'Wicket-Keeper')]
    cricket_role = forms.ChoiceField(choices=cricket_role_choices, required=False, label="Cricket Role")

    # Football-Specific Fields
    playing_position_choices = [
        ('Goalkeeper', 'Goalkeeper'), ('Defender', 'Defender'), ('Midfielder', 'Midfielder'), ('Forward', 'Forward')
    ]
    playing_position = forms.ChoiceField(choices=playing_position_choices, required=False, label="Playing Position")

    preferred_foot_choices = [('Right', 'Right'), ('Left', 'Left'), ('Both', 'Both')]
    preferred_foot = forms.ChoiceField(choices=preferred_foot_choices, required=False, label="Preferred Foot")

    playing_style_choices = [
        ('Playmaker', 'Playmaker'), ('Dribbler', 'Dribbler'), ('Poacher', 'Poacher'), ('Sweeper', 'Sweeper')
    ]
    playing_style = forms.ChoiceField(choices=playing_style_choices, required=False, label="Playing Style")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'phone', 'dob', 'sport']

    def clean(self):
        cleaned_data = super().clean()
        sport = cleaned_data.get("sport")

        # Validate Cricket Fields
        if sport == "cricket":
            if not cleaned_data.get("batting_style") or not cleaned_data.get("cricket_role"):
                raise forms.ValidationError("Please fill all Cricket-related fields.")
        
        # Validate Football Fields
        elif sport == "football":
            if not cleaned_data.get("playing_position") or not cleaned_data.get("preferred_foot"):
                raise forms.ValidationError("Please fill all Football-related fields.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'player'
        user.full_name = self.cleaned_data['full_name']
        user.phone = self.cleaned_data['phone']
        user.dob = self.cleaned_data['dob']
        user.sport = self.cleaned_data['sport']

        if commit:
            user.save()
            Player.objects.create(
                user=user,
                sport=user.sport,
                batting_style=self.cleaned_data.get('batting_style', ''),
                bowling_style=self.cleaned_data.get('bowling_style', ''),
                cricket_role=self.cleaned_data.get('cricket_role', ''),
                playing_position=self.cleaned_data.get('playing_position', ''),
                preferred_foot=self.cleaned_data.get('preferred_foot', ''),
                playing_style=self.cleaned_data.get('playing_style', '')
            )

        return user

# Manager Creation Form (Only Admin Can Create Managers)
class ManagerCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'manager'  # Assigning Manager role
        if commit:
            user.set_password(self.cleaned_data['password'])  # Hash the password
            user.save()
        return user

# Team Creation Form
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'manager']

# Payment Form (For Registration Fees)
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['player', 'amount']

# Fine Management Form (For Managers)
class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['player', 'amount', 'reason']

# Password Reset Request Form
class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(label="Enter your email", max_length=254)