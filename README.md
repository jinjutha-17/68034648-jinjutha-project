ลิงก์วิดิโอนำเสนอ https://drive.google.com/file/d/1fUaSRYIFHjRchkaUcK2ORj9eu7QBkyig/view?usp=drive_link

# 68034648-jinjutha-project
# 🏢 Apartment Management System

ระบบจัดการอพาร์ตเมนต์แบบครบวงจร (Apartment Rental Management System)

---

## 📌 Project Overview (ภาพรวมโครงการ)

ระบบนี้ถูกพัฒนาขึ้นเพื่อช่วยในการบริหารจัดการอพาร์ตเมนต์ให้เป็นระบบมากยิ่งขึ้น ลดความซับซ้อนในการทำงานของผู้ดูแล (Admin) และเพิ่มความสะดวกให้กับผู้เช่า (Tenant) โดยรองรับตั้งแต่การจัดการห้องพัก การจอง การแจ้งซ่อม ไปจนถึงการชำระเงิน

พัฒนาโดยใช้ **Django Framework** เชื่อมต่อกับฐานข้อมูล **PostgreSQL / SQLite** และออกแบบให้ใช้งานผ่าน Web Application

---

## 🎯 Objectives (วัตถุประสงค์)

* เพื่อพัฒนาระบบบริหารจัดการอพาร์ตเมนต์แบบอัตโนมัติ
* ลดการใช้เอกสาร และลดข้อผิดพลาดจากการทำงานแบบ Manual
* เพิ่มความสะดวกในการติดตามข้อมูล เช่น ห้องว่าง การชำระเงิน และงานซ่อม
* รองรับการขยายระบบในอนาคต

---

## 🚀 Features (ฟีเจอร์หลักของระบบ)

### 🏠 ระบบจัดการห้องพัก (Room Management)

* เพิ่ม / แก้ไข / ลบ ห้องพัก
* แสดงสถานะห้อง (ว่าง / ไม่ว่าง / จองแล้ว)
* แยกประเภทห้อง

### 👤 ระบบจัดการผู้เช่า (Tenant Management)

* บันทึกข้อมูลผู้เช่า
* วันเข้าอยู่ / วันย้ายออก
* ประวัติการเช่า

### 📅 ระบบจองห้อง (Booking System)

* ผู้เช่าสามารถจองห้องล่วงหน้า
* ตรวจสอบสถานะการจอง
* ป้องกันการจองซ้ำ

### 🔧 ระบบแจ้งซ่อม (Maintenance System)

* ผู้เช่าแจ้งปัญหา (แนบรูปได้)
* Admin รับเรื่องและมอบหมายงาน
* อัปเดตสถานะ (รอดำเนินการ / กำลังซ่อม / เสร็จสิ้น)

### 💰 ระบบชำระเงิน (Payment System)

* คำนวณค่าเช่าอัตโนมัติ
* บันทึกการชำระเงิน
* ตรวจสอบสถานะค้างชำระ

### 📊 Dashboard

* แสดงภาพรวมของระบบ
* จำนวนห้องว่าง
* รายได้ / สถานะการเช่า
* งานแจ้งซ่อมล่าสุด

---

## 👥 User Roles (บทบาทผู้ใช้งาน)

### 🔑 Admin (ผู้ดูแลระบบ)

* จัดการห้องพัก
* ดูและแก้ไขข้อมูลผู้เช่า
* ตรวจสอบการจอง
* จัดการแจ้งซ่อม
* ตรวจสอบและบันทึกการชำระเงิน

### 🧑‍💼 Tenant (ผู้เช่า)

* ดูข้อมูลห้อง
* จองห้อง
* แจ้งซ่อม
* ตรวจสอบสถานะการเช่า
* ดูประวัติการชำระเงิน

---

## 🔄 System Flow (ลำดับการทำงานของระบบ)

### 📌 1. การเริ่มต้นใช้งาน

* ผู้ใช้เข้าสู่ระบบ (Login)
* ระบบตรวจสอบสิทธิ์ (Admin / Tenant)

---

### 🏠 2. Flow การเช่าห้อง

1. ผู้เช่าเลือกดูห้องว่าง
2. ทำการจองห้อง
3. Admin ตรวจสอบและอนุมัติ
4. เปลี่ยนสถานะห้องเป็น "ไม่ว่าง"
5. บันทึกข้อมูลผู้เช่าเข้าระบบ

---

### 🔧 3. Flow การแจ้งซ่อม

1. ผู้เช่าแจ้งปัญหา (เลือกประเภท + รายละเอียด + แนบรูป)
2. ระบบบันทึกสถานะ "รอดำเนินการ"
3. Admin รับเรื่อง
4. มอบหมายงานให้ช่าง
5. อัปเดตสถานะเป็น "กำลังซ่อม"
6. เมื่อเสร็จ เปลี่ยนเป็น "เสร็จสิ้น"

---

### 💰 4. Flow การชำระเงิน

1. Admin กรอกเลขมิเตอร์ / ค่าใช้จ่าย
2. ระบบคำนวณค่าเช่าอัตโนมัติ
3. สร้างใบแจ้งหนี้
4. ผู้เช่าชำระเงิน
5. ระบบอัปเดตสถานะเป็น "ชำระแล้ว"

---

### 📊 5. Flow Dashboard

* ดึงข้อมูลจากทุกระบบ
* แสดงผลแบบสรุป
* ใช้ในการตัดสินใจของ Admin

---

## 🛠 Tech Stack

* **Backend:** Django 5
* **Database:** PostgreSQL / SQLite
* **Frontend:** HTML, CSS, Bootstrap
* **Tools:** VS Code, GitHub

---

## ⚙️ Installation (วิธีติดตั้งระบบ)

### 1. Clone Project

```bash
git clone https://github.com/your-username/apartment.git
cd apartment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
copy .env.example .env
```

### 4. Run Migration

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

---

## 📁 Project Structure

```
apartment/
│
├── apartment_project/
├── apps/
│   ├── rooms/
│   ├── tenants/
│   ├── bookings/
│   ├── payments/
│   ├── maintenance/
│   └── dashboard/
│
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

---

## 📈 Advantages (ข้อดีของระบบ)

* ลดงานเอกสาร
* ลดความผิดพลาดจากมนุษย์
* ตรวจสอบข้อมูลได้แบบ Real-time
* เพิ่มความสะดวกให้ทั้งผู้ดูแลและผู้เช่า

---

## 🔮 Future Improvements (พัฒนาต่อในอนาคต)

* เพิ่มระบบแจ้งเตือน (Notification)
* รองรับ Mobile Application
* เชื่อมต่อระบบชำระเงินออนไลน์ (QR PromptPay)
* เพิ่มระบบรายงานขั้นสูง (Analytics)

---

## 📄 License

This project is developed for educational purposes.

