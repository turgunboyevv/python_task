-- EduPlatform uchun SQL Skript
-- Generatsiya qilingan sana: 2025-06-14T15:40:37.565966

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
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498973042799, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-14T15:35:04.235873', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498973043058, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-14T15:35:04.251816', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498973043318, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-14T15:35:04.267688', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498973043476, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-14T15:35:04.283543', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498973043335, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-14T15:35:04.299694', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498974348613, N'turgunboyevv jaxongir', N'turgunboyevv777@gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-14T15:37:14.865382', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17498974482811, N'0', N'0', N'O''quvchi', NULL, NULL, N'2025-06-14T15:37:28.276827', N'Sinf: 0');

-- Ma'lumotlar: Assignments
INSERT INTO Assignments (ID, Title, Subject, ClassID, Deadline, Difficulty, TeacherID, SubmissionsCount) VALUES (17498976374632, N'assignment', N'Matematika', N'9-A', N'2025-06-15T23:59:59', N'qiyin', 17498973043058, 0);
