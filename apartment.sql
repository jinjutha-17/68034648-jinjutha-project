USE master;
GO
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'ApartmentDB') 
    ALTER DATABASE ApartmentDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE ApartmentDB;
GO
CREATE DATABASE ApartmentDB;
GO
USE ApartmentDB;
GO

-- 1. ห้องพัก
CREATE TABLE Rooms (RoomID INT PRIMARY KEY IDENTITY, RoomNumber NVARCHAR(10), Status NVARCHAR(20));
-- 2. ผู้เช่า
CREATE TABLE Tenants (TenantID INT PRIMARY KEY IDENTITY, FullName NVARCHAR(100), Phone NVARCHAR(20));
-- 3. สัญญาเช่า + ค่าน้ำไฟ (องค์ประกอบสำคัญ)
CREATE TABLE Invoices (InvoiceID INT PRIMARY KEY IDENTITY, RoomNumber NVARCHAR(10), TenantName NVARCHAR(100), WaterBill DECIMAL(10,2), ElecBill DECIMAL(10,2), Total DECIMAL(10,2));
-- 4. การแจ้งซ่อม
CREATE TABLE Repairs (RepairID INT PRIMARY KEY IDENTITY, RoomNumber NVARCHAR(10), Description NVARCHAR(MAX), Status NVARCHAR(20));

-- ใส่ข้อมูลตัวอย่าง (เพื่อให้หน้าเว็บไม่ว่าง)
INSERT INTO Rooms VALUES ('101', 'Occupied'), ('102', 'Available');
INSERT INTO Tenants VALUES (N'สมชาย ใจดี', '081-222-3333');
INSERT INTO Invoices VALUES ('101', N'สมชาย ใจดี', 150, 450, 5600);
INSERT INTO Repairs VALUES ('101', N'แอร์ไม่เย็น', 'Pending');
GO