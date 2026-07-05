-- 视图脚本

DROP VIEW IF EXISTS View_Reservation_Detail;
CREATE VIEW View_Reservation_Detail AS
SELECT
    r.reservation_id AS `预约ID`,
    r.user_id AS `申请人ID`,
    u.name AS `申请人姓名`,
    r.classroom_id AS `教室ID`,
    c.building AS `楼宇`,
    c.room_number AS `教室号`,
    r.reservation_date AS `预约日期`,
    r.start_period AS `开始节次`,
    r.end_period AS `结束节次`,
    r.purpose AS `用途`,
    r.apply_time AS `申请时间`,
    r.status AS `状态`,
    latest_audit.admin_id AS `审核人ID`,
    latest_audit.audit_time AS `审核时间`,
    latest_audit.audit_result AS `审核结果`,
    latest_audit.audit_comment AS `审核备注`,
    admin_user.name AS `审核人姓名`
FROM Reservation r
JOIN `User` u ON u.user_id = r.user_id
JOIN Classroom c ON c.classroom_id = r.classroom_id
LEFT JOIN (
    SELECT
        a.reservation_id,
        a.admin_id,
        a.audit_time,
        a.audit_result,
        a.audit_comment
    FROM Reservation_Audit a
    INNER JOIN (
        SELECT reservation_id, MAX(audit_id) AS audit_id
        FROM Reservation_Audit
        GROUP BY reservation_id
    ) latest ON latest.reservation_id = a.reservation_id AND latest.audit_id = a.audit_id
) latest_audit ON latest_audit.reservation_id = r.reservation_id
LEFT JOIN `User` admin_user ON admin_user.user_id = latest_audit.admin_id;

DROP VIEW IF EXISTS View_Course_Schedule;
CREATE VIEW View_Course_Schedule AS
SELECT
    s.schedule_id AS `排课ID`,
    s.course_id AS `课程ID`,
    c.course_name AS `课程名称`,
    c.teacher_id AS `教师ID`,
    t.name AS `教师姓名`,
    s.classroom_id AS `教室ID`,
    cl.building AS `楼宇`,
    cl.room_number AS `教室号`,
    s.weekday AS `星期`,
    s.start_period AS `开始节次`,
    s.end_period AS `结束节次`,
    s.start_week AS `开始周`,
    s.end_week AS `结束周`
FROM Schedule s
JOIN Course c ON c.course_id = s.course_id
JOIN `User` t ON t.user_id = c.teacher_id
JOIN Classroom cl ON cl.classroom_id = s.classroom_id;

DROP VIEW IF EXISTS View_Classroom_Usage;
CREATE VIEW View_Classroom_Usage AS
SELECT
    cl.classroom_id AS `教室ID`,
    cl.building AS `楼宇`,
    cl.room_number AS `教室号`,
    cl.capacity AS `容量`,
    cl.floor AS `楼层`,
    cl.status AS `状态`,
    COALESCE(schedule_stats.schedule_count, 0) AS `排课次数`,
    COALESCE(schedule_stats.total_schedule_periods, 0) AS `排课节次总数`,
    COALESCE(reservation_stats.reservation_count, 0) AS `预约次数`,
    COALESCE(reservation_stats.approved_reservation_count, 0) AS `已通过预约次数`,
    COALESCE(reservation_stats.total_reservation_periods, 0) AS `预约节次总数`
FROM Classroom cl
LEFT JOIN (
    SELECT
        classroom_id,
        COUNT(*) AS schedule_count,
        SUM(end_period - start_period + 1) AS total_schedule_periods
    FROM Schedule
    GROUP BY classroom_id
) schedule_stats ON schedule_stats.classroom_id = cl.classroom_id
LEFT JOIN (
    SELECT
        classroom_id,
        COUNT(*) AS reservation_count,
        SUM(CASE WHEN status = 'APPROVED' THEN 1 ELSE 0 END) AS approved_reservation_count,
        SUM(CASE WHEN status = 'APPROVED' THEN (end_period - start_period + 1) ELSE 0 END) AS total_reservation_periods
    FROM Reservation
    GROUP BY classroom_id
) reservation_stats ON reservation_stats.classroom_id = cl.classroom_id;
