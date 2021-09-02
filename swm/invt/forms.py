from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TUser,Waste,TransportVehicle,ProcesssingPlant,Landfill

class UserRegisterForm(UserCreationForm):
    class Meta:
        fields = ["username", "email", "password1", "password2",'area','landmark','city','state','zipcode']
        model = TUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Full name"
        self.fields["email"].label = "Email address"

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = TUser
        fields = ['username', 'email','area','landmark','city','state','zipcode']

class WasteGenerationForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = ['type_waste', 'created_date','quantity','tv']
        
    def __init__(self,*args, **kwargs):
        super(WasteGenerationForm,self).__init__(*args, **kwargs) 
        self.fields["type_waste"].label = "Type of Waste"
        self.fields["created_date"].label = "Date of Collection"
        self.fields["quantity"].label = "Quantity(in kgs)"
        self.fields["tv"].label = "Transport Vehicle"
class TvGenerationForm(forms.ModelForm):
    class Meta:
        model = TransportVehicle
        fields = ['plate_number', 'capacity','permit','pp','pincode']
        
    def __init__(self,*args, **kwargs):
        super(TvGenerationForm,self).__init__(*args, **kwargs) 
        self.fields["plate_number"].label = "Plate Number/Vehile Number"
        self.fields["capacity"].label = "Total Capacity"
        self.fields["permit"].label = "Permit"
        self.fields["pp"].label = "Processing Plant"
        self.fields["pincode"].label = "Pincode"
class PpGenerationForm(forms.ModelForm):
    class Meta:
        model = ProcesssingPlant
        fields = ['ppname', 'total_waste','landfill_waste','area','landmark','city','state','zipcode']
        
    def __init__(self,*args, **kwargs):
        super(PpGenerationForm,self).__init__(*args, **kwargs) 
        self.fields["ppname"].label = "Processing Plant Name"
        self.fields["total_waste"].label = "Total Waste till date"
        self.fields["landfill_waste"].label = "Landfill waste till date"
        self.fields["area"].label = "Area"
        self.fields["landmark"].label = "Landmark"
        self.fields["city"].label = "City"
        self.fields["state"].label = "State"
        self.fields["zipcode"].label = "Pincode"
        

class LfGenerationForm(forms.ModelForm):
    class Meta:
        model = Landfill
        fields = ['lfname', 'maximum_capacity','capacity_filled','pp','area','landmark','city','state','zipcode']
        
    def __init__(self,*args, **kwargs):
        super(LfGenerationForm,self).__init__(*args, **kwargs) 
        self.fields["lfname"].label = "Landfill Name"
        self.fields["maximum_capacity"].label = "Maximum Capacity Of Landfill"
        self.fields["capacity_filled"].label = "Capacity Filled"
        self.fields["pp"].label = "Processing Plant"
        self.fields["area"].label = "Area"
        self.fields["landmark"].label = "Landmark"
        self.fields["city"].label = "City"
        self.fields["state"].label = "State"
        self.fields["zipcode"].label = "Pincode"

class TvUpdateForm(forms.ModelForm):
    class Meta:
        model = TransportVehicle
        fields = ['plate_number', 'capacity','permit','pp','pincode']
class PpUpdateForm(forms.ModelForm):
    class Meta:
        model = ProcesssingPlant
        fields = ['ppname', 'total_waste','landfill_waste','area','landmark','city','state','zipcode']
class LfUpdateForm(forms.ModelForm):
    class Meta:
        model = Landfill
        fields = ['lfname', 'maximum_capacity','capacity_filled','pp','area','landmark','city','state','zipcode']