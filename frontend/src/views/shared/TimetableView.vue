<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { getTimetable, getSemesterInfo } from '@/api/timetable'
import { getClassrooms } from '@/api/classroom'
import { formatClassroom, formatWeekLabel, formatWeekday } from '@/utils/period'
import { useUserStore } from '@/stores/user'
import type { Classroom, TimetableReservation, TimetableSchedule } from '@/types'

const PERIODS = Array.from({ length: 13 }, (_, i) => i + 1)
const WEEKDAYS = [1, 2, 3, 4, 5, 6, 7]

const store = useUserStore()
const loading = ref(false)
const week = ref(1)
const totalWeeks = ref(20)
const weekStart = ref('')
const weekEnd = ref('')
const dates = ref<string[]>([])
const schedules = ref<TimetableSchedule[]>([])
const reservations = ref<TimetableReservation[]>([])
const classrooms = ref<Classroom[]>([])
const classroomId = ref<number | undefined>()
const onlyMine = ref(false)

const weekLabel = computed(() =>
  weekStart.value && weekEnd.value
    ? formatWeekLabel(week.value, weekStart.value, weekEnd.value)
    : `第${week.value}周`,
)

function dateForWeekday(weekday: number): string {
  return dates.value[weekday - 1] ?? ''
}

function eventsAt(weekday: number, period: number) {
  const date = dateForWeekday(weekday)
  const scheduleEvents = schedules.value
    .filter((s) => s.weekday === weekday && period >= s.start_period && period <= s.end_period)
    .map((s) => ({
      key: `s-${s.schedule_id}-${period}`,
      type: 'schedule' as const,
      title: s.course_name,
      sub: `${formatClassroom(s.building, s.room_number)} · ${s.teacher_name}`,
      isStart: period === s.start_period,
      span: s.end_period - s.start_period + 1,
    }))

  const reservationEvents = reservations.value
    .filter(
      (r) => r.reservation_date === date && period >= r.start_period && period <= r.end_period,
    )
    .map((r) => ({
      key: `r-${r.reservation_id}-${period}`,
      type: r.status === 'PENDING' ? ('pending' as const) : ('approved' as const),
      title: r.purpose,
      sub: `${formatClassroom(r.building, r.room_number)} · ${r.user_name}`,
      isStart: period === r.start_period,
      span: r.end_period - r.start_period + 1,
    }))

  return [...scheduleEvents, ...reservationEvents]
}

async function loadClassrooms() {
  const res = await getClassrooms({ page_size: 500, status: 'AVAILABLE' })
  classrooms.value = res.items
}

async function loadTimetable() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { week: week.value }
    if (classroomId.value) params.classroom_id = classroomId.value
    if (onlyMine.value && store.user?.role === 'TEACHER') {
      params.teacher_id = store.user.user_id
    }
    const data = await getTimetable(params as { week: number; classroom_id?: number; teacher_id?: string })
    week.value = data.week
    totalWeeks.value = data.total_weeks
    weekStart.value = data.week_start
    weekEnd.value = data.week_end
    dates.value = data.dates
    schedules.value = data.schedules
    reservations.value = data.reservations
  } finally {
    loading.value = false
  }
}

async function init() {
  const info = await getSemesterInfo()
  totalWeeks.value = info.total_weeks
  week.value = info.current_week
  await Promise.all([loadClassrooms(), loadTimetable()])
}

function prevWeek() {
  if (week.value > 1) {
    week.value -= 1
    loadTimetable()
  }
}

function nextWeek() {
  if (week.value < totalWeeks.value) {
    week.value += 1
    loadTimetable()
  }
}

function goCurrentWeek() {
  getSemesterInfo().then((info) => {
    week.value = info.current_week
    loadTimetable()
  })
}

watch([classroomId, onlyMine], () => loadTimetable())

onMounted(init)
</script>

