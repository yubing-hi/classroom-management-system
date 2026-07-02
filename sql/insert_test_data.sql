USE classroom_management;

INSERT INTO `User` (user_id, name, password, phone, email, role, status)
VALUES
    ('1001', '张老师', '123456', '13800000001', 'teacher1@example.com', 'TEACHER', 'ACTIVE'),
    ('1002', '王老师', '123456', '13800000002', 'teacher2@example.com', 'TEACHER', 'ACTIVE'),
    ('2001', '李学生', '123456', '13800000003', 'student1@example.com', 'STUDENT', 'ACTIVE'),
    ('9001', '管理员', '123456', '13800000099', 'admin@example.com', 'ADMIN', 'ACTIVE');

INSERT INTO `Classroom` (building, room_number, capacity, floor, status)
VALUES
    ('A', '101', 120, 1, 'AVAILABLE'),
    ('A', '102', 80, 1, 'AVAILABLE'),
    ('B', '301', 60, 3, 'AVAILABLE');

INSERT INTO `Device` (device_name, device_type, description)
VALUES
    ('投影仪', '多媒体', '教室投影设备'),
    ('空调', '环境', '空调设备');

INSERT INTO `Classroom_Device` (classroom_id, device_id, quantity)
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 1, 1);

INSERT INTO `Course` (course_name, teacher_id)
VALUES
    ('数据库系统', '1001');

INSERT INTO `Schedule` (course_id, classroom_id, weekday, start_period, end_period, start_week, end_week)
VALUES
    (1, 1, 3, 3, 4, 1, 16);

INSERT INTO `Reservation` (user_id, classroom_id, reservation_date, start_period, end_period, purpose)
VALUES
    ('2001', 1, '2026-07-10', 5, 6, '学生社团活动');

INSERT INTO `Reservation_Audit` (reservation_id, admin_id, audit_result, audit_comment)
VALUES
    (1, '9001', 'APPROVED', '审核通过');
