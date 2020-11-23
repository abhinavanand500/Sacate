from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here.


def home(request):
    return render(request, 'mysite/home.html')


def contact(request):
    if(request.method == 'POST'):
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if(len(name) < 2 or len(email) < 2 or len(phone) < 10 or len(content) < 2):
            messages.error(request, "Please fill this form Correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your response has been Submitted Successfully. Thank You!")
    return render(request, 'mysite/contact.html')


def about(request):
    return render(request, 'mysite/about.html')


def search(request):
    query = request.GET['query']
    if(len(query) > 50):
        allpost = Post.objects.none()
    else:
        allpostTitle = Post.objects.filter(title__icontains=query)
        allpostContent = Post.objects.filter(content__icontains=query)
        allpost = allpostTitle.union(allpostContent)
    if(allpost.count() == 0):
        messages.warning(
            request, "Your searched item is not present in this blog.")
    else:
        messages.success(request, "We have something for you.")
    params = {'allpost': allpost, 'query': query}
    return render(request, 'mysite/search.html', params)

# API's


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['phone']
        zip1 = request.POST['zip']
        user1 = Userinfo.objects.filter(username=username)
        if(user1):
            messages.error(
                request, "This username is not valid. Please try with other username.")
            return redirect('home')

        if(len(username) > 10):
            messages.error(
                request, "Username length must be less than 10 character.")
            return redirect('home')

        if not username.isalnum():
            messages.error(
                request, "Username should only contain character or numberå.")
            return redirect('home')

        if(pass1 != pass2):
            messages.error(request, "Password not matched. Please try again")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        userinformation = Userinfo(username=username, firstname=fname,
                                   lastname=lname, email=email, password=pass1, phone=phone, pin=zip1)
        userinformation.save()
        messages.success(
            request, "You have successfully registered in this Blog. Welcome!")
        return redirect('home')
    else:
        return HttpResponse("404 not Found")


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In. Welcome!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials. Please try again")
            return redirect('home')
    messages.error(request, "You need to Login to access this page")
    return redirect('home')


@login_required(login_url='handleLogin')
def profile(request):
    if request.method == "POST":
        data = Userinfo.objects.filter(username=request.user)
        data1 = User.objects.filter(username=request.user)
        fname1 = request.POST['fnamea']
        lname1 = request.POST['lnamea']
        phone = request.POST['phone']
        address = request.POST['address']
        pin = request.POST['pin']
        data.update(firstname=fname1, lastname=lname1,
                    phone=phone, address=address, pin=pin)
        data1.update(first_name=fname1, last_name=lname1)
        messages.success(request, "Successfully Profile Updated")
    data = Userinfo.objects.filter(username=request.user)
    params = {'data': data}
    return render(request, 'mysite/profile.html', params)


@login_required(login_url='handleLogin')
def deleteacc(request):
    if request.method == "POST":
        try:
            u = User.objects.get(username=request.user)
            p = Userinfo.objects.get(username=request.user)
            logout(request)
            u.delete()
            p.delete()
            messages.success(request, "The user is deleted")

        except:
            data = Userinfo.objects.filter(username=request.user)
            params = {'data': data}
            return render(request, 'mysite/profile.html', params)

    return redirect('home')


@login_required(login_url='handleLogin')
def changepassword(request):
    if(request.method == 'POST'):
        old = request.POST['old']
        new = request.POST['new']
        new1 = request.POST['new1']
        data = Userinfo.objects.filter(username=request.user)
        password = data[0].password
        if(password != old):
            messages.error(request, "Your Password is not Matching")
            d = Userinfo.objects.filter(username=request.user)
            params = {'data': d}
            return render(request, 'mysite/profile.html', params)
        elif(new != new1):
            messages.error(request, "Your new Password is not Matching")
            d = Userinfo.objects.filter(username=request.user)
            params = {'data': d}
            return render(request, 'mysite/profile.html', params)
        data = Userinfo.objects.filter(username=request.user)
        data1 = User.objects.filter(username=request.user)
        data.update(password=new)
        data1.set_password(new)
        messages.success(request, "Password Changed Successfully")
        params = {'data': data}
        return render(request, 'mysite/profile.html', params)


@login_required(login_url='handleLogin')
def viewprofile(request, slug):
    user1 = Userinfo.objects.filter(username=slug)
    params = {'users': user1}
    return render(request, 'mysite/viewProfile.html', params)


