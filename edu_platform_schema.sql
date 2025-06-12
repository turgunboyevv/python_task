-- EduPlatform uchun SQL Skript
-- Generatsiya qilingan sana: 2025-06-12T19:41:08.719427

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
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497390502946, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-12T19:37:30.260328', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497390503303, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-12T19:37:30.268960', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497390503089, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T19:37:30.277856', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497390503278, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T19:37:30.300843', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497390503908, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-12T19:37:30.310955', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497392620129, N'Turgunboyev Jaxongir', N'turgunboyevv7@gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-12T19:41:01.945494', N'Sinf: 10-A');
