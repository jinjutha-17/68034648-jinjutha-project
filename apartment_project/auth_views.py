from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def custom_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            # ส่งไปที่หน้า Dashboard (ต้องสะกด dashboard:dashboard ให้ตรงกับแอป)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')