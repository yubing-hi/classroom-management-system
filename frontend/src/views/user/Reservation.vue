<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getReservations, createReservation, cancelReservation } from '@/api/reservation'
import { getClassrooms } from '@/api/classroom'
import StatusTag from '@/components/StatusTag.vue'
import PeriodSelector from '@/components/PeriodSelector.vue'
import { formatClassroom, formatPeriod } from '@/utils/period'
import type { Classroom, Reservation } from '@/types'

const route = useRoute()
const loading = ref(false)
const list = ref<Reservation[]>([])
const total = ref(0)
const page = ref(1)
const classrooms = ref<Classroom[]>([])

const form = reactive({
  classroom_id: undefined as number | undefined,
  reservation_date: '',
  start_period: 1,
  end_period: 2,
  purpose: '',
})

async function loadList() {
  loading.value = true
  try {
    const res = await getReservations({ page: page.value, page_size: 10 })
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!form.classroom_id || !form.reservation_date || !form.purpose) {
    ElMessage.warning('请填写完整预约信息')
    return
  }
  await createReservation({
    classroom_id: form.classroom_id,
    reservation_date: form.reservation_date,
    start_period: form.start_period,
    end_period: form.end_period,
    purpose: form.purpose,
  })
  ElMessage.success('预约提交成功，等待审核')
  form.purpose = ''
  loadList()
}

async function handleCancel(row: Reservation) {
  await ElMessageBox.confirm('确定取消该预约？', '提示')
  await cancelReservation(row.reservation_id)
  ElMessage.success('已取消')
  loadList()
}

onMounted(async () => {
  const cr = await getClassrooms({ page_size: 100, status: 'AVAILABLE' })
  classrooms.value = cr.items
  if (route.query.classroom_id) {
    form.classroom_id = Number(route.query.classroom_id)
  }
  loadList()
})
</script>

<template>
  <el-card>
    <template #header><span>教室预约</span></template>

    <el-form :inline="true" class="reserve-form">
      <el-form-item label="教室">
        <el-select v-model="form.classroom_id" style="width: 160px" placeholder="选择教室">
          <el-option v-for="c in classrooms" :key="c.classroom_id"
            :label="formatClassroom(c.building, c.room_number)" :value="c.classroom_id" />
        </el-select>
      </el-form-item>
      <el-form-item label="日期">
        <el-date-picker v-model="form.reservation_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="节次">
        <PeriodSelector v-model="form.start_period" v-model:end-value="form.end_period" range />
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item label="用途">
        <el-input v-model="form.purpose" placeholder="请填写使用用途" style="max-width: 500px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">提交预约</el-button>
      </el-form-item>
    </el-form>

    <el-divider content-position="left">我的预约</el-divider>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="reservation_id" label="编号" width="70" />
      <el-table-column label="教室" width="100">
        <template #default="{ row }">{{ formatClassroom(row.building, row.room_number) }}</template>
      </el-table-column>
      <el-table-column prop="reservation_date" label="日期" width="120" />
      <el-table-column label="节次" width="100">
        <template #default="{ row }">{{ formatPeriod(row.start_period, row.end_period) }}</template>
      </el-table-column>
      <el-table-column prop="purpose" label="用途" show-overflow-tooltip />
      <el-table-column label="状态" width="90">
        <template #default="{ row }"><StatusTag :status="row.status" type="reservation" /></template>
      </el-table-column>
      <el-table-column prop="audit_comment" label="审核意见" show-overflow-tooltip />
      <el-table-column label="操作" width="80">
        <template #default="{ row }">
          <el-button v-if="row.status === 'PENDING' || row.status === 'APPROVED'" link type="danger" @click="handleCancel(row)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-model:current-page="page" :page-size="10" :total="total"
      layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadList" />
  </el-card>
</template>

<style scoped>
.reserve-form { margin-bottom: 0; }
</style>
