<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getCourses, createCourse, updateCourse, deleteCourse,
  getSchedules, createSchedule, updateSchedule, deleteSchedule, getTeachers,
} from '@/api/course'
import { getClassrooms } from '@/api/classroom'
import WeekdaySelect from '@/components/WeekdaySelect.vue'
import { formatWeekday, formatPeriod, formatWeekRange, formatClassroom } from '@/utils/period'
import type { Course, Schedule, Classroom } from '@/types'

const activeTab = ref('courses')
const loading = ref(false)

// ── 课程 ──
const courses = ref<Course[]>([])
const courseTotal = ref(0)
const coursePage = ref(1)
const courseQuery = reactive({ course_name: '', teacher_id: '' })
const teachers = ref<{ user_id: string; name: string }[]>([])
const courseDialog = ref(false)
const courseEdit = ref(false)
const courseForm = ref({ course_name: '', teacher_id: '' })

async function loadCourses() {
  loading.value = true
  try {
    const res = await getCourses({ ...courseQuery, page: coursePage.value, page_size: 10 })
    courses.value = res.items
    courseTotal.value = res.total
  } finally {
    loading.value = false
  }
}

function openCourseCreate() {
  courseEdit.value = false
  courseForm.value = { course_name: '', teacher_id: '' }
  courseDialog.value = true
}

function openCourseEdit(row: Course) {
  courseEdit.value = true
  courseForm.value = { course_name: row.course_name, teacher_id: row.teacher_id }
  ;(courseForm.value as any).course_id = row.course_id
  courseDialog.value = true
}

async function submitCourse() {
  if (!courseForm.value.course_name || !courseForm.value.teacher_id) {
    ElMessage.warning('请填写完整')
    return
  }
  if (courseEdit.value) {
    await updateCourse((courseForm.value as any).course_id, courseForm.value)
    ElMessage.success('更新成功')
  } else {
    await createCourse(courseForm.value)
    ElMessage.success('创建成功')
  }
  courseDialog.value = false
  loadCourses()
}

async function handleDeleteCourse(row: Course) {
  await ElMessageBox.confirm(`确定删除课程「${row.course_name}」？`, '警告', { type: 'warning' })
  await deleteCourse(row.course_id)
  ElMessage.success('删除成功')
  loadCourses()
}

// ── 排课 ──
const schedules = ref<Schedule[]>([])
const scheduleTotal = ref(0)
const schedulePage = ref(1)
const scheduleQuery = reactive({ course_id: undefined as number | undefined, classroom_id: undefined as number | undefined, weekday: 0 })
const classrooms = ref<Classroom[]>([])
const scheduleDialog = ref(false)
const scheduleEdit = ref(false)
const scheduleForm = ref<Partial<Schedule>>({})

async function loadSchedules() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: schedulePage.value, page_size: 10 }
    if (scheduleQuery.course_id) params.course_id = scheduleQuery.course_id
    if (scheduleQuery.classroom_id) params.classroom_id = scheduleQuery.classroom_id
    if (scheduleQuery.weekday) params.weekday = scheduleQuery.weekday
    const res = await getSchedules(params)
    schedules.value = res.items
    scheduleTotal.value = res.total
  } finally {
    loading.value = false
  }
}

function openScheduleCreate() {
  scheduleEdit.value = false
  scheduleForm.value = { course_id: undefined, classroom_id: undefined, weekday: 1, start_period: 1, end_period: 2, start_week: 1, end_week: 16 }
  scheduleDialog.value = true
}

function openScheduleEdit(row: Schedule) {
  scheduleEdit.value = true
  scheduleForm.value = { ...row }
  scheduleDialog.value = true
}

async function submitSchedule() {
  const f = scheduleForm.value
  if (!f.course_id || !f.classroom_id) { ElMessage.warning('请选择课程和教室'); return }
  if (scheduleEdit.value && f.schedule_id) {
    await updateSchedule(f.schedule_id, f)
    ElMessage.success('更新成功')
  } else {
    await createSchedule(f)
    ElMessage.success('创建成功')
  }
  scheduleDialog.value = false
  loadSchedules()
}

async function handleDeleteSchedule(row: Schedule) {
  await ElMessageBox.confirm('确定删除该排课？', '警告', { type: 'warning' })
  await deleteSchedule(row.schedule_id)
  ElMessage.success('删除成功')
  loadSchedules()
}

onMounted(async () => {
  teachers.value = await getTeachers()
  const cr = await getClassrooms({ page_size: 100 })
  classrooms.value = cr.items
  loadCourses()
  loadSchedules()
})
</script>

