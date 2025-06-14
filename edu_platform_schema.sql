-- EduPlatform uchun SQL Skript
-- Generatsiya qilingan sana: 2025-06-14T14:23:32.327663

-- 1. Jadvallarni yaratish

CREATE TABLE Users (
    ID BIGINT PRIMARY KEY,
    FullName NVARCHAR(255) NOT NULL,
    Email NVARCHAR(255) UNIQUE,
    Role NVARCHAR(50),
    Phone NVARCHAR(50),
    Address NVARCHAR(MAX),
    RegisteredAt DATETIME,
    ExtraInfo NVARCHAR(MAX)
);

CREATE TABLE Assignments (
    ID BIGINT PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Subject NVARCHAR(100),
    ClassID NVARCHAR(50),
    Deadline DATETIME,
    Difficulty NVARCHAR(50),
    TeacherID BIGINT,
    SubmissionsCount INT
);

CREATE TABLE Grades (
    ID BIGINT PRIMARY KEY,
    StudentID BIGINT,
    Subject NVARCHAR(100),
    Grade INT CHECK (Grade >= 1 AND Grade <= 5),
    GradeDate DATETIME,
    TeacherID BIGINT,
    Comment NVARCHAR(MAX)
);

-- 2. Ma'lumotlarni jadvallarga qo'shish

-- Ma'lumotlar: Users
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498929160244, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-14T14:21:55.950687', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498929160106, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-14T14:21:55.967239', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498929160372, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-14T14:21:55.987006', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498929160370, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-14T14:21:56.003040', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498929160130, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-14T14:21:56.019283', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498930121651, N'turgunboyev jaxon', N'turgunboyevv@gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-14T14:23:32.097503', N'Sinf: 9-A');
