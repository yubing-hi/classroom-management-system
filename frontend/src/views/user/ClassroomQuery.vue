<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getClassrooms, getAvailableClassrooms } from '@/api/classroom'
import StatusTag from '@/components/StatusTag.vue'
import PeriodSelector from '@/components/PeriodSelector.vue'
import { formatClassroom } from '@/utils/period'
import type { Classroom } from '@/types'

const router = useRouter()
const loading = ref(false)
const list = ref<Classroom[]>([])
const total = ref(0)
const page = ref(1)
const mode = ref<'all' | 'available'>('all')

const query = reactive({ building: '', capacity_min: undefined as number | undefined })
const availQuery = reactive({ date: '', start_period: 1, end_period: 2 })

async function loadAll() {
  mode.value = 'all'
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: 10 }
    if (query.building) params.building = query.building
    if (query.capacity_min) params.capacity_min = query.capacity_min
    const res = await getClassrooms(params)
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function loadAvailable() {
  if (!availQuery.date) return
  mode.value = 'available'
  loading.value = true
  try {
    const params: Record<string, unknown> = {
      date: availQuery.date,
      start_period: availQuery.start_period,
      end_period: availQuery.end_period,
    }
    if (query.building) params.building = query.building
    if (query.capacity_min) params.capacity_min = query.capacity_min
    const res = await getAvailableClassrooms(params)
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function goReserve(row: Classroom) {
  router.push({ path: '/user/reservations', query: { classroom_id: String(row.classroom_id) } })
}

onMounted(loadAll)
</script>

<template>
  <el-card>
    <template #header><span>教室查询</span></template>

    <el-form :inline="true" class="filter">
      <el-form-item label="楼宇"><el-input v-model="query.building" clearable /></el-form-item>
      <el-form-item label="容量≥"><el-input-number v-model="query.capacity_min" :min="1" /></el-form-item>
      <el-form-item><el-button type="primary" @click="loadAll">查询全部</el-button></el-form-item>
    </el-form>

    <el-divider content-position="left">空闲教室查询</el-divider>
    <el-form :inline="true" class="filter">
      <el-form-item label="日期">
        <el-date-picker v-model="availQuery.date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="节次"><PeriodSelector v-model="availQuery.start_period" v-model:end-value="availQuery.end_period" range /></el-form-item>
      <el-form-item><el-button type="success" @click="loadAvailable">查询空闲教室</el-button></el-form-item>
    </el-form>

    <el-tag v-if="mode === 'available'" type="success" style="margin-bottom: 12px">当前显示空闲教室（共 {{ total }} 间）</el-tag>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column label="教室" width="120">
        <template #default="{ row }">{{ formatClassroom(row.building, row.room_number) }}</template>
      </el-table-column>
      <el-table-column prop="capacity" label="容量" width="80" />
      <el-table-column prop="floor" label="楼层" width="70" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }"><StatusTag :status="row.status" type="classroom" /></template>
      </el-table-column>
      <el-table-column label="设备">
        <template #default="{ row }">
          <span v-if="row.devices?.length">{{ row.devices.map((d: any) => `${d.device_name}×${d.quantity}`).join(', ') }}</span>
          <span v-else class="muted">无</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" :disabled="row.status !== 'AVAILABLE'" @click="goReserve(row)">预约</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-if="mode === 'all'" v-model:current-page="page" :page-size="10" :total="total"
      layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadAll" />
  </el-card>
</template>

<style scoped>
.filter { margin-bottom: 4px; }
.muted { color: #c0c4cc; }
</style>