@login_required(login_url='handleLogin')
def donateFood(request):
    if(request.method == 'POST'):
        foodStatus = request.POST['foodStatus']
        exampleFoodDescription = request.POST['exampleFoodDescription']
        try:
            user = request.user
            user1 = Userinfo.objects.filter(username=user)
            pin1 = user1[0].pin
            address = user1[0].address
            phone = user1[0].phone
            donate = DonatedFood(foodStatus=foodStatus, foodDescription=exampleFoodDescription,
                                 user=user, pin=pin1, phone=phone, address=address)
            donate.save()
            messages.success(
                request, "Your response has been Submitted Successfully. Thank You!")
            return redirect('home')
        except:
            messages.error(
                request, "You are not logged in. Or you are not a member. Please Login for Donate")

    return render(request, 'mysite/donateFood.html')


@login_required(login_url='handleLogin')
def donateCloth(request):
    if(request.method == 'POST'):
        clothType = request.POST['clothType']
        exampleClothDescription = request.POST['exampleClothDescription']
        try:
            user = request.user
            user1 = Userinfo.objects.filter(username=user)
            pin1 = user1[0].pin
            address = user1[0].address
            phone = user1[0].phone
            donate = DonatedCloth(clothType=clothType, clothDescription=exampleClothDescription,
                                  user=user, pin=pin1, phone=phone, address=address)
            donate.save()
            messages.success(
                request, "Your response has been Submitted Successfully. Thank You!")
            return redirect('home')
        except:
            messages.error(
                request, "You are not logged in. Or you are not a member. Please Login for Donate")
    return render(request, 'mysite/donateCloth.html')


@login_required(login_url='handleLogin')
def createtweet(request):
    if(request.method == "POST"):
        uname = request.POST['uname']
        feed = request.POST['feed']
        data1 = User.objects.filter(username=uname)
        try:
            if(uname == data1[0].username):
                feed1 = NewsFeed(user1=uname, feed=feed)
                feed1.save()
                messages.success(
                    request, "Your response has been Submitted Successfully. Thank You!")
        except:
            messages.error(
                request, "Sorry This username is Invalid. Try Again")
    return redirect('home')


@login_required(login_url='handleLogin')
def tweet(request):
    feeds = NewsFeed.objects.all().order_by('-id')
    params = {'feeds': feeds}
    return render(request, 'mysite/newsFeed.html', params)


def handleLogout(request):
    logout(request)
    messages.success(
        request, "Successfully Logged Out. Visit after website again!. If you have any issue then post it on contact tab. Thankyou!")
    return redirect('home')


@login_required(login_url='handleLogin')
def dashboard(request):
    user = request.user
    if(user.is_superuser):
        user1 = Userinfo.objects.filter(username=user)
        pin1 = user1[0].pin
        others = DonatedOther.objects.filter(pin=pin1).order_by('-no')
        clothes = DonatedCloth.objects.filter(pin=pin1).order_by('-no')
        foods = DonatedFood.objects.filter(pin=pin1).order_by('-no')
        params = {'clothes': clothes, 'foods': foods, 'others': others}
        return render(request, 'mysite/dashboard.html', params)
    else:
        messages.error(request, "You are not authorised to visit this page")
        return redirect('home')


@login_required(login_url='handleLogin')
def acceptFood(request, slug):
    user = request.user
    if(user.is_superuser):
        user1 = Userinfo.objects.filter(username=user)
        pin1 = user1[0].pin
        others = DonatedOther.objects.filter(pin=pin1).order_by('-no')
        clothes = DonatedCloth.objects.filter(pin=pin1).order_by('-no')
        foods = DonatedFood.objects.filter(pin=pin1).order_by('-no')
        foods1 = DonatedFood.objects.filter(no=slug)
        enduser1 = foods[0].user
        phone1 = user1[0].phone
        address = user1[0].address
        desc = foods1[0].foodDescription
        type1 = 'Food'
        aa = Userinfo.objects.filter(username=enduser1)
        phone2 = aa[0].phone
        address2 = aa[0].address
        superuser1 = Finaluser(superuser=user, enduser=enduser1, phone=phone2,
                               address=address2, type1=type1, description=desc, done=0)
        superuser1.save()
        notify = Notification(superuser=user, enduser=enduser1, phone=phone1,
                              address=address, type1=type1, description=desc, done=0)
        notify.save()
        foods1.delete()
        params = {'clothes': clothes, 'foods': foods, 'others': others}
        messages.success(request, "You Confirmed Food Order")
        return render(request, 'mysite/dashboard.html', params)
    else:
        messages.error(request, "You are not authorised to call this API")
        return redirect('home')


