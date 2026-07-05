import os
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from pymysql.cursors import DictCursor

from db_connect import get_connection

app = Flask(__name__)
CORS(app, supports_credentials=True)

JWT_SECRET = os.getenv('JWT_SECRET', 'classroom-management-secret')
JWT_EXPIRE_HOURS = 24


def ok(data=None, message='success'):
    return jsonify({'code': 0, 'message': message, 'data': data})


def fail(message, code=1, status=400):
    return jsonify({'code': code, 'message': message, 'data': None}), status


def get_token():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        return auth[7:]
    return None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token()
        if not token:
            return fail('未登录', code=401, status=401)
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            g.user = payload
        except jwt.ExpiredSignatureError:
            return fail('登录已过期', code=401, status=401)
        except jwt.InvalidTokenError:
            return fail('无效令牌', code=401, status=401)
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if g.user.get('role') != 'ADMIN':
            return fail('无权限', code=403, status=403)
        return f(*args, **kwargs)

    return wrapper


def period_overlap(s1, e1, s2, e2):
    return s1 <= e2 and s2 <= e1


def paginate(items, page, page_size):
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], total


def find_reservation_conflicts(cur, classroom_id, reservation_date, start_period, end_period, exclude_id=None):
    sql = '''
        SELECT reservation_id, user_id, start_period, end_period, status
        FROM Reservation
        WHERE classroom_id=%s
          AND reservation_date=%s
          AND status IN ('PENDING', 'APPROVED')
    '''
    params = [classroom_id, reservation_date]
    if exclude_id:
        sql += ' AND reservation_id != %s'
        params.append(exclude_id)
    cur.execute(sql, params)
    return [
        row for row in cur.fetchall()
        if period_overlap(start_period, end_period, row['start_period'], row['end_period'])
    ]


def find_schedule_conflicts(cur, classroom_id, reservation_date, start_period, end_period):
    date_obj = datetime.strptime(str(reservation_date), '%Y-%m-%d')
    weekday = date_obj.isoweekday()
    cur.execute(
        '''
        SELECT s.schedule_id, s.start_period, s.end_period,
               c.course_name, u.name AS teacher_name
        FROM Schedule s
        JOIN Course c ON s.course_id = c.course_id
        JOIN `User` u ON c.teacher_id = u.user_id
        WHERE s.classroom_id=%s AND s.weekday=%s
        ''',
        (classroom_id, weekday),
    )
    return [
        row for row in cur.fetchall()
        if period_overlap(start_period, end_period, row['start_period'], row['end_period'])
    ]


# ── Auth ──────────────────────────────────────────────────────────────────────

@app.post('/api/auth/login')
def login():
    body = request.get_json(silent=True) or {}
    user_id = body.get('user_id', '').strip()
    password = body.get('password', '')
    if not user_id or not password:
        return fail('请输入账号和密码')

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(
                'SELECT user_id, name, role, status FROM `User` WHERE user_id=%s AND password=%s',
                (user_id, password),
            )
            user = cur.fetchone()
        if not user:
            return fail('账号或密码错误')
        if user['status'] != 'ACTIVE':
            return fail('账号已禁用')
        token = jwt.encode(
            {
                'user_id': user['user_id'],
                'name': user['name'],
                'role': user['role'],
                'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS),
            },
            JWT_SECRET,
            algorithm='HS256',
        )
        return ok({'token': token, 'user': user})
    finally:
        conn.close()


@app.get('/api/auth/me')
@login_required
def me():
    return ok({'user_id': g.user['user_id'], 'name': g.user['name'], 'role': g.user['role']})


@app.post('/api/auth/logout')
def logout():
    return ok()


# ── Classrooms ────────────────────────────────────────────────────────────────

def fetch_classroom_devices(cur, classroom_id):
    cur.execute(
        '''
        SELECT d.device_id, d.device_name, d.device_type, cd.quantity
        FROM Classroom_Device cd
        JOIN Device d ON cd.device_id = d.device_id
        WHERE cd.classroom_id = %s
        ''',
        (classroom_id,),
    )
    return cur.fetchall()


