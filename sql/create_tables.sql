-- 创建数据库
CREATE DATABASE IF NOT EXISTS classroom_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE classroom_management;

-- 用户表
CREATE TABLE IF NOT EXISTS `User` (
    user_id VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    role ENUM('ADMIN', 'TEACHER', 'STUDENT') NOT NULL,
    status ENUM('ACTIVE', 'DISABLED') NOT NULL DEFAULT 'ACTIVE',
    PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 教室表
CREATE TABLE IF NOT EXISTS `Classroom` (
    classroom_id INT AUTO_INCREMENT,
    building VARCHAR(50) NOT NULL,
    room_number VARCHAR(20) NOT NULL,
    capacity INT NOT NULL,
    floor INT NOT NULL,
    status ENUM('AVAILABLE', 'MAINTENANCE') NOT NULL DEFAULT 'AVAILABLE',
    PRIMARY KEY (classroom_id),
    UNIQUE KEY uk_classroom_building_room (building, room_number),
    CHECK (capacity > 0),
    CHECK (floor >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 设备表
CREATE TABLE IF NOT EXISTS `Device` (
    device_id INT AUTO_INCREMENT,
    device_name VARCHAR(50) NOT NULL,
    device_type VARCHAR(50) NOT NULL,
    description TEXT NULL,
    PRIMARY KEY (device_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 教室设备关联表
CREATE TABLE IF NOT EXISTS `Classroom_Device` (
    id INT AUTO_INCREMENT,
    classroom_id INT NOT NULL,
    device_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT fk_classroom_device_classroom
        FOREIGN KEY (classroom_id) REFERENCES `Classroom`(classroom_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_classroom_device_device
        FOREIGN KEY (device_id) REFERENCES `Device`(device_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (quantity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 课程表
CREATE TABLE IF NOT EXISTS `Course` (
    course_id INT AUTO_INCREMENT,
    course_name VARCHAR(100) NOT NULL,
    teacher_id VARCHAR(20) NOT NULL,
    PRIMARY KEY (course_id),
    CONSTRAINT fk_course_teacher
        FOREIGN KEY (teacher_id) REFERENCES `User`(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 课程安排表
CREATE TABLE IF NOT EXISTS `Schedule` (
    schedule_id INT AUTO_INCREMENT,
    course_id INT NOT NULL,
    classroom_id INT NOT NULL,
    weekday TINYINT NOT NULL,
    start_period TINYINT NOT NULL,
    end_period TINYINT NOT NULL,
    start_week INT NOT NULL,
    end_week INT NOT NULL,
    PRIMARY KEY (schedule_id),
    CONSTRAINT fk_schedule_course
        FOREIGN KEY (course_id) REFERENCES `Course`(course_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_schedule_classroom
        FOREIGN KEY (classroom_id) REFERENCES `Classroom`(classroom_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (weekday BETWEEN 1 AND 7),
    CHECK (start_period BETWEEN 1 AND 13),
    CHECK (end_period BETWEEN 1 AND 13),
    CHECK (start_period <= end_period),
    CHECK (start_week <= end_week),
    CHECK (start_week > 0),
    CHECK (end_week > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 预约表
CREATE TABLE IF NOT EXISTS `Reservation` (
    reservation_id INT AUTO_INCREMENT,
    user_id VARCHAR(20) NOT NULL,
    classroom_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    start_period TINYINT NOT NULL,
    end_period TINYINT NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    apply_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED') NOT NULL DEFAULT 'PENDING',
    PRIMARY KEY (reservation_id),
    CONSTRAINT fk_reservation_user
        FOREIGN KEY (user_id) REFERENCES `User`(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_reservation_classroom
        FOREIGN KEY (classroom_id) REFERENCES `Classroom`(classroom_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (start_period BETWEEN 1 AND 13),
    CHECK (end_period BETWEEN 1 AND 13),
    CHECK (start_period <= end_period)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 预约审核表
CREATE TABLE IF NOT EXISTS `Reservation_Audit` (
    audit_id INT AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    admin_id VARCHAR(20) NOT NULL,
    audit_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    audit_result ENUM('APPROVED', 'REJECTED') NOT NULL,
    audit_comment VARCHAR(255) NULL,
    PRIMARY KEY (audit_id),
    CONSTRAINT fk_audit_reservation
        FOREIGN KEY (reservation_id) REFERENCES `Reservation`(reservation_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_audit_admin
        FOREIGN KEY (admin_id) REFERENCES `User`(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 系统配置表
CREATE TABLE IF NOT EXISTS `System_Config` (
    config_key VARCHAR(50) NOT NULL,
    config_value VARCHAR(255) NOT NULL,
    PRIMARY KEY (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `System_Config` (config_key, config_value) VALUES
    ('semester_start_date', '2026-02-24'),
    ('semester_total_weeks', '20')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);