@login_required(login_url='handleLogin')
def acceptCloth(request, slug):
    user = request.user
    if(user.is_superuser):
        user1 = Userinfo.objects.filter(username=user)
        pin1 = user1[0].pin
        others = DonatedOther.objects.filter(pin=pin1).order_by('-no')
        clothes = DonatedCloth.objects.filter(pin=pin1).order_by('-no')
        foods = DonatedFood.objects.filter(pin=pin1).order_by('-no')
        clothes1 = DonatedCloth.objects.filter(no=slug)
        enduser1 = clothes[0].user
        phone1 = user1[0].phone
        address = user1[0].address
        desc = clothes1[0].clothDescription
        type1 = 'Cloth'
        aa = Userinfo.objects.filter(username=enduser1)
        phone2 = aa[0].phone
        address2 = aa[0].address
        superuser1 = Finaluser(superuser=user, enduser=enduser1, phone=phone2,
                               address=address2, type1=type1, description=desc, done=0)
        superuser1.save()
        notify = Notification(superuser=user, enduser=enduser1, phone=phone1,
                              address=address, type1=type1, description=desc, done=0)
        notify.save()
        clothes1.delete()
        messages.success(request, "You Confirmed Clothes Order")
        params = {'clothes': clothes, 'foods': foods, 'others': others}
        return render(request, 'mysite/dashboard.html', params)
    else:
        messages.error(request, "You are not authorised to call this API")
        return redirect('home')


@login_required(login_url='handleLogin')
def notify(request):
    users = request.user
    noti = Notification.objects.filter(enduser=users).order_by('-id')
    params = {'notis': noti}
    return render(request, 'mysite/notification.html', params)


@login_required(login_url='handleLogin')
def donateOther(request):
    if(request.method == 'POST'):
        exampleOtherDescription = request.POST['exampleOtherDescription']
        try:
            user = request.user
            user1 = Userinfo.objects.filter(username=user)
            pin1 = user1[0].pin
            address = user1[0].address
            phone = user1[0].phone
            donate = DonatedOther(otherDescription=exampleOtherDescription,
                                  user=user, pin=pin1, phone=phone, address=address)
            donate.save()
            messages.success(
                request, "Your response has been Submitted Successfully. Thank You!")
            return redirect('home')
        except:
            messages.error(
                request, "You are not logged in. Or you are not be a member. Please Login to Donate")
    return render(request, 'mysite/donateOther.html')


@login_required(login_url='handleLogin')
def acceptOther(request, slug):
    user = request.user
    if(user.is_superuser):
        user1 = Userinfo.objects.filter(username=user)
        pin1 = user1[0].pin
        clothes = DonatedCloth.objects.filter(pin=pin1).order_by('-no')
        others = DonatedOther.objects.filter(pin=pin1).order_by('-no')
        foods = DonatedFood.objects.filter(pin=pin1).order_by('-no')
        others1 = DonatedOther.objects.filter(no=slug)
        enduser1 = others[0].user
        phone1 = user1[0].phone
        address = user1[0].address
        desc = others1[0].otherDescription
        type1 = 'Other'
        aa = Userinfo.objects.filter(username=enduser1)
        phone2 = aa[0].phone
        address2 = aa[0].address
        superuser1 = Finaluser(superuser=user, enduser=enduser1, phone=phone2,
                               address=address2, type1=type1, description=desc, done=0)
        superuser1.save()
        notify = Notification(superuser=user, enduser=enduser1, phone=phone1,
                              address=address, type1=type1, description=desc, done=0)
        notify.save()
        others1.delete()
        messages.success(request, "You Confirmed Others Order")
        params = {'clothes': clothes, 'foods': foods, 'others': others}
        return render(request, 'mysite/dashboard.html', params)
    else:
        messages.error(request, "You are not authorised to call this API")
        return redirect('home')


@login_required(login_url='handleLogin')
def acceptedOrder(request):
    users = request.user
    noti = Finaluser.objects.filter(superuser=users).order_by('-id')
    params = {'notis': noti}
    return render(request, 'mysite/acceptedOrder.html', params)
# created by decoders