<template>
  <el-card class="timetable-card" v-loading="loading">
    <template #header>
      <div class="header-row">
        <span class="title">可视化课表</span>
        <div class="legend">
          <span class="legend-item schedule">排课</span>
          <span class="legend-item approved">已通过预约</span>
          <span class="legend-item pending">待审核预约</span>
        </div>
      </div>
    </template>

    <div class="toolbar">
      <div class="week-nav">
        <el-button :disabled="week <= 1" @click="prevWeek">上一周</el-button>
        <span class="week-text">{{ weekLabel }}</span>
        <el-button :disabled="week >= totalWeeks" @click="nextWeek">下一周</el-button>
        <el-button link type="primary" @click="goCurrentWeek">回到本周</el-button>
      </div>
      <div class="filters">
        <el-select
          v-model="classroomId"
          clearable
          filterable
          placeholder="全部教室"
          style="width: 220px"
        >
          <el-option
            v-for="c in classrooms"
            :key="c.classroom_id"
            :label="formatClassroom(c.building, c.room_number)"
            :value="c.classroom_id"
          />
        </el-select>
        <el-checkbox
          v-if="store.user?.role === 'TEACHER'"
          v-model="onlyMine"
          label="仅看我的课程"
        />
      </div>
    </div>

    <div class="table-wrap">
      <table class="timetable">
        <thead>
          <tr>
            <th class="period-col">节次</th>
            <th v-for="wd in WEEKDAYS" :key="wd">
              <div>{{ formatWeekday(wd) }}</div>
              <div class="date-sub">{{ dateForWeekday(wd).slice(5) }}</div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in PERIODS" :key="p">
            <td class="period-col">第{{ p }}节</td>
            <td v-for="wd in WEEKDAYS" :key="`${wd}-${p}`" class="cell">
              <div
                v-for="ev in eventsAt(wd, p)"
                :key="ev.key"
                class="event"
                :class="[ev.type, { continued: !ev.isStart }]"
              >
                <template v-if="ev.isStart">
                  <div class="event-title">{{ ev.title }}</div>
                  <div class="event-sub">{{ ev.sub }}</div>
                </template>
                <template v-else>↑ 续</template>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </el-card>
</template>

<style scoped>
.timetable-card {
  max-width: none;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.title {
  font-weight: 600;
  font-size: 16px;
}
.legend {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #606266;
}
.legend-item {
  padding-left: 14px;
  position: relative;
}
.legend-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 10px;
  height: 10px;
  border-radius: 2px;
}
.legend-item.schedule::before { background: #409eff; }
.legend-item.approved::before { background: #67c23a; }
.legend-item.pending::before { background: #e6a23c; }

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}
.week-nav {
  display: flex;
  align-items: center;
  gap: 12px;
}
.week-text {
  font-weight: 600;
  min-width: 200px;
  text-align: center;
}
.filters {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-wrap {
  overflow-x: auto;
}
.timetable {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  min-width: 960px;
}
.timetable th,
.timetable td {
  border: 1px solid #ebeef5;
  vertical-align: top;
  padding: 4px;
}
.timetable th {
  background: #f5f7fa;
  font-weight: 600;
  padding: 8px 4px;
  text-align: center;
}
.date-sub {
  font-size: 12px;
  color: #909399;
  font-weight: normal;
  margin-top: 2px;
}
.period-col {
  width: 64px;
  text-align: center;
  background: #fafafa;
  font-size: 13px;
  color: #606266;
}
.cell {
  height: 52px;
  min-width: 110px;
  background: #fff;
}
.event {
  border-radius: 4px;
  padding: 3px 6px;
  margin-bottom: 3px;
  font-size: 12px;
  line-height: 1.35;
  border-left: 3px solid;
}
.event.schedule {
  background: #ecf5ff;
  border-left-color: #409eff;
  color: #303133;
}
.event.approved {
  background: #f0f9eb;
  border-left-color: #67c23a;
  color: #303133;
}
.event.pending {
  background: #fdf6ec;
  border-left-color: #e6a23c;
  color: #303133;
}
.event.continued {
  opacity: 0.55;
  text-align: center;
  padding: 2px;
}
.event-title {
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.event-sub {
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