<template>
  <el-card>
    <template #header><span>课程管理</span></template>
    <el-tabs v-model="activeTab">
      <!-- 课程 Tab -->
      <el-tab-pane label="课程列表" name="courses">
        <el-form :inline="true" class="filter">
          <el-form-item label="课程名"><el-input v-model="courseQuery.course_name" clearable /></el-form-item>
          <el-form-item label="教师">
            <el-select v-model="courseQuery.teacher_id" clearable style="width: 140px">
              <el-option v-for="t in teachers" :key="t.user_id" :label="t.name" :value="t.user_id" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadCourses">查询</el-button>
            <el-button type="success" @click="openCourseCreate">新增课程</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="courses" v-loading="loading" stripe>
          <el-table-column prop="course_id" label="编号" width="70" />
          <el-table-column prop="course_name" label="课程名称" />
          <el-table-column prop="teacher_name" label="任课教师" width="120" />
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button link type="primary" @click="openCourseEdit(row)">编辑</el-button>
              <el-button link type="danger" @click="handleDeleteCourse(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination v-model:current-page="coursePage" :page-size="10" :total="courseTotal"
          layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadCourses" />
      </el-tab-pane>

      <!-- 排课 Tab -->
      <el-tab-pane label="排课管理" name="schedules">
        <el-form :inline="true" class="filter">
          <el-form-item label="课程">
            <el-select v-model="scheduleQuery.course_id" clearable style="width: 160px">
              <el-option v-for="c in courses" :key="c.course_id" :label="c.course_name" :value="c.course_id" />
            </el-select>
          </el-form-item>
          <el-form-item label="教室">
            <el-select v-model="scheduleQuery.classroom_id" clearable style="width: 140px">
              <el-option v-for="c in classrooms" :key="c.classroom_id"
                :label="formatClassroom(c.building, c.room_number)" :value="c.classroom_id" />
            </el-select>
          </el-form-item>
          <el-form-item label="星期"><WeekdaySelect v-model="scheduleQuery.weekday" /></el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadSchedules">查询</el-button>
            <el-button type="success" @click="openScheduleCreate">新增排课</el-button>
          </el-form-item>
        </el-form>
        <el-table :data="schedules" v-loading="loading" stripe>
          <el-table-column prop="schedule_id" label="编号" width="70" />
          <el-table-column prop="course_name" label="课程" />
          <el-table-column prop="teacher_name" label="教师" width="100" />
          <el-table-column label="教室" width="100">
            <template #default="{ row }">{{ formatClassroom(row.building, row.room_number) }}</template>
          </el-table-column>
          <el-table-column label="星期" width="70">
            <template #default="{ row }">{{ formatWeekday(row.weekday) }}</template>
          </el-table-column>
          <el-table-column label="节次" width="100">
            <template #default="{ row }">{{ formatPeriod(row.start_period, row.end_period) }}</template>
          </el-table-column>
          <el-table-column label="周次" width="100">
            <template #default="{ row }">{{ formatWeekRange(row.start_week, row.end_week) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="160">
            <template #default="{ row }">
              <el-button link type="primary" @click="openScheduleEdit(row)">编辑</el-button>
              <el-button link type="danger" @click="handleDeleteSchedule(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination v-model:current-page="schedulePage" :page-size="10" :total="scheduleTotal"
          layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadSchedules" />
      </el-tab-pane>
    </el-tabs>
  </el-card>

  <!-- 课程弹窗 -->
  <el-dialog v-model="courseDialog" :title="courseEdit ? '编辑课程' : '新增课程'" width="440px">
    <el-form label-width="80px">
      <el-form-item label="课程名称"><el-input v-model="courseForm.course_name" /></el-form-item>
      <el-form-item label="任课教师">
        <el-select v-model="courseForm.teacher_id" style="width: 100%">
          <el-option v-for="t in teachers" :key="t.user_id" :label="`${t.name} (${t.user_id})`" :value="t.user_id" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="courseDialog = false">取消</el-button>
      <el-button type="primary" @click="submitCourse">确定</el-button>
    </template>
  </el-dialog>

  <!-- 排课弹窗 -->
  <el-dialog v-model="scheduleDialog" :title="scheduleEdit ? '编辑排课' : '新增排课'" width="500px">
    <el-form label-width="80px">
      <el-form-item label="课程">
        <el-select v-model="scheduleForm.course_id" style="width: 100%">
          <el-option v-for="c in courses" :key="c.course_id" :label="c.course_name" :value="c.course_id" />
        </el-select>
      </el-form-item>
      <el-form-item label="教室">
        <el-select v-model="scheduleForm.classroom_id" style="width: 100%">
          <el-option v-for="c in classrooms" :key="c.classroom_id"
            :label="formatClassroom(c.building, c.room_number)" :value="c.classroom_id" />
        </el-select>
      </el-form-item>
      <el-form-item label="星期">
        <el-select v-model="scheduleForm.weekday" style="width: 100%">
          <el-option v-for="d in 7" :key="d" :label="formatWeekday(d)" :value="d" />
        </el-select>
      </el-form-item>
      <el-form-item label="节次">
        <el-input-number v-model="scheduleForm.start_period" :min="1" :max="13" /> 至
        <el-input-number v-model="scheduleForm.end_period" :min="scheduleForm.start_period" :max="13" />
      </el-form-item>
      <el-form-item label="周次">
        <el-input-number v-model="scheduleForm.start_week" :min="1" /> 至
        <el-input-number v-model="scheduleForm.end_week" :min="scheduleForm.start_week" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="scheduleDialog = false">取消</el-button>
      <el-button type="primary" @click="submitSchedule">确定</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.filter { margin-bottom: 8px; }
</style>
