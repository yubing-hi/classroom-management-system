USE classroom_management;

-- 1. 查询指定日期和节次范围内可预约教室
SET @target_date = '2026-07-10';
SET @start_period = 5;
SET @end_period = 6;

SELECT c.*
FROM `Classroom` c
WHERE c.status = 'AVAILABLE'
  AND NOT EXISTS (
      SELECT 1
      FROM `Reservation` r
      WHERE r.classroom_id = c.classroom_id
        AND r.reservation_date = @target_date
        AND r.status IN ('PENDING', 'APPROVED')
        AND @start_period <= r.end_period
        AND @end_period >= r.start_period
  )
  AND NOT EXISTS (
      SELECT 1
      FROM `Schedule` s
      WHERE s.classroom_id = c.classroom_id
        AND s.weekday = WEEKDAY(@target_date) + 1
        AND @start_period <= s.end_period
        AND @end_period >= s.start_period
  )
ORDER BY c.building, c.room_number;

-- 2. 管理员查看待审核预约
SELECT *
FROM `View_Reservation_Detail`
WHERE status = 'PENDING'
ORDER BY apply_time DESC;

-- 3. 用户查看自己的预约记录
SET @target_user_id = '2001';

SELECT *
FROM `View_Reservation_Detail`
WHERE user_id = @target_user_id
ORDER BY apply_time DESC;

-- 4. 热门教室统计
SELECT
    classroom_id,
    building,
    room_number,
    approved_reservation_count
FROM `View_Classroom_Usage`
ORDER BY approved_reservation_count DESC, classroom_id;

-- 5. 教师课程数量统计
SELECT
    teacher_id,
    teacher_name,
    COUNT(*) AS course_count
FROM `View_Course_Schedule`
GROUP BY teacher_id, teacher_name
ORDER BY course_count DESC, teacher_id;

-- 6. 月度预约数量统计
SELECT
    DATE_FORMAT(reservation_date, '%Y-%m') AS month,
    COUNT(*) AS reservation_count,
    SUM(status = 'APPROVED') AS approved_count,
    SUM(status = 'PENDING') AS pending_count
FROM `Reservation`
GROUP BY DATE_FORMAT(reservation_date, '%Y-%m')
ORDER BY month;
