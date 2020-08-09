from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages as msg
from .models import Profile,Status
from .utils import otp_generate
from django.db import IntegrityError
from .forms import ImageForm

# Create your views here.

@login_required(login_url="/login/")
def home_view(request):
    user = User.objects.get(username = request.user)
    profile = Profile.objects.get(user=user)
    data = Status.objects.filter(passing_year=user.profile.batch).order_by("-updated")
    mynotes = Status.objects.filter(profile=profile).order_by("-updated")
    return render(request,'userapp/home.html',{"data":data,"user":user,"mynotes":mynotes})
        
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if "@" in username:
            user = authenticate(username=username,password=password)
            if user:
                request.session['login'] = True
                login(request,user)
                msg.success(request,'Login Successfully')
                return redirect("/")
            else:
                msg.error(request,'Invalid username or password')
                return redirect("/login")
        else:
            try:
                profile = Profile.objects.get(mobile=username)
                user = authenticate(username=profile.user.username,password=password)
                if user:
                    request.session['login'] = True
                    login(request,user)
                    msg.success(request,'Login Successfully')
                    return redirect("/")
                else:
                    msg.error(request,'Invalid username or password')
                    return redirect("/login")
            except Profile.DoesNotExist:
                msg.error(request,'Invalid username or password')
                return redirect("/login")
    else:
        return render(request,'userapp/login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('email','')
        fullname = request.POST.get('fullname','')
        mobile = request.POST.get('mobile','')
        password = request.POST.get('pwd1','')
        passing = request.POST.get('passing','')
        gender = request.POST.get('gender','')
        try:
            User.objects.get(username=username)
            msg.error(request,'Email ID Already Registered')
            return redirect("/user/signup")
        except User.DoesNotExist:
            try:
                Profile.objects.get(mobile=mobile)
                msg.error(request,'Mobile Number Already Registered')
                return redirect("/signup")
            except Profile.DoesNotExist:
                request.session['username'] = username
                request.session['password'] = password
                request.session['fullname'] = fullname
                request.session['mobile'] = mobile
                request.session['passing'] = passing
                request.session['gender'] = gender
                request.session['otp'] = otp_generate()
                print(request.session['otp'])
                return redirect("/otp")
    else:
        return render(request,'userapp/signup.html')

def otp_view(request):
    if request.method == "POST":
        otp_user = request.POST.get('otp','')
        if otp_user == request.session['otp']:
            user = User.objects.create_user(username = request.session['username'],password=request.session['password'])
            Profile(user=user,full_name=request.session['fullname'],email=request.session['username'],mobile=request.session['mobile'],batch=request.session['passing'],gender=request.session['gender']).save()
            login(request,user)
            request.session['login'] = True
            msg.success(request,'Signup Completed Successfully')
            return redirect("/")
        else:
            msg.error(request,'Invalid OTP')
            return redirect('/otp')

    else:
        return render(request,'userapp/otp.html')

@login_required(login_url="/login")
def add_status(request):
    title = request.POST.get('title','')
    description = request.POST.get('description','')
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    Status(profile=profile,title=title,description=description,passing_year=user.profile.batch).save()
    msg.success(request,"Note added successfully")
    return redirect("/")
@login_required(login_url="/login")
def search(request):
    serach_result = request.GET.get('search','')
    profile_data = Profile.objects.filter(full_name__icontains=serach_result)
    notes_data = Status.objects.filter(title__icontains=serach_result) | Status.objects.filter(description__icontains=serach_result)
    return render(request,'userapp/search-result.html',{"search":serach_result,'profile_data':profile_data,'notes_data':notes_data})

def logout_view(request):
    request.session.clear()
    logout(request)
    msg.success(request,"Logout Successfully")
    return redirect("/")
@login_required(login_url="/login")
def details_profile(request,uid):
    data = Profile.objects.get(uid=uid)
    return render(request,'userapp/detail.html',{"profile":data})
@login_required(login_url="/login")
def details_status(request,uid):
    data = Status.objects.get(uid=uid)
    return render(request,'userapp/detail.html',{"status":data})



@login_required(login_url='/login/')
def profile_update(request):
    form = ImageForm()
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        profile.full_name = request.POST.get('fullname','')
        profile.email = request.POST.get('email','')
        user.username = request.POST.get('email','')
        user.save()
        profile.save()
        msg.success(request,"Profile Updated successfully")
        return redirect("/")
    else:
        return render(request,'userapp/profile-update.html',{"data":profile,"form":form})

@login_required(login_url='/login/')
def change_password(request):
    if request.method == "POST":
        user = authenticate(username=request.user,password=request.POST['password'])
        if user:
            user1 = User.objects.get(username=request.user)
            user1.set_password(request.POST['newpassword'])
            user1.save()
            msg.success(request,"Password Changed Successfully")
            return redirect("/")
        else:
            msg.error(request,"Incorrect Old Password")
            return redirect("/profile-update")
@login_required(login_url='/login/')
def delete(request,uid):
    status = Status.objects.get(uid=uid)
    status.delete()
    msg.success(request,"One Note Deleted")
    return redirect("/")
@login_required(login_url='/login/')
def update(request,uid):
    data = Status.objects.get(uid=uid)
    if request.method =="POST":
        data.title = request.POST.get("title","")
        data.description = request.POST.get("description","")
        data.save()
        msg.success(request,"Notes Updated Successfully")
        return redirect("/")
    else:
        return render(request,'userapp/note-update.html',{"data":data})
@login_required(login_url="/login/")
def change_profile_picture(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    form = ImageForm(request.POST,request.FILES,instance=profile)
    form.save()
    return redirect("/")

@login_required(login_url="/login/")
def delete_profile_picture(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=user)
    profile.picture = ""
    profile.save()
    return redirect("/")
