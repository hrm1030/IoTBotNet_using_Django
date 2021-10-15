from django import forms  
from homeview.models import LogHistory, User
class LogHistoryForm(forms.ModelForm):  
    class Meta:  
        model = LogHistory  
        fields = "__all__"  

class UserForm(forms.ModelForm):
    """Form definition for User."""

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = ['username', 'password', 'role']