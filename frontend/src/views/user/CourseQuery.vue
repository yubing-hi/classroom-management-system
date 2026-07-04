<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { getSchedules } from '@/api/course'
import { useUserStore } from '@/stores/user'
import WeekdaySelect from '@/components/WeekdaySelect.vue'
import { formatWeekday, formatPeriod, formatWeekRange, formatClassroom } from '@/utils/period'
import type { Schedule } from '@/types'

const store = useUserStore()
const loading = ref(false)
const list = ref<Schedule[]>([])
const total = ref(0)
const page = ref(1)

const query = reactive({
  course_name: '',
  weekday: 0,
  mineOnly: store.user?.role === 'TEACHER',
})

const teacherId = computed(() => (query.mineOnly ? store.user?.user_id : ''))

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: 10 }
    if (teacherId.value) params.teacher_id = teacherId.value
    if (query.weekday) params.weekday = query.weekday
    const res = await getSchedules(params)
    let items = res.items
    if (query.course_name) {
      items = items.filter((s) => s.course_name?.includes(query.course_name))
    }
    list.value = items
    total.value = query.course_name ? items.length : res.total
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <el-card>
    <template #header><span>课程查询</span></template>

    <el-form :inline="true" class="filter">
      <el-form-item label="课程名"><el-input v-model="query.course_name" clearable /></el-form-item>
      <el-form-item label="星期"><WeekdaySelect v-model="query.weekday" /></el-form-item>
      <el-form-item v-if="store.user?.role === 'TEACHER'">
        <el-checkbox v-model="query.mineOnly" @change="loadData">仅看我的课程</el-checkbox>
      </el-form-item>
      <el-form-item><el-button type="primary" @click="loadData">查询</el-button></el-form-item>
    </el-form>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="course_name" label="课程名称" />
      <el-table-column prop="teacher_name" label="任课教师" width="100" />
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
    </el-table>

    <el-pagination v-model:current-page="page" :page-size="10" :total="total"
      layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadData" />
  </el-card>
</template>

<style scoped>
.filter { margin-bottom: 8px; }
</style>
