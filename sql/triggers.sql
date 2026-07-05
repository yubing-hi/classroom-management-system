-- 预约冲突检测与审核状态同步触发器

DELIMITER $$

CREATE TRIGGER trg_reservation_before_insert
BEFORE INSERT ON Reservation
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Reservation r
        WHERE r.classroom_id = NEW.classroom_id
          AND r.reservation_date = NEW.reservation_date
          AND r.status = 'APPROVED'
          AND NEW.start_period <= r.end_period
          AND NEW.end_period >= r.start_period
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '该时段教室已被预约';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM Schedule s
        WHERE s.classroom_id = NEW.classroom_id
          AND s.weekday = ((DAYOFWEEK(NEW.reservation_date) + 5) % 7) + 1
          AND NEW.start_period <= s.end_period
          AND NEW.end_period >= s.start_period
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = '该时段教室有课程安排';
    END IF;
END$$

CREATE TRIGGER trg_reservation_before_update
BEFORE UPDATE ON Reservation
FOR EACH ROW
BEGIN
    IF NEW.status = 'APPROVED' AND (OLD.status IS NULL OR OLD.status <> 'APPROVED') THEN
        IF EXISTS (
            SELECT 1
            FROM Reservation r
            WHERE r.classroom_id = NEW.classroom_id
              AND r.reservation_date = NEW.reservation_date
              AND r.status = 'APPROVED'
              AND r.reservation_id <> NEW.reservation_id
              AND NEW.start_period <= r.end_period
              AND NEW.end_period >= r.start_period
        ) THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '该时段教室已被预约';
        END IF;

        IF EXISTS (
            SELECT 1
            FROM Schedule s
            WHERE s.classroom_id = NEW.classroom_id
              AND s.weekday = ((DAYOFWEEK(NEW.reservation_date) + 5) % 7) + 1
              AND NEW.start_period <= s.end_period
              AND NEW.end_period >= s.start_period
        ) THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = '该时段教室有课程安排';
        END IF;
    END IF;
END$$

CREATE TRIGGER trg_reservation_audit_after_insert
AFTER INSERT ON Reservation_Audit
FOR EACH ROW
BEGIN
    UPDATE Reservation
    SET status = CASE WHEN NEW.audit_result = 'APPROVED' THEN 'APPROVED' ELSE 'REJECTED' END
    WHERE reservation_id = NEW.reservation_id;
END$$

DELIMITER ;
