USE classroom_management;

DROP VIEW IF EXISTS `View_Reservation_Detail`;
DROP VIEW IF EXISTS `View_Course_Schedule`;
DROP VIEW IF EXISTS `View_Classroom_Usage`;

CREATE VIEW `View_Reservation_Detail` AS
SELECT
    r.reservation_id,
    r.user_id,
    u.name AS user_name,
    u.role AS user_role,
    r.classroom_id,
    c.building,
    c.room_number,
    c.capacity,
    r.reservation_date,
    r.start_period,
    r.end_period,
    r.purpose,
    r.apply_time,
    r.status,
    ra.admin_id,
    admin_user.name AS admin_name,
    ra.audit_time,
    ra.audit_result,
    ra.audit_comment
FROM `Reservation` r
JOIN `User` u ON r.user_id = u.user_id
JOIN `Classroom` c ON r.classroom_id = c.classroom_id
LEFT JOIN `Reservation_Audit` ra
    ON ra.audit_id = (
        SELECT ra2.audit_id
        FROM `Reservation_Audit` ra2
        WHERE ra2.reservation_id = r.reservation_id
        ORDER BY ra2.audit_time DESC, ra2.audit_id DESC
        LIMIT 1
    )
LEFT JOIN `User` admin_user ON ra.admin_id = admin_user.user_id;

CREATE VIEW `View_Course_Schedule` AS
SELECT
    s.schedule_id,
    s.course_id,
    co.course_name,
    co.teacher_id,
    u.name AS teacher_name,
    s.classroom_id,
    c.building,
    c.room_number,
    s.weekday,
    s.start_period,
    s.end_period,
    s.start_week,
    s.end_week
FROM `Schedule` s
JOIN `Course` co ON s.course_id = co.course_id
JOIN `User` u ON co.teacher_id = u.user_id
JOIN `Classroom` c ON s.classroom_id = c.classroom_id;

CREATE VIEW `View_Classroom_Usage` AS
SELECT
    c.classroom_id,
    c.building,
    c.room_number,
    c.capacity,
    c.status,
    COUNT(DISTINCT s.schedule_id) AS schedule_count,
    COUNT(DISTINCT CASE WHEN r.status = 'APPROVED' THEN r.reservation_id END) AS approved_reservation_count,
    COUNT(DISTINCT CASE WHEN r.status = 'PENDING' THEN r.reservation_id END) AS pending_reservation_count
FROM `Classroom` c
LEFT JOIN `Schedule` s ON c.classroom_id = s.classroom_id
LEFT JOIN `Reservation` r ON c.classroom_id = r.classroom_id
GROUP BY c.classroom_id, c.building, c.room_number, c.capacity, c.status;