@app.get('/api/classrooms')
@login_required
def list_classrooms():
    building = request.args.get('building', '').strip()
    room_number = request.args.get('room_number', '').strip()
    capacity_min = request.args.get('capacity_min', type=int)
    floor = request.args.get('floor', type=int)
    status = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    sql = 'SELECT * FROM Classroom WHERE 1=1'
    params = []
    if building:
        sql += ' AND building LIKE %s'
        params.append(f'%{building}%')
    if room_number:
        sql += ' AND room_number LIKE %s'
        params.append(f'%{room_number}%')
    if capacity_min:
        sql += ' AND capacity >= %s'
        params.append(capacity_min)
    if floor is not None:
        sql += ' AND floor = %s'
        params.append(floor)
    if status:
        sql += ' AND status = %s'
        params.append(status)
    sql += ' ORDER BY classroom_id'

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            for row in rows:
                row['devices'] = fetch_classroom_devices(cur, row['classroom_id'])
        items, total = paginate(rows, page, page_size)
        return ok({'items': items, 'total': total, 'page': page, 'page_size': page_size})
    finally:
        conn.close()


@app.get('/api/classrooms/available')
@login_required
def available_classrooms():
    date_str = request.args.get('date', '')
    start_period = request.args.get('start_period', type=int)
    end_period = request.args.get('end_period', type=int)
    capacity_min = request.args.get('capacity_min', type=int)
    building = request.args.get('building', '').strip()

    if not date_str or not start_period or not end_period:
        return fail('请提供日期和节次')
    if start_period > end_period:
        return fail('节次范围不合法')

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            sql = "SELECT * FROM Classroom WHERE status = 'AVAILABLE'"
            params = []
            if capacity_min:
                sql += ' AND capacity >= %s'
                params.append(capacity_min)
            if building:
                sql += ' AND building LIKE %s'
                params.append(f'%{building}%')
            cur.execute(sql, params)
            classrooms = cur.fetchall()

            available = []
            for c in classrooms:
                cid = c['classroom_id']
                if find_reservation_conflicts(cur, cid, date_str, start_period, end_period):
                    continue

                if find_schedule_conflicts(cur, cid, date_str, start_period, end_period):
                    continue

                c['devices'] = fetch_classroom_devices(cur, cid)
                available.append(c)

        return ok({'items': available, 'total': len(available)})
    finally:
        conn.close()


@app.get('/api/classrooms/<int:classroom_id>')
@login_required
def get_classroom(classroom_id):
    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT * FROM Classroom WHERE classroom_id=%s', (classroom_id,))
            row = cur.fetchone()
            if not row:
                return fail('教室不存在', status=404)
            row['devices'] = fetch_classroom_devices(cur, classroom_id)
        return ok(row)
    finally:
        conn.close()


@app.post('/api/classrooms')
@admin_required
def create_classroom():
    body = request.get_json(silent=True) or {}
    building = body.get('building', '').strip()
    room_number = body.get('room_number', '').strip()
    capacity = body.get('capacity')
    floor = body.get('floor')
    status = body.get('status', 'AVAILABLE')

    if not building or not room_number or not capacity or floor is None:
        return fail('请填写完整信息')
    if capacity <= 0 or floor < 0:
        return fail('容量或楼层不合法')

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO Classroom (building, room_number, capacity, floor, status) VALUES (%s,%s,%s,%s,%s)',
                (building, room_number, capacity, floor, status),
            )
            new_id = cur.lastrowid
        return ok({'classroom_id': new_id}, '创建成功')
    except Exception as e:
        if 'uk_classroom_building_room' in str(e):
            return fail('该楼宇下房间号已存在')
        return fail(str(e))
    finally:
        conn.close()


@app.put('/api/classrooms/<int:classroom_id>')
@admin_required
def update_classroom(classroom_id):
    body = request.get_json(silent=True) or {}
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT classroom_id FROM Classroom WHERE classroom_id=%s', (classroom_id,))
            if not cur.fetchone():
                return fail('教室不存在', status=404)
            fields, params = [], []
            for key in ('building', 'room_number', 'capacity', 'floor', 'status'):
                if key in body:
                    fields.append(f'{key}=%s')
                    params.append(body[key])
            if not fields:
                return fail('无更新内容')
            params.append(classroom_id)
            cur.execute(f"UPDATE Classroom SET {', '.join(fields)} WHERE classroom_id=%s", params)
        return ok(message='更新成功')
    except Exception as e:
        if 'uk_classroom_building_room' in str(e):
            return fail('该楼宇下房间号已存在')
        return fail(str(e))
    finally:
        conn.close()


@app.delete('/api/classrooms/<int:classroom_id>')
@admin_required
def delete_classroom(classroom_id):
    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT COUNT(*) AS cnt FROM Schedule WHERE classroom_id=%s', (classroom_id,))
            if cur.fetchone()['cnt']:
                return fail('该教室有关联排课，无法删除')
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM Reservation WHERE classroom_id=%s AND status IN ('PENDING','APPROVED')",
                (classroom_id,),
            )
            if cur.fetchone()['cnt']:
                return fail('该教室有进行中的预约，无法删除')
            cur.execute('DELETE FROM Classroom WHERE classroom_id=%s', (classroom_id,))
            if cur.rowcount == 0:
                return fail('教室不存在', status=404)
        return ok(message='删除成功')
    finally:
        conn.close()


