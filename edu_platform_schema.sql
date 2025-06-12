-- Eduplatform uchun sql skript

-- Jadvallarni yaratish

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

--  Ma'lumotlarni jadvallarga qo'shish

-- Users
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497072356648, N'Admin Akmalov', N'admin@edu.com', N'Admin', NULL, NULL, N'2025-06-12T10:47:15.600583', N'');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497072356205, N'Ustoz Olimov', N'teacher@edu.com', N'O''qituvchi', NULL, NULL, N'2025-06-12T10:47:15.616203', N'Fanlar: Matematika, Fizika');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497072356462, N'Ali Valiyev', N'ali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T10:47:15.618645', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497072356286, N'Vali Aliyev', N'vali@edu.com', N'O''quvchi', NULL, NULL, N'2025-06-12T10:47:15.622597', N'Sinf: 9-A');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497072356725, N'Valiyev Ota', N'parent@edu.com', N'Ota-ona', NULL, NULL, N'2025-06-12T10:47:15.631383', N'Farzandlar soni: 2');
INSERT INTO Users (ID, FullName, Email, Role, Phone, Address, RegisteredAt, ExtraInfo) VALUES (17497073468052, N'Jaxongir Turgunboyev', N'turgunboyevv7:gmail.com', N'O''quvchi', NULL, NULL, N'2025-06-12T10:49:06.716607', N'Sinf: 11-A');
