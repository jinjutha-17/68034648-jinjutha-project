from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from apps.tenants.models import UserProfile


def login_view(request):
    """
    Login system with role-based redirect (Admin / Tenant / Staff)
    """

    next_url = request.GET.get('next') or request.POST.get('next') or '/dashboard/'

    if request.method == 'POST':
        login_input = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Email or Username support
        if '@' in login_input:
            user_obj = User.objects.filter(email=login_input).first()
            username = user_obj.username if user_obj else login_input
        else:
            username = login_input

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'Tenant'}
            )

            login_role = request.POST.get('login_role', 'tenant')
            is_admin_or_staff = profile.role in ('Admin', 'Staff') or user.is_staff or user.is_superuser
            is_tenant = profile.role == 'Tenant' and not user.is_staff and not user.is_superuser

            if login_role == 'admin' and not is_admin_or_staff:
                messages.error(request, 'บัญชีนี้ไม่มีสิทธิ์เข้าระบบแอดมิน กรุณาใช้แท็บผู้เช่า')
            elif login_role == 'tenant' and not is_tenant:
                messages.error(request, 'บัญชีนี้ไม่ใช่ผู้เช่า กรุณาเลือกแท็บ แอดมิน / สตาฟ')
            else:
                login(request, user)

                from django.middleware.csrf import rotate_token
                rotate_token(request)

                messages.success(request, f'ยินดีต้อนรับคุณ {user.username}')

                if user.is_superuser or profile.role == "Admin":
                    return redirect("/dashboard/")
                elif user.is_staff or profile.role == "Staff":
                    return redirect("/dashboard/")
                else:
                    return redirect("tenants:tenant_home")

        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')

    return render(request, 'dashboard/login.html', {'next': next_url})


def register_view(request):
    """
    Register new user (default role = Tenant)
    """

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username or not email or not password:
            messages.error(request, 'กรุณากรอกข้อมูลให้ครบถ้วน')

        elif password != password_confirm:
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'ชื่อผู้ใช้นี้ถูกใช้งานแล้ว')

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            if full_name:
                names = full_name.split(' ', 1)
                user.first_name = names[0]
                user.last_name = names[1] if len(names) > 1 else '-'
                user.save()

            UserProfile.objects.create(user=user, role='Tenant')

            # สร้าง Tenant อัตโนมัติตอน register
            from apps.tenants.models import Tenant
            Tenant.objects.create(
                first_name=user.first_name or username,
                last_name=user.last_name or '-',
                email=email,
                phone='',
            )

            login(request, user)

            return redirect("tenants:tenant_home")

    return render(request, 'dashboard/register.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')