# ── Courses ───────────────────────────────────────────────────────────────────

@app.get('/api/courses')
@login_required
def list_courses():
    course_name = request.args.get('course_name', '').strip()
    teacher_id = request.args.get('teacher_id', '').strip()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    sql = '''
        SELECT c.course_id, c.course_name, c.teacher_id, u.name AS teacher_name
        FROM Course c JOIN `User` u ON c.teacher_id = u.user_id WHERE 1=1
    '''
    params = []
    if course_name:
        sql += ' AND c.course_name LIKE %s'
        params.append(f'%{course_name}%')
    if teacher_id:
        sql += ' AND c.teacher_id = %s'
        params.append(teacher_id)
    sql += ' ORDER BY c.course_id'

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        items, total = paginate(rows, page, page_size)
        return ok({'items': items, 'total': total, 'page': page, 'page_size': page_size})
    finally:
        conn.close()


@app.post('/api/courses')
@admin_required
def create_course():
    body = request.get_json(silent=True) or {}
    course_name = body.get('course_name', '').strip()
    teacher_id = body.get('teacher_id', '').strip()
    if not course_name or not teacher_id:
        return fail('请填写课程名称和教师')

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM `User` WHERE user_id=%s AND role='TEACHER'", (teacher_id,))
            if not cur.fetchone():
                return fail('教师不存在')
            cur.execute('INSERT INTO Course (course_name, teacher_id) VALUES (%s,%s)', (course_name, teacher_id))
            new_id = cur.lastrowid
        return ok({'course_id': new_id}, '创建成功')
    finally:
        conn.close()


@app.put('/api/courses/<int:course_id>')
@admin_required
def update_course(course_id):
    body = request.get_json(silent=True) or {}
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT course_id FROM Course WHERE course_id=%s', (course_id,))
            if not cur.fetchone():
                return fail('课程不存在', status=404)
            fields, params = [], []
            if 'course_name' in body:
                fields.append('course_name=%s')
                params.append(body['course_name'])
            if 'teacher_id' in body:
                cur.execute("SELECT user_id FROM `User` WHERE user_id=%s AND role='TEACHER'", (body['teacher_id'],))
                if not cur.fetchone():
                    return fail('教师不存在')
                fields.append('teacher_id=%s')
                params.append(body['teacher_id'])
            if not fields:
                return fail('无更新内容')
            params.append(course_id)
            cur.execute(f"UPDATE Course SET {', '.join(fields)} WHERE course_id=%s", params)
        return ok(message='更新成功')
    finally:
        conn.close()


