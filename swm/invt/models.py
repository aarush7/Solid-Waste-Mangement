from django.db import models
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib import auth

class TUser(auth.models.User, auth.models.PermissionsMixin):
    area=models.CharField(max_length=150,blank=False)
    landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)
    
    def __str__(self):
        return "@{}".format(self.username)

class OrganisationAddress(models.Model):
    area=models.CharField(max_length=150,blank=False)
    landmark=models.CharField(max_length=150,blank=True)
    city=models.CharField(max_length=50,blank=False)
    state=models.CharField(max_length=30,blank=False)
    zipcode=models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)

class ProcesssingPlant(OrganisationAddress):
    pp_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ppname=models.CharField(blank=False,max_length=100)
    total_waste=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    landfill_waste=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    def get_rw(self):
        return self.total_waste-self.landfill_waste
    recycled_Waste=property(get_rw)

    def __str__(self):
        return self.ppname

class TransportVehicle(models.Model):
    tv_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_Of_collection = models.DateField(default=timezone.now)
    plate_number=models.CharField(blank=False,null=False,max_length=20)
    capacity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    choices_permit=(
        ('ALL INDIA PERMIT','ALL INDIA PERMIT'),
        ('STATE PERMIT','STATE PERMIT'),
        ('CITY','CITY')
    )
    permit=models.CharField(max_length=20,choices=choices_permit,blank=False)
    pp=models.ForeignKey(ProcesssingPlant,on_delete=models.CASCADE)
    pincode = models.IntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)],blank=False)

    def __str__(self):
        return str(self.pincode) +" ( "+ self.plate_number+" ) "

class Landfill(OrganisationAddress):
    lf_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lfname=models.CharField(blank=False,max_length=100)
    maximum_capacity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    capacity_filled=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    pp=models.ForeignKey(ProcesssingPlant,on_delete=models.CASCADE)

    def __str__(self):
        return self.lfname

class Waste(models.Model):
    waste_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tpuser= models.ForeignKey('auth.User',null=True,on_delete=models.SET_NULL)
    choices_type=(
        ('Recyable','Recyable'),
        ('Non-Recyable','Non-Recyable')
    )
    type_waste=models.CharField(max_length=20,choices=choices_type,blank=False)
    created_date = models.DateField(default=timezone.now)
    quantity=models.IntegerField(blank=False,null=False,validators=[MaxValueValidator(99999),MinValueValidator(0)])
    tv = models.ForeignKey(TransportVehicle,blank=True,null=True,on_delete=models.SET_NULL)


class WasteML(models.Model):
    ppname = models.ForeignKey(ProcesssingPlant,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    waste_qty = models.IntegerField(blank=False,null=False)

    









    