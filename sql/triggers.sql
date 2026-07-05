USE classroom_management;

DROP TRIGGER IF EXISTS trg_reservation_before_insert;
DROP TRIGGER IF EXISTS trg_reservation_audit_after_insert;

DELIMITER //

CREATE TRIGGER trg_reservation_before_insert
BEFORE INSERT ON `Reservation`
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM `Reservation` r
        WHERE r.classroom_id = NEW.classroom_id
          AND r.reservation_date = NEW.reservation_date
          AND r.status IN ('PENDING', 'APPROVED')
          AND NEW.start_period <= r.end_period
          AND NEW.end_period >= r.start_period
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '该时段教室已有预约申请或已通过预约';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM `Schedule` s
        WHERE s.classroom_id = NEW.classroom_id
          AND s.weekday = WEEKDAY(NEW.reservation_date) + 1
          AND NEW.start_period <= s.end_period
          AND NEW.end_period >= s.start_period
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '该时段教室有课程安排';
    END IF;
END//

CREATE TRIGGER trg_reservation_audit_after_insert
AFTER INSERT ON `Reservation_Audit`
FOR EACH ROW
BEGIN
    UPDATE `Reservation`
    SET status = NEW.audit_result
    WHERE reservation_id = NEW.reservation_id;
END//

DELIMITER ;

-- 如果测试数据先于触发器导入，已有审核记录不会触发 AFTER INSERT。
-- 这里按每条预约的最新审核记录同步一次状态，保证本地测试结果一致。
UPDATE `Reservation` r
JOIN (
    SELECT ra.reservation_id, ra.audit_result
    FROM `Reservation_Audit` ra
    JOIN (
        SELECT reservation_id, MAX(audit_id) AS latest_audit_id
        FROM `Reservation_Audit`
        GROUP BY reservation_id
    ) latest ON ra.audit_id = latest.latest_audit_id
) latest_audit ON r.reservation_id = latest_audit.reservation_id
SET r.status = latest_audit.audit_result;
