"""
Seed Script — อาคาร A 3 ชั้น ชั้นละ 10 ห้อง (30 ห้องรวม)
รันด้วย: python manage.py shell < seed_demo.py
"""
import os
import django
import random
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apartment_project.settings')
django.setup()

from django.contrib.auth.models import User
from apps.rooms.models import Room
from apps.tenants.models import Tenant, UserProfile
from apps.payments.models import Payment

# ===== ล้างข้อมูลเก่า (ถ้ามี) =====
print("🧹 ล้างข้อมูลเก่า...")
Payment.objects.all().delete()
Tenant.objects.all().delete()
Room.objects.all().delete()

# ===== ข้อมูลผู้เช่าจำลอง =====
TENANTS_DATA = [
    ("สมชาย",   "มีสุข",     "somchai@mail.com",   "0811111111"),
    ("สมหญิง",  "ใจดี",      "somying@mail.com",   "0822222222"),
    ("ประเสริฐ", "วงษ์ทอง",  "prasert@mail.com",   "0833333333"),
    ("มาลี",    "สุขสันต์",  "malee@mail.com",     "0844444444"),
    ("วิชัย",   "ทองดี",     "wichai@mail.com",    "0855555555"),
    ("นภา",     "แก้วใส",    "napa@mail.com",      "0866666666"),
    ("อนุชา",   "พรมมา",     "anucha@mail.com",    "0877777777"),
    ("จิตรา",   "บุญมา",     "jittra@mail.com",    "0888888888"),
    ("ธนากร",   "ศรีสุข",    "thanakorn@mail.com", "0899999999"),
    ("พรรณี",   "ลาภมาก",    "pannee@mail.com",    "0810101010"),
    ("กิตติ",   "เจริญ",     "kitti@mail.com",     "0821212121"),
    ("ลลิตา",   "นาคดี",     "lalita@mail.com",    "0832323232"),
    ("สุรชัย",  "โชคดี",     "surachai@mail.com",  "0843434343"),
    ("วันดี",   "มีทรัพย์",  "wandee@mail.com",    "0854545454"),
    ("ณัฐพล",   "รุ่งเรือง", "nattapon@mail.com",  "0865656565"),
    ("อรอนงค์", "สวัสดิ์",   "onanong@mail.com",   "0876767676"),
    ("ชัยวัฒน์","ทรัพย์มาก", "chaiwat@mail.com",   "0887878787"),
    ("ปิยะ",    "เกษมสุข",   "piya@mail.com",      "0898989898"),
    ("รุ่งทิวา", "ดีงาม",    "rungtiva@mail.com",  "0819090909"),
    ("ศักดิ์ชัย","วิไล",     "sakchai@mail.com",   "0820102010"),
]

# ===== สร้างห้อง 3 ชั้น ชั้นละ 10 ห้อง =====
print("🏢 สร้างห้องพัก...")
rooms = []
tenant_index = 0

# กำหนดสถานะห้อง: 20 ห้องมีคน, 7 ห้องว่าง, 3 ห้องซ่อม
statuses = ["ไม่ว่าง"] * 20 + ["ว่าง"] * 7 + ["ซ่อมบำรุง"] * 3
random.shuffle(statuses)

room_index = 0
for floor in range(1, 4):      # ชั้น 1, 2, 3
    for num in range(1, 11):   # ห้อง 01–10
        room_number = f"{floor}0{num}" if num < 10 else f"{floor}10"
        rent = Decimal(str(random.choice([3000, 3500, 4000, 4500])))
        status = statuses[room_index]

        room = Room.objects.create(
            room_number=room_number,
            floor=floor,
            room_type="รายเดือน",
            size_sqm=Decimal("28.00"),
            monthly_rent=rent,
            elec_rate=Decimal("7.00"),
            water_rate=Decimal("18.00"),
            status=status,
        )
        rooms.append((room, status))
        room_index += 1

print(f"  ✅ สร้างห้องทั้งหมด {len(rooms)} ห้อง")

# ===== สร้างผู้เช่า + ผูกกับห้องที่ "ไม่ว่าง" =====
print("👤 สร้างผู้เช่า...")
occupied_rooms = [r for r, s in rooms if s == "ไม่ว่าง"]
tenants_created = []

for i, room in enumerate(occupied_rooms):
    if i >= len(TENANTS_DATA):
        break
    fname, lname, email, phone = TENANTS_DATA[i]

    # สร้าง Django User
    username = email.split("@")[0]
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            email=email,
            password="1234",
            first_name=fname,
            last_name=lname,
        )
        UserProfile.objects.get_or_create(user=user, defaults={"role": "Tenant"})
    else:
        user = User.objects.get(username=username)

    # สร้าง Tenant
    tenant = Tenant.objects.create(
        first_name=fname,
        last_name=lname,
        email=email,
        phone=phone,
        room=room,
        move_in_date=date.today() - timedelta(days=random.randint(30, 365)),
        is_active=True,
    )
    tenants_created.append((tenant, room))

print(f"  ✅ สร้างผู้เช่าทั้งหมด {len(tenants_created)} คน")

# ===== สร้างข้อมูลการชำระเงิน =====
print("💰 สร้างข้อมูลการชำระเงิน...")
payment_count = 0
today = date.today()

for tenant, room in tenants_created:
    # ค่าเช่าเดือนที่แล้ว (จ่ายแล้ว)
    Payment.objects.create(
        tenant=tenant,
        room=room,
        payment_type="rent",
        amount=room.monthly_rent,
        due_date=today.replace(day=1) - timedelta(days=1),
        paid_date=today.replace(day=1) - timedelta(days=random.randint(1, 10)),
        status="paid",
    )
    payment_count += 1

    # ค่าเช่าเดือนนี้ (บางคนจ่ายแล้ว บางคนยังค้าง)
    status = random.choice(["paid", "paid", "pending", "overdue"])
    paid_date = today if status == "paid" else None
    Payment.objects.create(
        tenant=tenant,
        room=room,
        payment_type="rent",
        amount=room.monthly_rent,
        due_date=today.replace(day=5),
        paid_date=paid_date,
        status=status,
    )
    payment_count += 1

print(f"  ✅ สร้างรายการชำระเงิน {payment_count} รายการ")

# ===== สรุป =====
print("\n" + "="*40)
print("✅ Seed สำเร็จ!")
print(f"  🏢 ห้องทั้งหมด  : {Room.objects.count()} ห้อง")
print(f"  🟢 ว่าง         : {Room.objects.filter(status='ว่าง').count()} ห้อง")
print(f"  🔴 ไม่ว่าง      : {Room.objects.filter(status='ไม่ว่าง').count()} ห้อง")
print(f"  🔧 ซ่อมบำรุง   : {Room.objects.filter(status='ซ่อมบำรุง').count()} ห้อง")
print(f"  👤 ผู้เช่า      : {Tenant.objects.count()} คน")
print(f"  💰 รายการเงิน  : {Payment.objects.count()} รายการ")
print("="*40)
print("\nรันเสร็จแล้ว! เปิด http://127.0.0.1:8000/dashboard/ ได้เลย 🎉")