@app.delete('/api/courses/<int:course_id>')
@admin_required
def delete_course(course_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM Course WHERE course_id=%s', (course_id,))
            if cur.rowcount == 0:
                return fail('课程不存在', status=404)
        return ok(message='删除成功')
    finally:
        conn.close()


# ── Schedules ─────────────────────────────────────────────────────────────────

@app.get('/api/schedules')
@login_required
def list_schedules():
    course_id = request.args.get('course_id', type=int)
    teacher_id = request.args.get('teacher_id', '').strip()
    classroom_id = request.args.get('classroom_id', type=int)
    weekday = request.args.get('weekday', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    sql = '''
        SELECT s.*, c.course_name, u.name AS teacher_name,
               cl.building, cl.room_number
        FROM Schedule s
        JOIN Course c ON s.course_id = c.course_id
        JOIN `User` u ON c.teacher_id = u.user_id
        JOIN Classroom cl ON s.classroom_id = cl.classroom_id
        WHERE 1=1
    '''
    params = []
    if course_id:
        sql += ' AND s.course_id = %s'
        params.append(course_id)
    if teacher_id:
        sql += ' AND c.teacher_id = %s'
        params.append(teacher_id)
    if classroom_id:
        sql += ' AND s.classroom_id = %s'
        params.append(classroom_id)
    if weekday:
        sql += ' AND s.weekday = %s'
        params.append(weekday)
    sql += ' ORDER BY s.schedule_id'

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
        items, total = paginate(rows, page, page_size)
        return ok({'items': items, 'total': total, 'page': page, 'page_size': page_size})
    finally:
        conn.close()


@app.post('/api/schedules')
@admin_required
def create_schedule():
    body = request.get_json(silent=True) or {}
    required = ['course_id', 'classroom_id', 'weekday', 'start_period', 'end_period', 'start_week', 'end_week']
    if any(body.get(k) is None for k in required):
        return fail('请填写完整排课信息')
    if body['start_period'] > body['end_period'] or body['start_week'] > body['end_week']:
        return fail('节次或周次范围不合法')

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                '''INSERT INTO Schedule
                   (course_id, classroom_id, weekday, start_period, end_period, start_week, end_week)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                (
                    body['course_id'], body['classroom_id'], body['weekday'],
                    body['start_period'], body['end_period'], body['start_week'], body['end_week'],
                ),
            )
            new_id = cur.lastrowid
        return ok({'schedule_id': new_id}, '创建成功')
    finally:
        conn.close()


@app.put('/api/schedules/<int:schedule_id>')
@admin_required
def update_schedule(schedule_id):
    body = request.get_json(silent=True) or {}
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT schedule_id FROM Schedule WHERE schedule_id=%s', (schedule_id,))
            if not cur.fetchone():
                return fail('排课不存在', status=404)
            fields, params = [], []
            for key in ('course_id', 'classroom_id', 'weekday', 'start_period', 'end_period', 'start_week', 'end_week'):
                if key in body:
                    fields.append(f'{key}=%s')
                    params.append(body[key])
            if not fields:
                return fail('无更新内容')
            params.append(schedule_id)
            cur.execute(f"UPDATE Schedule SET {', '.join(fields)} WHERE schedule_id=%s", params)
        return ok(message='更新成功')
    finally:
        conn.close()


@app.delete('/api/schedules/<int:schedule_id>')
@admin_required
def delete_schedule(schedule_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM Schedule WHERE schedule_id=%s', (schedule_id,))
            if cur.rowcount == 0:
                return fail('排课不存在', status=404)
        return ok(message='删除成功')
    finally:
        conn.close()


# ── Reservations ──────────────────────────────────────────────────────────────

def fetch_reservations(cur, where_sql, params):
    cur.execute(
        f'''
        SELECT r.*, u.name AS user_name, cl.building, cl.room_number,
               (SELECT audit_comment FROM Reservation_Audit ra
                WHERE ra.reservation_id = r.reservation_id
                ORDER BY ra.audit_time DESC LIMIT 1) AS audit_comment
        FROM Reservation r
        JOIN `User` u ON r.user_id = u.user_id
        JOIN Classroom cl ON r.classroom_id = cl.classroom_id
        WHERE {where_sql}
        ORDER BY r.apply_time DESC
        ''',
        params,
    )
    return cur.fetchall()


@app.get('/api/reservations')
@login_required
def list_reservations():
    status = request.args.get('status', '').strip()
    classroom_id = request.args.get('classroom_id', type=int)
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    conditions = ['1=1']
    params = []
    if g.user['role'] != 'ADMIN':
        conditions.append('r.user_id = %s')
        params.append(g.user['user_id'])
    if status:
        conditions.append('r.status = %s')
        params.append(status)
    if classroom_id:
        conditions.append('r.classroom_id = %s')
        params.append(classroom_id)

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            rows = fetch_reservations(cur, ' AND '.join(conditions), params)
        items, total = paginate(rows, page, page_size)
        return ok({'items': items, 'total': total, 'page': page, 'page_size': page_size})
    finally:
        conn.close()


@app.get('/api/reservations/conflicts')
@login_required
def reservation_conflicts():
    classroom_id = request.args.get('classroom_id', type=int)
    reservation_date = request.args.get('reservation_date', '')
    start_period = request.args.get('start_period', type=int)
    end_period = request.args.get('end_period', type=int)

    if not all([classroom_id, reservation_date, start_period, end_period]):
        return fail('请提供教室、日期和节次')
    if start_period > end_period:
        return fail('节次范围不合法')

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT classroom_id FROM Classroom WHERE classroom_id=%s', (classroom_id,))
            if not cur.fetchone():
                return fail('教室不存在')

            reservation_rows = find_reservation_conflicts(
                cur, classroom_id, reservation_date, start_period, end_period
            )
            schedule_rows = find_schedule_conflicts(
                cur, classroom_id, reservation_date, start_period, end_period
            )
        return ok({
            'has_conflict': bool(reservation_rows or schedule_rows),
            'reservation_conflicts': reservation_rows,
            'schedule_conflicts': schedule_rows,
        })
    finally:
        conn.close()


@app.post('/api/reservations')
@login_required
def create_reservation():
    if g.user['role'] == 'ADMIN':
        return fail('管理员请使用审核功能', code=403, status=403)

    body = request.get_json(silent=True) or {}
    classroom_id = body.get('classroom_id')
    reservation_date = body.get('reservation_date', '')
    start_period = body.get('start_period')
    end_period = body.get('end_period')
    purpose = body.get('purpose', '').strip()

    if not all([classroom_id, reservation_date, start_period, end_period, purpose]):
        return fail('请填写完整预约信息')
    if start_period > end_period:
        return fail('节次范围不合法')

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute("SELECT status FROM Classroom WHERE classroom_id=%s", (classroom_id,))
            classroom = cur.fetchone()
            if not classroom:
                return fail('教室不存在')
            if classroom['status'] != 'AVAILABLE':
                return fail('教室当前不可预约')

            if find_reservation_conflicts(cur, classroom_id, reservation_date, start_period, end_period):
                return fail('该时段教室已有预约申请或已通过预约')

            if find_schedule_conflicts(cur, classroom_id, reservation_date, start_period, end_period):
                return fail('该时段教室有课程安排')

            cur.execute(
                '''INSERT INTO Reservation
                   (user_id, classroom_id, reservation_date, start_period, end_period, purpose)
                   VALUES (%s,%s,%s,%s,%s,%s)''',
                (g.user['user_id'], classroom_id, reservation_date, start_period, end_period, purpose),
            )
            new_id = cur.lastrowid
        return ok({'reservation_id': new_id}, '预约提交成功')
    except Exception as e:
        msg = str(e)
        if '该时段教室已被预约' in msg or '该时段教室有课程安排' in msg:
            return fail(msg)
        return fail('预约提交失败')
    finally:
        conn.close()


@app.put('/api/reservations/<int:reservation_id>/cancel')
@login_required
def cancel_reservation(reservation_id):
    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT * FROM Reservation WHERE reservation_id=%s', (reservation_id,))
            row = cur.fetchone()
            if not row:
                return fail('预约不存在', status=404)
            if g.user['role'] != 'ADMIN' and row['user_id'] != g.user['user_id']:
                return fail('无权限', code=403, status=403)
            if row['status'] not in ('PENDING', 'APPROVED'):
                return fail('当前状态不可取消')
            cur.execute(
                "UPDATE Reservation SET status='CANCELLED' WHERE reservation_id=%s",
                (reservation_id,),
            )
        return ok(message='已取消')
    finally:
        conn.close()


@app.post('/api/reservations/<int:reservation_id>/audit')
@admin_required
def audit_reservation(reservation_id):
    body = request.get_json(silent=True) or {}
    audit_result = body.get('audit_result', '')
    audit_comment = body.get('audit_comment', '').strip()
    if audit_result not in ('APPROVED', 'REJECTED'):
        return fail('审核结果不合法')

    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute('SELECT * FROM Reservation WHERE reservation_id=%s', (reservation_id,))
            row = cur.fetchone()
            if not row:
                return fail('预约不存在', status=404)
            if row['status'] != 'PENDING':
                return fail('该预约已审核')

            if audit_result == 'APPROVED':
                if find_reservation_conflicts(
                    cur,
                    row['classroom_id'],
                    row['reservation_date'],
                    row['start_period'],
                    row['end_period'],
                    exclude_id=reservation_id,
                ):
                    return fail('该时段教室已被其他预约占用')

                if find_schedule_conflicts(
                    cur,
                    row['classroom_id'],
                    row['reservation_date'],
                    row['start_period'],
                    row['end_period'],
                ):
                    return fail('该时段教室有课程安排')

            cur.execute(
                '''INSERT INTO Reservation_Audit
                   (reservation_id, admin_id, audit_result, audit_comment)
                   VALUES (%s,%s,%s,%s)''',
                (reservation_id, g.user['user_id'], audit_result, audit_comment or None),
            )
        return ok(message='审核完成')
    except Exception as e:
        msg = str(e)
        if '该时段教室已被预约' in msg or '该时段教室有课程安排' in msg:
            return fail(msg)
        return fail('审核失败')
    finally:
        conn.close()


# ── Helpers ───────────────────────────────────────────────────────────────────

@app.get('/api/users/teachers')
@login_required
def list_teachers():
    conn = get_connection()
    try:
        with conn.cursor(DictCursor) as cur:
            cur.execute(
                "SELECT user_id, name FROM `User` WHERE role='TEACHER' AND status='ACTIVE' ORDER BY user_id"
            )
            rows = cur.fetchall()
        return ok(rows)
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
