-- EduPlatform uchun SQL Skript
-- Generatsiya qilingan sana: 2025-06-12T20:45:39.032853

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
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497426867443, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-12T20:38:06.670097', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497426867300, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-12T20:38:06.672086', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497426867120, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:38:06.674027', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497426866741, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:38:06.683300', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497426867633, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-12T20:38:06.698381', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497427421401, N'Failiya ism', N'ism@gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-12T20:39:02.051632', N'Sinf: 9-A');

-- Ma'lumotlar: Assignments
INSERT INTO Assignments (ID, Title, Subject, ClassID, Deadline, Difficulty, TeacherID, SubmissionsCount) VALUES (17497428368651, N'something new', N'Matematika', N'9-A', N'2025-06-13T23:59:59', N'oson', 17497426867300, 1);

-- Ma'lumotlar: Grades
INSERT INTO Grades (ID, StudentID, Subject, Grade, GradeDate, TeacherID, Comment) VALUES (17497431390030, 17497427421401, N'Matematika', 4, N'2025-06-12T20:45:38.974973', 17497426867300, N'yomon emas');
