from pymysql.cursors import DictCursor

from db_connect import get_connection

TABLES = [
    'Reservation_Audit', 'Reservation', 'Schedule', 'Course',
    'Classroom_Device', 'Device', 'Classroom', 'User',
]

SEED = [
    (
        'INSERT INTO `User` (user_id,name,password,phone,email,role,status) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        [
            ('1001', '张老师', '123456', '13800000001', 'teacher1@example.com', 'TEACHER', 'ACTIVE'),
            ('1002', '王老师', '123456', '13800000002', 'teacher2@example.com', 'TEACHER', 'ACTIVE'),
            ('2001', '李学生', '123456', '13800000003', 'student1@example.com', 'STUDENT', 'ACTIVE'),
            ('9001', '管理员', '123456', '13800000099', 'admin@example.com', 'ADMIN', 'ACTIVE'),
        ],
    ),
    (
        'INSERT INTO Classroom (building,room_number,capacity,floor,status) VALUES (%s,%s,%s,%s,%s)',
        [('A', '101', 120, 1, 'AVAILABLE'), ('A', '102', 80, 1, 'AVAILABLE'), ('B', '301', 60, 3, 'AVAILABLE')],
    ),
    (
        'INSERT INTO Device (device_name,device_type,description) VALUES (%s,%s,%s)',
        [('投影仪', '多媒体', '教室投影设备'), ('空调', '环境', '空调设备')],
    ),
    (
        'INSERT INTO Classroom_Device (classroom_id,device_id,quantity) VALUES (%s,%s,%s)',
        [(1, 1, 1), (1, 2, 2), (2, 1, 1)],
    ),
    (
        'INSERT INTO Course (course_name,teacher_id) VALUES (%s,%s)',
        [('数据库系统', '1001')],
    ),
    (
        'INSERT INTO Schedule (course_id,classroom_id,weekday,start_period,end_period,start_week,end_week) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        [(1, 1, 3, 3, 4, 1, 16)],
    ),
    (
        'INSERT INTO Reservation (user_id,classroom_id,reservation_date,start_period,end_period,purpose) VALUES (%s,%s,%s,%s,%s,%s)',
        [('2001', 1, '2026-07-10', 5, 6, '学生社团活动')],
    ),
    (
        'INSERT INTO Reservation_Audit (reservation_id,admin_id,audit_result,audit_comment) VALUES (%s,%s,%s,%s)',
        [(1, '9001', 'APPROVED', '审核通过')],
    ),
]


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SET FOREIGN_KEY_CHECKS=0')
            for table in TABLES:
                cur.execute(f'DELETE FROM `{table}`')
                cur.execute(f'ALTER TABLE `{table}` AUTO_INCREMENT = 1')
            cur.execute('SET FOREIGN_KEY_CHECKS=1')
            for sql, rows in SEED:
                cur.executemany(sql, rows)
        conn.commit()

        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT user_id, name, role FROM `User`')
            print('用户数据：')
            for row in cur.fetchall():
                print(f"  {row['user_id']} | {row['name']} | {row['role']}")
        print('测试数据导入成功')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
