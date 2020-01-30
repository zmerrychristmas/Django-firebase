import pyrebase

from django.shortcuts import render, redirect
from django.contrib import auth

config = {
    'apiKey': "AIzaSyAtH-SPS013IWRl1h1xE3dTg6-sWMjbEFM",
    'authDomain': "fir-authendemo-c6c98.firebaseapp.com",
    'databaseURL': "https://fir-authendemo-c6c98.firebaseio.com",
    'projectId': "fir-authendemo-c6c98",
    'storageBucket': "fir-authendemo-c6c98.appspot.com",
    'messagingSenderId': "683258687467",
    'appId': "1:683258687467:web:2b5fd78a3349f70ceab3ae",
    'measurementId': "G-7T79B5JSKK"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
        print(user['idToken'])
        session_id=user['idToken']
        request.session['uid']=str(session_id)
        return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=auth.create_user_with_email_and_password(email,passw)
        # print(database.child("users").get())
        print(user['localId'])
        print(auth)
        uid = user['localId']
        data={"name":name,"status":"1"}
        mss = database.child("users").child(uid).child("details").set(data)
        # print(mss)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    return render(request,"signIn.html")

def create(request):

    return render(request,'create.html')


def post_create(request):

    import time
    from datetime import datetime, timezone
    import pytz

    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress =request.POST.get('progress')

    idtoken= request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        'progress':progress
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'Welcome.html', {'e':name})