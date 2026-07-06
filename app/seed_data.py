import re
from pathlib import Path

from pymysql.cursors import DictCursor

from db_connect import get_connection

ROOT_DIR = Path(__file__).resolve().parents[1]

CREATE_TRIGGER_PATTERN = re.compile(
    r'CREATE TRIGGER\s+\w+.*?END\s*;',
    re.DOTALL | re.IGNORECASE,
)


def parse_sql_file(path: Path) -> list[str]:
    """Parse SQL file into statements executable via pymysql."""
    text = path.read_text(encoding='utf-8')
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        upper = stripped.upper()
        if upper.startswith('USE ') or upper.startswith('DELIMITER'):
            continue
        lines.append(line)
    text = '\n'.join(lines).replace('END//', 'END;')

    statements: list[str] = []
    pos = 0
    for match in CREATE_TRIGGER_PATTERN.finditer(text):
        before = text[pos:match.start()]
        statements.extend(stmt for stmt in _split_simple_statements(before))
        statements.append(match.group(0).strip())
        pos = match.end()
    statements.extend(stmt for stmt in _split_simple_statements(text[pos:]))
    return statements


def _split_simple_statements(text: str) -> list[str]:
    return [stmt.strip() for stmt in text.split(';') if stmt.strip()]
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
        [
            ('1688','109',3,1,'AVAILABLE'),('1102','1号楼127',3,1,'AVAILABLE'),('1443','2锅炉房',3,1,'AVAILABLE'),('1108','3号楼131-132',3,1,'AVAILABLE'),('1108','3号楼301',3,3,'AVAILABLE'),('1108','3号楼302',3,3,'AVAILABLE'),('1108','3号楼308',3,3,'AVAILABLE'),('1108','3号楼310',3,3,'AVAILABLE'),('1108','3号楼311',3,3,'AVAILABLE'),('1108','3号楼312',3,3,'AVAILABLE'),('1108','3号楼313',3,3,'AVAILABLE'),('1108','3号楼314',3,3,'AVAILABLE'),('1108','3号楼315',3,3,'AVAILABLE'),('1108','3号楼318',3,3,'AVAILABLE'),('1108','3号楼324',3,3,'AVAILABLE'),('1108','3号楼325/326',3,3,'AVAILABLE'),('1108','3号楼327/328',3,3,'AVAILABLE'),('1108','3号楼329',3,3,'AVAILABLE'),('1108','3号楼330',3,3,'AVAILABLE'),('1108','3号楼335',3,3,'AVAILABLE'),('1108','3号楼337',3,3,'AVAILABLE'),('1108','3号楼338',3,3,'AVAILABLE'),('1108','3号楼341',3,3,'AVAILABLE'),('1108','3号楼401',3,4,'AVAILABLE'),('1108','3号楼402',3,4,'AVAILABLE'),('1108','3号楼404',3,4,'AVAILABLE'),('1108','3号楼406',3,4,'AVAILABLE'),('1108','3号楼407',3,4,'AVAILABLE'),('1108','3号楼422',3,4,'AVAILABLE'),('1108','3号楼423',3,4,'AVAILABLE'),('1108','3号楼425',3,4,'AVAILABLE'),('1108','3号楼427',3,4,'AVAILABLE'),('1108','3号楼428',3,4,'AVAILABLE'),('1108','3号楼429',3,4,'AVAILABLE'),('1108','3号楼430',3,4,'AVAILABLE'),('1108','3号楼434',3,4,'AVAILABLE'),('1108','3号楼435',3,4,'AVAILABLE'),('1108','3号楼436',3,4,'AVAILABLE'),('1108','3号楼437',3,4,'AVAILABLE'),('1108','3号楼438',3,4,'AVAILABLE'),('1108','3号楼440',3,4,'AVAILABLE'),('257','4号楼140',3,1,'AVAILABLE'),('257','4号楼233',3,2,'AVAILABLE'),('257','4号楼319',3,3,'AVAILABLE'),('257','4号楼322',3,3,'AVAILABLE'),('257','4号楼332',3,3,'AVAILABLE'),('257','4号楼410',3,4,'AVAILABLE'),('257','4号楼427',3,4,'AVAILABLE'),('257','4号楼434',3,4,'AVAILABLE'),('257','4号楼438',3,4,'AVAILABLE'),('257','4号楼447',3,4,'AVAILABLE'),('257','4号楼448',3,4,'AVAILABLE'),('257','4号楼450',3,4,'AVAILABLE'),('257','4号楼503',3,5,'AVAILABLE'),('845','5号楼1005',3,10,'AVAILABLE'),('845','5号楼1011',3,10,'AVAILABLE'),('845','5号楼1023',3,10,'AVAILABLE'),('845','5号楼106',3,1,'AVAILABLE'),('845','5号楼108',3,1,'AVAILABLE'),('845','5号楼117',3,1,'AVAILABLE'),('845','5号楼204',3,2,'AVAILABLE'),('845','5号楼216',3,2,'AVAILABLE'),('845','5号楼218B',3,2,'AVAILABLE'),('845','5号楼302',3,3,'AVAILABLE'),('845','5号楼319',3,3,'AVAILABLE'),('845','5号楼322',3,3,'AVAILABLE'),('845','5号楼401',3,4,'AVAILABLE'),('845','5号楼402',3,4,'AVAILABLE'),('845','5号楼415',3,4,'AVAILABLE'),('845','5号楼417',3,4,'AVAILABLE'),('845','5号楼419',3,4,'AVAILABLE'),('845','5号楼427',3,4,'AVAILABLE'),('845','5号楼514B',3,5,'AVAILABLE'),('845','5号楼602',3,6,'AVAILABLE'),('845','5号楼603',3,6,'AVAILABLE'),('845','5号楼626',3,6,'AVAILABLE'),('845','5号楼627',3,6,'AVAILABLE'),('845','5号楼628',3,6,'AVAILABLE'),('845','5号楼802-3',3,8,'AVAILABLE'),('845','5号楼823',3,8,'AVAILABLE'),('845','5号楼901',3,9,'AVAILABLE'),('845','5号楼B122',3,1,'AVAILABLE'),('845','5号楼B123',3,1,'AVAILABLE'),('1702','6号楼601',3,6,'AVAILABLE'),('644','7号楼108',3,1,'AVAILABLE'),('644','7号楼403',3,4,'AVAILABLE'),('1807','8号楼1001',3,10,'AVAILABLE'),('1807','8号楼1003',3,10,'AVAILABLE'),('1807','8号楼1005',3,10,'AVAILABLE'),('1807','8号楼1007',3,10,'AVAILABLE'),('1807','8号楼1009',3,10,'AVAILABLE'),('1807','8号楼2001',3,20,'AVAILABLE'),('1807','8号楼2003',3,20,'AVAILABLE'),('1807','8号楼2005',3,20,'AVAILABLE'),('1807','8号楼2007',3,20,'AVAILABLE'),('1807','8号楼2009',3,20,'AVAILABLE'),('1807','8号楼3001',3,30,'AVAILABLE'),('1807','8号楼3003',3,30,'AVAILABLE'),('1807','8号楼3005',3,30,'AVAILABLE'),('1807','8号楼3007',3,30,'AVAILABLE'),
            ('1807','8号楼3009',3,30,'AVAILABLE'),('1807','8号楼3019',3,30,'AVAILABLE'),('1807','8号楼4001',3,40,'AVAILABLE'),('1807','8号楼4003',3,40,'AVAILABLE'),('1807','8号楼4005',3,40,'AVAILABLE'),('1807','8号楼4007',3,40,'AVAILABLE'),('1807','8号楼4009',3,40,'AVAILABLE'),('1807','8号楼4014',3,40,'AVAILABLE'),('1807','8号楼4018',3,40,'AVAILABLE'),('1807','8号楼4023',3,40,'AVAILABLE'),('1807','8号楼5001',3,50,'AVAILABLE'),('1807','8号楼5003',3,50,'AVAILABLE'),('1807','8号楼5005',3,50,'AVAILABLE'),('1807','8号楼5007',3,50,'AVAILABLE'),('1807','8号楼5009',3,50,'AVAILABLE'),('1807','8号楼6001',3,60,'AVAILABLE'),('1807','8号楼6003',3,60,'AVAILABLE'),('1807','8号楼6005',3,60,'AVAILABLE'),('280H','HA505',3,5,'AVAILABLE'),('280H','HC402',3,4,'AVAILABLE'),('280H','HD105',3,1,'AVAILABLE'),('280H','HD106',3,1,'AVAILABLE'),('280H','HE105',3,1,'AVAILABLE'),('280H','HE106',3,1,'AVAILABLE'),('280H','HF101',3,1,'AVAILABLE'),('280H','HF103',3,1,'AVAILABLE'),('280H','HF107',3,1,'AVAILABLE'),('280H','HF108',3,1,'AVAILABLE'),('280H','HF201',3,2,'AVAILABLE'),('280H','HF202',3,2,'AVAILABLE'),('280H','HF203',3,2,'AVAILABLE'),('280H','HF204',3,2,'AVAILABLE'),('280H','HF205',3,2,'AVAILABLE'),('280H','HF207',3,2,'AVAILABLE'),('280H','HF208',3,2,'AVAILABLE'),('280H','HF301',3,3,'AVAILABLE'),('280H','HF302',3,3,'AVAILABLE'),('280H','HF303',3,3,'AVAILABLE'),('280H','HF304',3,3,'AVAILABLE'),('280H','HF305',3,3,'AVAILABLE'),('280H','HF306',3,3,'AVAILABLE'),('280H','HF307',3,3,'AVAILABLE'),('280H','HF308',3,3,'AVAILABLE'),('280H','HG301',3,3,'AVAILABLE'),('280H','HG302',3,3,'AVAILABLE'),('280H','HG303',3,3,'AVAILABLE'),('280H','HG304',3,3,'AVAILABLE'),('280H','HG305',3,3,'AVAILABLE'),('280H','HH101',3,1,'AVAILABLE'),('280H','HH102',3,1,'AVAILABLE'),('280H','HH107',3,1,'AVAILABLE'),('280H','HH108',3,1,'AVAILABLE'),('280H','HH201',3,2,'AVAILABLE'),('280H','HH202',3,2,'AVAILABLE'),('280H','HH203',3,2,'AVAILABLE'),('280H','HH204',3,2,'AVAILABLE'),('280H','HH205',3,2,'AVAILABLE'),('280H','HH207',3,2,'AVAILABLE'),('280H','HH208',3,2,'AVAILABLE'),('280H','HH209',3,2,'AVAILABLE'),('280H','HH301',3,3,'AVAILABLE'),('280H','HH302',3,3,'AVAILABLE'),('280H','HH303',3,3,'AVAILABLE'),('280H','HH304',3,3,'AVAILABLE'),('280H','HH305',3,3,'AVAILABLE'),('280H','HH306',3,3,'AVAILABLE'),('280H','HH307',3,3,'AVAILABLE'),('280H','HH308',3,3,'AVAILABLE'),('280H','HH310',3,3,'AVAILABLE'),('280H','HH311',3,3,'AVAILABLE'),('280H','HH312',3,3,'AVAILABLE'),('280J','JB212',3,2,'AVAILABLE'),('280M','MB104',3,1,'AVAILABLE'),('280M','MC504',3,5,'AVAILABLE'),('280Q','QC317',3,3,'AVAILABLE'),('750','北校区篮球场',3,1,'AVAILABLE'),('2928','本研同考场',3,1,'AVAILABLE'),('845','玻璃工房（5号楼东南侧）',3,1,'AVAILABLE'),('1112','搏击综合教室（体育部游泳池一层）',3,1,'AVAILABLE'),('1682','车辆实验楼106',3,1,'AVAILABLE'),('1682','车辆实验楼301',3,3,'AVAILABLE'),('2914','丹枫C225',3,2,'AVAILABLE'),('2914','丹枫C325',3,3,'AVAILABLE'),('2914','丹枫C425',3,4,'AVAILABLE'),('2914','丹枫C525',3,5,'AVAILABLE'),('2914','丹枫C625',3,6,'AVAILABLE'),('2914','丹枫C725',3,7,'AVAILABLE'),('2914','丹枫C825',3,8,'AVAILABLE'),('1680','东105',3,1,'AVAILABLE'),('1680','东106',3,1,'AVAILABLE'),('1112','东篮球场',3,1,'AVAILABLE'),('1112','东排球场',3,1,'AVAILABLE'),('2650','工程训练中心',3,1,'AVAILABLE'),('2650','工训楼',3,1,'AVAILABLE'),('2650','工训楼1003',3,10,'AVAILABLE'),('2650','工训楼1004',3,10,'AVAILABLE'),('2650','工训楼1005',3,10,'AVAILABLE'),('2650','工训楼1010',3,10,'AVAILABLE'),('2650','工训楼1011',3,10,'AVAILABLE'),('2650','工训楼1015',3,10,'AVAILABLE'),
            ('2650','工训楼102',3,1,'AVAILABLE'),('2650','工训楼104',3,1,'AVAILABLE'),('2650','工训楼105',3,1,'AVAILABLE'),('2650','工训楼106',3,1,'AVAILABLE'),('2650','工训楼107',3,1,'AVAILABLE'),('2650','工训楼108',3,1,'AVAILABLE'),('2650','工训楼113',3,1,'AVAILABLE'),('2650','工训楼209',3,2,'AVAILABLE'),('2650','工训楼301',3,3,'AVAILABLE'),('2650','工训楼302A',3,3,'AVAILABLE'),('2650','工训楼306',3,3,'AVAILABLE'),('2650','工训楼307',3,3,'AVAILABLE'),('2650','工训楼309',3,3,'AVAILABLE'),('2650','工训楼312',3,3,'AVAILABLE'),('2650','工训楼313',3,3,'AVAILABLE'),('2650','工训楼315',3,3,'AVAILABLE'),('2650','工训楼402',3,4,'AVAILABLE'),('2650','工训楼403',3,4,'AVAILABLE'),('2650','工训楼404',3,4,'AVAILABLE'),('2650','工训楼406',3,4,'AVAILABLE'),('2650','工训楼411',3,4,'AVAILABLE'),('2650','工训楼412',3,4,'AVAILABLE'),('2650','工训楼502',3,5,'AVAILABLE'),('2650','工训楼503',3,5,'AVAILABLE'),('2650','工训楼505',3,5,'AVAILABLE'),('2650','工训楼506',3,5,'AVAILABLE'),('2650','工训楼507',3,5,'AVAILABLE'),('2650','工训楼508',3,5,'AVAILABLE'),('2650','工训楼509',3,5,'AVAILABLE'),('2650','工训楼602',3,6,'AVAILABLE'),('2650','工训楼603',3,6,'AVAILABLE'),('2650','工训楼604',3,6,'AVAILABLE'),('2650','工训楼606',3,6,'AVAILABLE'),('2650','工训楼607',3,6,'AVAILABLE'),('2650','工训楼608',3,6,'AVAILABLE'),('2650','工训楼610',3,6,'AVAILABLE'),('2650','工训楼802',3,8,'AVAILABLE'),('2650','工训楼804',3,8,'AVAILABLE'),('2650','工训楼805',3,8,'AVAILABLE'),('2650','工训楼811',3,8,'AVAILABLE'),('2650','工训楼902',3,9,'AVAILABLE'),('2650','工训楼903',3,9,'AVAILABLE'),('2650','工训楼904',3,9,'AVAILABLE'),('2650','工训楼905',3,9,'AVAILABLE'),('2650','工训楼908',3,9,'AVAILABLE'),('2650','工训楼909',3,9,'AVAILABLE'),('2650','工训楼910',3,9,'AVAILABLE'),('2650','工训楼911',3,9,'AVAILABLE'),('2650','工训楼913',3,9,'AVAILABLE'),('2650','工训楼915',3,9,'AVAILABLE'),('2650','工训楼配楼114',3,1,'AVAILABLE'),('2650','工训楼配楼314',3,3,'AVAILABLE'),('810','工业生态楼电镜112',3,1,'AVAILABLE'),('810','工业生态楼分析测试中心',3,1,'AVAILABLE'),('810','工业生态楼化工基础201',3,2,'AVAILABLE'),('810','工业生态楼精细301',3,3,'AVAILABLE'),('810','工业生态楼科研实验室',3,1,'AVAILABLE'),('810','工业生态楼能源303',3,3,'AVAILABLE'),('810','工业生态楼色谱质谱实验室',3,1,'AVAILABLE'),('810','工业生态楼生化302',3,3,'AVAILABLE'),('810','工业生态楼仪器分析202',3,2,'AVAILABLE'),('810','工业生态楼制药310',3,3,'AVAILABLE'),('806','化学实验楼508',3,5,'AVAILABLE'),('806','化学实验楼大化实验室',3,1,'AVAILABLE'),('806','化学实验中心100',3,1,'AVAILABLE'),('806','化学实验中心104',3,1,'AVAILABLE'),('806','化学实验中心105',3,1,'AVAILABLE'),('806','化学实验中心115',3,1,'AVAILABLE'),('806','化学实验中心216',3,2,'AVAILABLE'),('806','化学实验中心218',3,2,'AVAILABLE'),('806','化学实验中心219',3,2,'AVAILABLE'),('806','化学实验中心220',3,2,'AVAILABLE'),('806','化学实验中心222',3,2,'AVAILABLE'),('806','化学实验中心312',3,3,'AVAILABLE'),('806','化学实验中心317',3,3,'AVAILABLE'),('806','化学实验中心402',3,4,'AVAILABLE'),('806','化学实验中心405',3,4,'AVAILABLE'),('806','化学实验中心407',3,4,'AVAILABLE'),('806','化学实验中心429',3,4,'AVAILABLE'),('806','化学实验中心509',3,5,'AVAILABLE'),('806','化学实验中心分析122',3,1,'AVAILABLE'),('806','化学实验中心分析124',3,1,'AVAILABLE'),('806','化学实验中心分析505',3,5,'AVAILABLE'),('806','化学实验中心化工原理117',3,1,'AVAILABLE'),('806','化学实验中心无机322',3,3,'AVAILABLE'),('806','化学实验中心无机325',3,3,'AVAILABLE'),('806','化学实验中心无机327',3,3,'AVAILABLE'),('806','化学实验中心物化215',3,2,'AVAILABLE'),('806','化学实验中心虚拟仿真110',3,1,'AVAILABLE'),('806','化学实验中心仪器分析114',3,1,'AVAILABLE'),('806','化学实验中心有机412',3,4,'AVAILABLE'),('806','化学实验中心有机413',3,4,'AVAILABLE'),('806','化学实验中心有机414',3,4,'AVAILABLE'),('1112','健美操教室',3,1,'AVAILABLE'),('1112','篮球训练场',3,1,'AVAILABLE'),('2998','理教楼101',3,1,'AVAILABLE'),('2998','理教楼102',3,1,'AVAILABLE'),('2998','理教楼103',3,1,'AVAILABLE'),('2998','理教楼104',3,1,'AVAILABLE'),('2998','理教楼105',3,1,'AVAILABLE'),
            ('2998','理教楼106',3,1,'AVAILABLE'),('2998','理教楼107',3,1,'AVAILABLE'),('2998','理教楼108',3,1,'AVAILABLE'),('2998','理教楼109',3,1,'AVAILABLE'),('2998','理教楼201',3,2,'AVAILABLE'),('2998','理教楼202',3,2,'AVAILABLE'),('2998','理教楼203',3,2,'AVAILABLE'),('2998','理教楼204',3,2,'AVAILABLE'),('2998','理教楼205',3,2,'AVAILABLE'),('2998','理教楼206',3,2,'AVAILABLE'),('2998','理教楼207',3,2,'AVAILABLE'),('2998','理教楼208',3,2,'AVAILABLE'),('2998','理教楼209',3,2,'AVAILABLE'),('2998','理教楼210',3,2,'AVAILABLE'),('2998','理教楼301',3,3,'AVAILABLE'),('2998','理教楼302',3,3,'AVAILABLE'),('2998','理教楼303',3,3,'AVAILABLE'),('2998','理教楼304',3,3,'AVAILABLE'),('2998','理教楼305',3,3,'AVAILABLE'),('2998','理教楼306',3,3,'AVAILABLE'),('2998','理教楼307',3,3,'AVAILABLE'),('2998','理教楼308',3,3,'AVAILABLE'),('2998','理教楼309',3,3,'AVAILABLE'),('2998','理教楼310',3,3,'AVAILABLE'),('2998','理教楼401',3,4,'AVAILABLE'),('2998','理教楼402',3,4,'AVAILABLE'),('2998','理教楼403',3,4,'AVAILABLE'),('2998','理教楼404',3,4,'AVAILABLE'),('2998','理教楼405',3,4,'AVAILABLE'),('2998','理教楼406',3,4,'AVAILABLE'),('2998','理教楼407',3,4,'AVAILABLE'),('2998','理教楼408',3,4,'AVAILABLE'),('2998','理教楼409',3,4,'AVAILABLE'),('2998','理教楼501',3,5,'AVAILABLE'),('2998','理教楼502',3,5,'AVAILABLE'),('2998','理教楼503',3,5,'AVAILABLE'),('2998','理教楼504',3,5,'AVAILABLE'),('2998','理教楼505',3,5,'AVAILABLE'),('2998','理教楼506',3,5,'AVAILABLE'),('2803','理学B2-102',3,1,'AVAILABLE'),('2803','理学B2-106',3,1,'AVAILABLE'),('2803','理学B2-206',3,2,'AVAILABLE'),('2804','理学C1-106',3,1,'AVAILABLE'),('2804','理学C1-207',3,2,'AVAILABLE'),('2804','理学C303',3,3,'AVAILABLE'),('2804','理学C304',3,3,'AVAILABLE'),('2804','理学C305',3,3,'AVAILABLE'),('2804','理学C306',3,3,'AVAILABLE'),('2804','理学C307',3,3,'AVAILABLE'),('2804','理学C313',3,3,'AVAILABLE'),('2804','理学C314',3,3,'AVAILABLE'),('2804','理学C315',3,3,'AVAILABLE'),('2804','理学C402',3,4,'AVAILABLE'),('2804','理学C403',3,4,'AVAILABLE'),('2804','理学C404',3,4,'AVAILABLE'),('2804','理学C405',3,4,'AVAILABLE'),('2804','理学C406',3,4,'AVAILABLE'),('2804','理学C408',3,4,'AVAILABLE'),('2804','理学C409',3,4,'AVAILABLE'),('2804','理学C410',3,4,'AVAILABLE'),('750','良乡体育馆202',3,2,'AVAILABLE'),('750','良乡体育馆209',3,2,'AVAILABLE'),('750','良乡体育馆212',3,2,'AVAILABLE'),('750','良乡体育馆302',3,3,'AVAILABLE'),('750','良乡体育馆316',3,3,'AVAILABLE'),('750','良乡体育馆407',3,4,'AVAILABLE'),('750','良乡体育馆北广场',3,1,'AVAILABLE'),('750','良乡体育馆健身房',3,1,'AVAILABLE'),('750','良乡体育馆篮球场',3,1,'AVAILABLE'),('750','良乡体育馆南广场',3,1,'AVAILABLE'),('750','良乡体育馆西广场',3,1,'AVAILABLE'),('750','良乡体育馆羽毛球场',3,1,'AVAILABLE'),('901','良乡图书馆地下一层101A',3,1,'AVAILABLE'),('901','良乡图书馆地下一层102A',3,1,'AVAILABLE'),('901','良乡图书馆二号机房',3,1,'AVAILABLE'),('901','良乡图书馆六号机房',3,1,'AVAILABLE'),('901','良乡图书馆三号机房',3,1,'AVAILABLE'),('901','良乡图书馆四号机房',3,1,'AVAILABLE'),('901','良乡图书馆五号机房',3,1,'AVAILABLE'),('901','良乡图书馆一号机房',3,1,'AVAILABLE'),('1112','轮滑场（体育公园）',3,1,'AVAILABLE'),('1112','轮滑场（西排球场）',3,1,'AVAILABLE'),('750','南校区篮球场',3,1,'AVAILABLE'),('750','南校区排球场',3,1,'AVAILABLE'),('750','南校区网球场',3,1,'AVAILABLE'),('750','南校区足球场',3,1,'AVAILABLE'),('809','排练厅D11',3,1,'AVAILABLE'),('809','排练厅D13',3,1,'AVAILABLE'),('1112','排球场',3,1,'AVAILABLE'),('1112','乒乓球场（乒羽中心）',3,1,'AVAILABLE'),('1112','乒乓球场（艺悦楼一层）',3,1,'AVAILABLE'),('810','生态楼118',3,1,'AVAILABLE'),('845','实验室',3,1,'AVAILABLE'),('1112','手球场（田径场）',3,1,'AVAILABLE'),('750','疏桐园A地下',3,1,'AVAILABLE'),('1112','塑身瑜伽教室（体育部游泳池一层）',3,1,'AVAILABLE'),('1112','体育场看台下',3,1,'AVAILABLE'),('1112','体育多媒体教室',3,1,'AVAILABLE'),('1112','体育公园篮球场',3,1,'AVAILABLE'),('1112','体育公园网球场',3,1,'AVAILABLE'),
            ('809','体育馆夹层J13',3,1,'AVAILABLE'),('809','体育馆乐团排练厅',3,1,'AVAILABLE'),('1112','体育教室A（学生宿舍21栋）',3,1,'AVAILABLE'),('1112','体育教室B（学生宿舍22栋）',3,1,'AVAILABLE'),('1112','体育教室C（学生宿舍23栋）',3,1,'AVAILABLE'),('1112','体育舞蹈教室',3,1,'AVAILABLE'),('1112','天然草足球场（弘毅楼旁）',3,1,'AVAILABLE'),('1112','田径场',3,1,'AVAILABLE'),('750','田径场主席台',3,1,'AVAILABLE'),('750','图书馆地下101A',3,1,'AVAILABLE'),('750','图书馆地下102A',3,1,'AVAILABLE'),('901','图书馆音乐厅',3,1,'AVAILABLE'),('1112','拓展基地',3,1,'AVAILABLE'),('1112','网球场',3,1,'AVAILABLE'),('wbzx','文博中心大剧院',3,1,'AVAILABLE'),('1112','文体馆112-健身中心',3,1,'AVAILABLE'),('1112','文体中心教室1',3,1,'AVAILABLE'),('1112','文体中心教室2',3,1,'AVAILABLE'),('1112','文体中心教室3',3,1,'AVAILABLE'),('1112','文体中心教室5',3,1,'AVAILABLE'),('1112','文体中心教室6',3,1,'AVAILABLE'),('1112','文体中心教室7',3,1,'AVAILABLE'),('1112','文体中心教室8',3,1,'AVAILABLE'),('1112','文体中心乒乓球室',3,1,'AVAILABLE'),('1112','文体中心体育教室A',3,1,'AVAILABLE'),('1112','文体中心体育教室B',3,1,'AVAILABLE'),('1112','文体综合馆',3,1,'AVAILABLE'),('2701-2','文萃楼B129',3,1,'AVAILABLE'),('2701-2','文萃楼B130',3,1,'AVAILABLE'),('2701-2','文萃楼B139',3,1,'AVAILABLE'),('2701-2','文萃楼B140',3,1,'AVAILABLE'),('2701-2','文萃楼B221',3,2,'AVAILABLE'),('2701-2','文萃楼B222',3,2,'AVAILABLE'),('2701-2','文萃楼B223',3,2,'AVAILABLE'),('2701-2','文萃楼B224',3,2,'AVAILABLE'),('2701-2','文萃楼B227',3,2,'AVAILABLE'),('2701-2','文萃楼B228',3,2,'AVAILABLE'),('2701-2','文萃楼B233',3,2,'AVAILABLE'),('2701-3','文萃楼C501a',3,5,'AVAILABLE'),('2701-3','文萃楼C501b',3,5,'AVAILABLE'),('2701-3','文萃楼C501c',3,5,'AVAILABLE'),('2701-3','文萃楼C501d',3,5,'AVAILABLE'),('2701-3','文萃楼C505',3,5,'AVAILABLE'),('2701-3','文萃楼C506',3,5,'AVAILABLE'),('2701-3','文萃楼C605',3,6,'AVAILABLE'),('2701-3','文萃楼C703',3,7,'AVAILABLE'),('2701-3','文萃楼C705',3,7,'AVAILABLE'),('2701-3','文萃楼C803',3,8,'AVAILABLE'),('2701-3','文萃楼C805',3,8,'AVAILABLE'),('2701-3','文萃楼C806',3,8,'AVAILABLE'),('2701-3','文萃楼C903',3,9,'AVAILABLE'),('2701-3','文萃楼C905',3,9,'AVAILABLE'),('2701-5','文萃楼E207',3,2,'AVAILABLE'),('2701-5','文萃楼E218',3,2,'AVAILABLE'),('2701-6','文萃楼F101',3,1,'AVAILABLE'),('2701-6','文萃楼F102',3,1,'AVAILABLE'),('2701-6','文萃楼F103',3,1,'AVAILABLE'),('2701-6','文萃楼F201',3,2,'AVAILABLE'),('2701-6','文萃楼F202',3,2,'AVAILABLE'),('2701-6','文萃楼F203',3,2,'AVAILABLE'),('2701-6','文萃楼F204',3,2,'AVAILABLE'),('2701-6','文萃楼F205',3,2,'AVAILABLE'),('2701-6','文萃楼F301',3,3,'AVAILABLE'),('2701-6','文萃楼F302',3,3,'AVAILABLE'),('2701-6','文萃楼F303',3,3,'AVAILABLE'),('2701-6','文萃楼F304',3,3,'AVAILABLE'),('2701-6','文萃楼F305',3,3,'AVAILABLE'),('2701-6','文萃楼F401',3,4,'AVAILABLE'),('2701-6','文萃楼F402',3,4,'AVAILABLE'),('2701-6','文萃楼F403',3,4,'AVAILABLE'),('2701-6','文萃楼F404',3,4,'AVAILABLE'),('2701-6','文萃楼F405',3,4,'AVAILABLE'),('2701-6','文萃楼F501',3,5,'AVAILABLE'),('2701-6','文萃楼F502',3,5,'AVAILABLE'),('2701-6','文萃楼F503',3,5,'AVAILABLE'),('2701-6','文萃楼F504',3,5,'AVAILABLE'),('2701-6','文萃楼F505',3,5,'AVAILABLE'),('2701-6','文萃楼F601',3,6,'AVAILABLE'),('2701-6','文萃楼F602',3,6,'AVAILABLE'),('2701-6','文萃楼F603',3,6,'AVAILABLE'),('2701-6','文萃楼F604',3,6,'AVAILABLE'),('2701-6','文萃楼F605',3,6,'AVAILABLE'),('2701-6','文萃楼F701',3,7,'AVAILABLE'),('2701-6','文萃楼F702',3,7,'AVAILABLE'),('2701-6','文萃楼F703',3,7,'AVAILABLE'),('2701-6','文萃楼F704',3,7,'AVAILABLE'),('2701-6','文萃楼F705',3,7,'AVAILABLE'),('2701-7','文萃楼G124',3,1,'AVAILABLE'),('2701-7','文萃楼G125',3,1,'AVAILABLE'),('2701-7','文萃楼G126',3,1,'AVAILABLE'),('2701-7','文萃楼G130',3,1,'AVAILABLE'),('2701-7','文萃楼G221',3,2,'AVAILABLE'),('2701-7','文萃楼G222',3,2,'AVAILABLE'),('2701-7','文萃楼G223',3,2,'AVAILABLE'),('2701-7','文萃楼G224',3,2,'AVAILABLE'),('2701-7','文萃楼G227',3,2,'AVAILABLE'),('2701-8','文萃楼H124良乡一号机房',3,1,'AVAILABLE'),('2701-8','文萃楼H125良乡二号机房',3,1,'AVAILABLE'),('2701-8','文萃楼H126良乡三号机房',3,1,'AVAILABLE'),('2701-8','文萃楼H130',3,1,'AVAILABLE'),
            ('2701-8','文萃楼H221良乡四号机房',3,2,'AVAILABLE'),('2701-8','文萃楼H222良乡五号机房',3,2,'AVAILABLE'),('2701-8','文萃楼H226良乡六号机房',3,2,'AVAILABLE'),('2701-8','文萃楼H229良乡七号机房',3,2,'AVAILABLE'),('2701-9','文萃楼I101',3,1,'AVAILABLE'),('2701-9','文萃楼I102',3,1,'AVAILABLE'),('2701-9','文萃楼I103',3,1,'AVAILABLE'),('2701-9','文萃楼I201',3,2,'AVAILABLE'),('2701-9','文萃楼I202',3,2,'AVAILABLE'),('2701-9','文萃楼I203',3,2,'AVAILABLE'),('2701-9','文萃楼I204',3,2,'AVAILABLE'),('2701-9','文萃楼I205',3,2,'AVAILABLE'),('2701-9','文萃楼I301',3,3,'AVAILABLE'),('2701-9','文萃楼I302',3,3,'AVAILABLE'),('2701-9','文萃楼I303',3,3,'AVAILABLE'),('2701-9','文萃楼I304',3,3,'AVAILABLE'),('2701-9','文萃楼I305',3,3,'AVAILABLE'),('2701-9','文萃楼I401',3,4,'AVAILABLE'),('2701-9','文萃楼I402',3,4,'AVAILABLE'),('2701-9','文萃楼I403',3,4,'AVAILABLE'),('2701-9','文萃楼I404',3,4,'AVAILABLE'),('2701-9','文萃楼I405',3,4,'AVAILABLE'),('2701-9','文萃楼I501',3,5,'AVAILABLE'),('2701-9','文萃楼I502',3,5,'AVAILABLE'),('2701-9','文萃楼I503',3,5,'AVAILABLE'),('2701-9','文萃楼I504',3,5,'AVAILABLE'),('2701-9','文萃楼I505',3,5,'AVAILABLE'),('2701-9','文萃楼I601',3,6,'AVAILABLE'),('2701-9','文萃楼I602',3,6,'AVAILABLE'),('2701-9','文萃楼I603',3,6,'AVAILABLE'),('2701-9','文萃楼I604',3,6,'AVAILABLE'),('2701-9','文萃楼I605',3,6,'AVAILABLE'),('2701-9','文萃楼I701',3,7,'AVAILABLE'),('2701-9','文萃楼I702',3,7,'AVAILABLE'),('2701-9','文萃楼I703',3,7,'AVAILABLE'),('2701-9','文萃楼I704',3,7,'AVAILABLE'),('2701-9','文萃楼I705',3,7,'AVAILABLE'),('2701-10','文萃楼J909',3,9,'AVAILABLE'),('2701-10','文萃楼J911',3,9,'AVAILABLE'),('2701-10','文萃楼J916',3,9,'AVAILABLE'),('2701-12','文萃楼L106',3,1,'AVAILABLE'),('2701-12','文萃楼L614',3,6,'AVAILABLE'),('2701-12','文萃楼L812',3,8,'AVAILABLE'),('2701-13','文萃楼M124',3,1,'AVAILABLE'),('2701-13','文萃楼M125',3,1,'AVAILABLE'),('2701-13','文萃楼M134',3,1,'AVAILABLE'),('2701-13','文萃楼M135',3,1,'AVAILABLE'),('2701-13','文萃楼M221',3,2,'AVAILABLE'),('2701-13','文萃楼M222',3,2,'AVAILABLE'),('2701-13','文萃楼M223',3,2,'AVAILABLE'),('2701-13','文萃楼M224',3,2,'AVAILABLE'),('2701-13','文萃楼M227',3,2,'AVAILABLE'),('2701-13','文萃楼M228',3,2,'AVAILABLE'),('2701-13','文萃楼M233',3,2,'AVAILABLE'),('2701-14','文萃楼报告厅Y101',3,1,'AVAILABLE'),('2701-14','文萃楼报告厅Y201',3,2,'AVAILABLE'),('750','文萃楼中心广场',3,1,'AVAILABLE'),('806','无机化学化学实验室320',3,3,'AVAILABLE'),('1112','武术教室',3,1,'AVAILABLE'),('805','物理实验127',3,1,'AVAILABLE'),('805','物理实验201-202',3,2,'AVAILABLE'),('805','物理实验203-204',3,2,'AVAILABLE'),('805','物理实验205-206',3,2,'AVAILABLE'),('805','物理实验207',3,2,'AVAILABLE'),('805','物理实验208-209',3,2,'AVAILABLE'),('805','物理实验210-211',3,2,'AVAILABLE'),('805','物理实验212',3,2,'AVAILABLE'),('805','物理实验213-214',3,2,'AVAILABLE'),('805','物理实验215-216',3,2,'AVAILABLE'),('805','物理实验217-218',3,2,'AVAILABLE'),('805','物理实验219',3,2,'AVAILABLE'),('805','物理实验220',3,2,'AVAILABLE'),('805','物理实验221',3,2,'AVAILABLE'),('805','物理实验222',3,2,'AVAILABLE'),('805','物理实验223',3,2,'AVAILABLE'),('805','物理实验225-226',3,2,'AVAILABLE'),('805','物理实验227',3,2,'AVAILABLE'),('805','物理实验228',3,2,'AVAILABLE'),('805','物理实验229-230',3,2,'AVAILABLE'),('805','物理实验231-232',3,2,'AVAILABLE'),('805','物理实验233',3,2,'AVAILABLE'),('805','物理实验301',3,3,'AVAILABLE'),('805','物理实验302-303',3,3,'AVAILABLE'),('805','物理实验304-305',3,3,'AVAILABLE'),('805','物理实验306-307',3,3,'AVAILABLE'),('805','物理实验308',3,3,'AVAILABLE'),('805','物理实验309-310',3,3,'AVAILABLE'),('805','物理实验311-312',3,3,'AVAILABLE'),('805','物理实验313',3,3,'AVAILABLE'),('805','物理实验314-315',3,3,'AVAILABLE'),('805','物理实验316-317',3,3,'AVAILABLE'),('805','物理实验318-319',3,3,'AVAILABLE'),('805','物理实验320-321',3,3,'AVAILABLE'),('805','物理实验322',3,3,'AVAILABLE'),('805','物理实验323',3,3,'AVAILABLE'),('805','物理实验324-325',3,3,'AVAILABLE'),('805','物理实验326-327',3,3,'AVAILABLE'),('805','物理实验328-329',3,3,'AVAILABLE'),('805','物理实验330-331',3,3,'AVAILABLE'),('805','物理实验332',3,3,'AVAILABLE'),
            ('805','物理实验333',3,3,'AVAILABLE'),('805','物理实验401-402',3,4,'AVAILABLE'),('805','物理实验403-404',3,4,'AVAILABLE'),('805','物理实验405',3,4,'AVAILABLE'),('805','物理实验406-407',3,4,'AVAILABLE'),('805','物理实验408-409',3,4,'AVAILABLE'),('805','物理实验410',3,4,'AVAILABLE'),('805','物理实验411-412',3,4,'AVAILABLE'),('805','物理实验413-414',3,4,'AVAILABLE'),('805','物理实验415-416',3,4,'AVAILABLE'),('805','物理实验417-418',3,4,'AVAILABLE'),('805','物理实验419',3,4,'AVAILABLE'),('805','物理实验420',3,4,'AVAILABLE'),('805','物理实验421-422',3,4,'AVAILABLE'),('805','物理实验423-424',3,4,'AVAILABLE'),('805','物理实验425',3,4,'AVAILABLE'),('805','物理实验426',3,4,'AVAILABLE'),('805','物理实验501',3,5,'AVAILABLE'),('805','物理实验502',3,5,'AVAILABLE'),('805','物理实验504',3,5,'AVAILABLE'),('805','物理实验506',3,5,'AVAILABLE'),('805','物理实验508',3,5,'AVAILABLE'),('805','物理实验509',3,5,'AVAILABLE'),('805','物理实验510',3,5,'AVAILABLE'),('805','物理实验511-512',3,5,'AVAILABLE'),('805','物理实验513-514',3,5,'AVAILABLE'),('805','物理实验515-516',3,5,'AVAILABLE'),('805','物理实验517',3,5,'AVAILABLE'),('805','物理实验518',3,5,'AVAILABLE'),('805','物理实验522',3,5,'AVAILABLE'),('805','物理实验中心',3,1,'AVAILABLE'),('1679','西101',3,1,'AVAILABLE'),('1679','西102',3,1,'AVAILABLE'),('1679','西103',3,1,'AVAILABLE'),('1679','西104',3,1,'AVAILABLE'),('1112','西篮球场',3,1,'AVAILABLE'),('809','西南篮球场',3,1,'AVAILABLE'),('1112','西排球场',3,1,'AVAILABLE'),('525','西山校区北院338楼104',3,3,'AVAILABLE'),('525','西山阻燃楼',3,1,'AVAILABLE'),('1806','线上考试1',3,1,'AVAILABLE'),('280H','线上考试1（珠海）',3,1,'AVAILABLE'),('2903','线上考试2',3,1,'AVAILABLE'),('1807','线上考试3',3,1,'AVAILABLE'),('922','心理与社会工作实验室',3,1,'AVAILABLE'),('719','信息科学楼102东',3,1,'AVAILABLE'),('719','信息科学楼102西',3,1,'AVAILABLE'),('719','信息科学楼302',3,3,'AVAILABLE'),('114','信息中心110',3,1,'AVAILABLE'),('114','信息中心一层大机房',3,1,'AVAILABLE'),('1112','形体教室',3,1,'AVAILABLE'),('1112','休闲健身教室（体育部游泳池一层）',3,1,'AVAILABLE'),('927','学生服务中心211',3,2,'AVAILABLE'),('1112','学生宿舍34栋楼下架空层体育教室',3,1,'AVAILABLE'),('1112','学生宿舍35栋楼下架空层体育教室',3,1,'AVAILABLE'),('1806','研楼103',3,1,'AVAILABLE'),('1806','研楼104',3,1,'AVAILABLE'),('1806','研楼105',3,1,'AVAILABLE'),('1806','研楼106',3,1,'AVAILABLE'),('1806','研楼107',3,1,'AVAILABLE'),('1806','研楼112',3,1,'AVAILABLE'),('1806','研楼203',3,2,'AVAILABLE'),('1806','研楼204',3,2,'AVAILABLE'),('1806','研楼206',3,2,'AVAILABLE'),('1806','研楼207',3,2,'AVAILABLE'),('1806','研楼208',3,2,'AVAILABLE'),('1806','研楼209',3,2,'AVAILABLE'),('1806','研楼210',3,2,'AVAILABLE'),('1806','研楼301',3,3,'AVAILABLE'),('1806','研楼302',3,3,'AVAILABLE'),('1806','研楼303',3,3,'AVAILABLE'),('1806','研楼304',3,3,'AVAILABLE'),('1806','研楼304C',3,3,'AVAILABLE'),('1806','研楼306',3,3,'AVAILABLE'),('1806','研楼307',3,3,'AVAILABLE'),('1806','研楼308',3,3,'AVAILABLE'),('1806','研楼403',3,4,'AVAILABLE'),('1806','研楼404',3,4,'AVAILABLE'),('1806','研楼405',3,4,'AVAILABLE'),('1806','研楼406',3,4,'AVAILABLE'),('1806','研楼407',3,4,'AVAILABLE'),('1806','研楼408',3,4,'AVAILABLE'),('1806','研楼409',3,4,'AVAILABLE'),('1806','研楼410',3,4,'AVAILABLE'),('1806','研楼414',3,4,'AVAILABLE'),('1806','研楼415',3,4,'AVAILABLE'),('1806','研楼501',3,5,'AVAILABLE'),('1806','研楼502',3,5,'AVAILABLE'),('1806','研楼503',3,5,'AVAILABLE'),('1806','研楼504',3,5,'AVAILABLE'),('1806','研楼505',3,5,'AVAILABLE'),('1806','研楼506',3,5,'AVAILABLE'),('1806','研楼507',3,5,'AVAILABLE'),('1806','研楼508',3,5,'AVAILABLE'),('1806','研楼509',3,5,'AVAILABLE'),('1806','研楼603',3,6,'AVAILABLE'),('1806','研楼604',3,6,'AVAILABLE'),('1806','研楼605',3,6,'AVAILABLE'),('1806','研楼606',3,6,'AVAILABLE'),('1806','研楼607',3,6,'AVAILABLE'),
            ('1806','研楼608',3,6,'AVAILABLE'),('1806','研楼609',3,6,'AVAILABLE'),('1112','游泳池',3,1,'AVAILABLE'),('750','游泳馆浅水区北侧',3,1,'AVAILABLE'),('750','游泳馆浅水区南侧',3,1,'AVAILABLE'),('750','游泳馆深水区',3,1,'AVAILABLE'),('888','宇航楼103',3,1,'AVAILABLE'),('888','宇航楼104',3,1,'AVAILABLE'),('888','宇航楼113',3,1,'AVAILABLE'),('888','宇航楼116',3,1,'AVAILABLE'),('888','宇航楼203',3,2,'AVAILABLE'),('888','宇航楼307',3,3,'AVAILABLE'),('888','宇航楼308',3,3,'AVAILABLE'),('888','宇航楼311B',3,3,'AVAILABLE'),('888','宇航楼313',3,3,'AVAILABLE'),('888','宇航楼613',3,6,'AVAILABLE'),('888','宇航楼614',3,6,'AVAILABLE'),('888','宇航楼机房311',3,3,'AVAILABLE'),('1112','羽毛球场（乒羽中心）',3,1,'AVAILABLE'),('2928','至善园A104',3,1,'AVAILABLE'),('809','中关村东操场主席台',3,1,'AVAILABLE'),('809','中关村体育馆北厅140',3,1,'AVAILABLE'),('809','中关村体育馆地下乒乓球场',3,1,'AVAILABLE'),('809','中关村体育馆地下羽毛球场',3,1,'AVAILABLE'),('809','中关村体育馆辅馆',3,1,'AVAILABLE'),('809','中关村体育馆健身房',3,1,'AVAILABLE'),('809','中关村体育馆素质拓展报告厅D15',3,1,'AVAILABLE'),('809','中关村体育馆唯实报告厅',3,1,'AVAILABLE'),('809','中关村体育馆一层羽毛球场',3,1,'AVAILABLE'),('809','中关村西操场网球场',3,1,'AVAILABLE'),('809','中关村西操场足球场',3,1,'AVAILABLE'),('809','中关村校区西南篮球场',3,1,'AVAILABLE'),('1892','中关村校医院b105',3,1,'AVAILABLE'),('806','中级仪器平台实验室 310',3,3,'AVAILABLE'),('1814','中教1003',3,10,'AVAILABLE'),('1814','中教211',3,2,'AVAILABLE'),('1814','中教230',3,2,'AVAILABLE'),('1814','中教307',3,3,'AVAILABLE'),('1814','中教316',3,3,'AVAILABLE'),('1814','中教325',3,3,'AVAILABLE'),('1814','中教407',3,4,'AVAILABLE'),('1814','中教425',3,4,'AVAILABLE'),('1814','中教638',3,6,'AVAILABLE'),('1814','中教824',3,8,'AVAILABLE'),('1814','中教911',3,9,'AVAILABLE'),('1262','主楼241',3,2,'AVAILABLE'),('1262','主楼309',3,3,'AVAILABLE'),('1262','主楼317',3,3,'AVAILABLE'),('1262','主楼409',3,4,'AVAILABLE'),('1262','主楼418',3,4,'AVAILABLE'),('1262','主楼429',3,4,'AVAILABLE'),('TS0001','综合教学楼102',3,1,'AVAILABLE'),('TS0001','综合教学楼201',3,2,'AVAILABLE'),('TS0001','综合教学楼202',3,2,'AVAILABLE'),('TS0001','综合教学楼203',3,2,'AVAILABLE'),('TS0001','综合教学楼302',3,3,'AVAILABLE'),('TS0001','综合教学楼303',3,3,'AVAILABLE'),('2801','综教A101',3,1,'AVAILABLE'),('2801','综教A102',3,1,'AVAILABLE'),('2801','综教A103',3,1,'AVAILABLE'),('2801','综教A104',3,1,'AVAILABLE'),('2801','综教A105',3,1,'AVAILABLE'),('2801','综教A106',3,1,'AVAILABLE'),('2801','综教A201',3,2,'AVAILABLE'),('2801','综教A202',3,2,'AVAILABLE'),('2801','综教A203',3,2,'AVAILABLE'),('2801','综教A204',3,2,'AVAILABLE'),('2801','综教A205',3,2,'AVAILABLE'),('2801','综教A206',3,2,'AVAILABLE'),('2801','综教A301',3,3,'AVAILABLE'),('2801','综教A302',3,3,'AVAILABLE'),('2801','综教A303',3,3,'AVAILABLE'),('2801','综教A304',3,3,'AVAILABLE'),('2801','综教A305',3,3,'AVAILABLE'),('2801','综教A306',3,3,'AVAILABLE'),('2801','综教A401',3,4,'AVAILABLE'),('2801','综教A402',3,4,'AVAILABLE'),('2801','综教A403',3,4,'AVAILABLE'),('2801','综教A404',3,4,'AVAILABLE'),('2801','综教A405',3,4,'AVAILABLE'),('2801','综教A406',3,4,'AVAILABLE'),('2801','综教A501',3,5,'AVAILABLE'),('2801','综教A502',3,5,'AVAILABLE'),('2801','综教A503',3,5,'AVAILABLE'),('2801','综教A504',3,5,'AVAILABLE'),('2903','综教B101',3,1,'AVAILABLE'),('2903','综教B102',3,1,'AVAILABLE'),('2903','综教B103',3,1,'AVAILABLE'),('2903','综教B104',3,1,'AVAILABLE'),('2903','综教B105',3,1,'AVAILABLE'),('2903','综教B201',3,2,'AVAILABLE'),('2903','综教B202',3,2,'AVAILABLE'),('2903','综教B203',3,2,'AVAILABLE'),('2903','综教B204',3,2,'AVAILABLE'),('2903','综教B205',3,2,'AVAILABLE'),('2903','综教B206',3,2,'AVAILABLE'),('2903','综教B301',3,3,'AVAILABLE'),('2903','综教B302',3,3,'AVAILABLE'),('2903','综教B303',3,3,'AVAILABLE'),('2903','综教B304',3,3,'AVAILABLE'),
            ('2903','综教B305',3,3,'AVAILABLE'),('2903','综教B306',3,3,'AVAILABLE'),('2903','综教B401',3,4,'AVAILABLE'),('2903','综教B402',3,4,'AVAILABLE'),('2903','综教B403',3,4,'AVAILABLE'),('2903','综教B404',3,4,'AVAILABLE'),('2903','综教B405',3,4,'AVAILABLE'),('2903','综教B406',3,4,'AVAILABLE'),('2903','综教B501',3,5,'AVAILABLE'),('2903','综教B502',3,5,'AVAILABLE'),('2903','综教B503',3,5,'AVAILABLE'),('2903','综教B504',3,5,'AVAILABLE'),('2903','综教B505',3,5,'AVAILABLE'),('2903','综教B506(语音室)',3,5,'AVAILABLE'),('1112','足球场',3,1,'AVAILABLE'),('1112','瑜伽教室',3,1,'AVAILABLE'),('1112','毽球场（乒羽中心）',3,1,'AVAILABLE'),('1112','跆拳道教室（乒羽中心）',3,1,'AVAILABLE')
        ],
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
        [
            ('数据库系统', '1001'),
            ('计算机组成原理', '1001'),
            ('操作系统', '1001'),
            ('软件工程', '1001'),
            ('数据结构', '1002'),
            ('算法设计', '1002'),
            ('计算机网络', '1002'),
            ('编译原理', '1002'),
            ('人工智能导论', '1001'),
            ('机器学习', '1001'),
            ('深度学习', '1001'),
            ('数据挖掘', '1001'),
            ('Web前端开发', '1002'),
            ('Java程序设计', '1002'),
            ('Python程序设计', '1002'),
            ('C++程序设计', '1002'),
            ('数字逻辑', '1001'),
            ('信息安全基础', '1001'),
            ('网络安全', '1001'),
            ('云计算与虚拟化', '1001'),
            ('物联网技术', '1002'),
            ('区块链基础', '1002'),
            ('分布式系统', '1002'),
            ('软件测试', '1002'),
            ('计算思维', '1001'),
            ('高等数学A', '1002'),
            ('线性代数B', '1002'),
            ('大学物理', '1001'),
            ('现代教育技术', '1002'),
            ('创新创业实践', '1001'),
            ('形式语言与自动机', '1002'),
        ],
    ),
    (
        'INSERT INTO Schedule (course_id,classroom_id,weekday,start_period,end_period,start_week,end_week) VALUES (%s,%s,%s,%s,%s,%s,%s)',
        [
            (1, 1, 3, 3, 4, 1, 16),   # 张老师 - 数据库系统
            (2, 2, 1, 1, 2, 1, 16),   # 张老师 - 计算机组成原理
            (3, 3, 2, 3, 4, 1, 16),   # 张老师 - 操作系统
            (4, 4, 4, 5, 6, 1, 16),   # 张老师 - 软件工程
            (9, 5, 5, 1, 2, 1, 16),   # 张老师 - 人工智能导论
            (10, 6, 1, 7, 8, 1, 16),  # 张老师 - 机器学习
            (11, 7, 3, 5, 6, 1, 16),  # 张老师 - 深度学习
            (25, 8, 2, 1, 2, 1, 16),  # 张老师 - 计算思维
            (5, 9, 1, 3, 4, 1, 16),   # 王老师 - 数据结构
            (6, 10, 2, 5, 6, 1, 16),  # 王老师 - 算法设计
            (7, 11, 4, 1, 2, 1, 16),  # 王老师 - 计算机网络
            (8, 12, 5, 3, 4, 1, 16),  # 王老师 - 编译原理
            (13, 13, 2, 7, 8, 1, 16), # 王老师 - Web前端开发
        ],
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

            sql_files = [ROOT_DIR / 'sql' / 'triggers.sql', ROOT_DIR / 'sql' / 'views.sql']
            for sql_path in sql_files:
                if sql_path.exists():
                    for statement in parse_sql_file(sql_path):
                        cur.execute(statement)
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
