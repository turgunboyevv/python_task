-- EduPlatform uchun SQL Skript
-- Generatsiya qilingan sana: 2025-06-12T20:28:58.146577

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
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497420475407, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-12T20:27:27.506542', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497420475965, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-12T20:27:27.510557', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497420476005, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:27:27.529979', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497420475899, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:27:27.545743', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497420475957, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-12T20:27:27.547315', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497421237635, N'Jasurbek Turgunboyev', N'turgunboyevv777@gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:28:43.704770', N'Sinf: 9-A');
