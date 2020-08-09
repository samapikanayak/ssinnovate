from django.db import models
from django.contrib.auth.models import User
from .utils import year_of_passing_fun
import uuid
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    full_name = models.CharField(max_length = 150)
    email = models.EmailField()
    mobile = models.CharField(max_length=10,unique=True)
    batch = models.CharField("Year of Passing",max_length=15,choices=year_of_passing_fun())
    uid = models.UUIDField(editable=False,unique=True)
    picture = models.ImageField(upload_to="images/%Y/%m/%d/",blank=True)
    gender = models.CharField(max_length=10,choices=[('male',"Male"),('female',"Female"),('other',"Other"),])
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    def save(self):
        if not self.uid:
            self.uid = uuid.uuid4()
            while Profile.objects.filter(uid = self.uid).exists():
                self.uid = uuid.uuid4()
        super().save()
    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name_plural = "Alumini Members"

class Status(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length = 150)
    description = models.TextField()
    passing_year = models.CharField(max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uid = models.UUIDField(editable=False,unique=True)
    class Meta:
        verbose_name_plural = "Notes"
    def save(self):
        if not self.uid:
            self.uid = uuid.uuid4()
            while Status.objects.filter(uid = self.uid).exists():
                self.uid = uuid.uuid4()
        super().save()
