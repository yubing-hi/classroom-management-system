<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getReservations, auditReservation } from '@/api/reservation'
import StatusTag from '@/components/StatusTag.vue'
import { formatClassroom, formatPeriod } from '@/utils/period'
import type { Reservation } from '@/types'

const loading = ref(false)
const list = ref<Reservation[]>([])
const total = ref(0)
const page = ref(1)
const query = reactive({ status: 'PENDING' })

const auditDialog = ref(false)
const auditForm = ref({ reservation_id: 0, audit_result: 'APPROVED', audit_comment: '' })

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: 10 }
    if (query.status) params.status = query.status
    const res = await getReservations(params)
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function openAudit(row: Reservation, result: string) {
  auditForm.value = { reservation_id: row.reservation_id, audit_result: result, audit_comment: '' }
  auditDialog.value = true
}

async function submitAudit() {
  await auditReservation(auditForm.value.reservation_id, {
    audit_result: auditForm.value.audit_result,
    audit_comment: auditForm.value.audit_comment,
  })
  ElMessage.success('审核完成')
  auditDialog.value = false
  loadData()
}

onMounted(loadData)
</script>

<template>
  <el-card>
    <template #header><span>预约审核</span></template>

    <el-form :inline="true" class="filter">
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable style="width: 130px" placeholder="全部">
          <el-option label="待审核" value="PENDING" />
          <el-option label="已通过" value="APPROVED" />
          <el-option label="已驳回" value="REJECTED" />
          <el-option label="已取消" value="CANCELLED" />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type="primary" @click="loadData">查询</el-button></el-form-item>
    </el-form>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="reservation_id" label="编号" width="70" />
      <el-table-column prop="user_name" label="申请人" width="100" />
      <el-table-column label="教室" width="100">
        <template #default="{ row }">{{ formatClassroom(row.building, row.room_number) }}</template>
      </el-table-column>
      <el-table-column prop="reservation_date" label="日期" width="120" />
      <el-table-column label="节次" width="100">
        <template #default="{ row }">{{ formatPeriod(row.start_period, row.end_period) }}</template>
      </el-table-column>
      <el-table-column prop="purpose" label="用途" show-overflow-tooltip />
      <el-table-column prop="apply_time" label="申请时间" width="170" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }"><StatusTag :status="row.status" type="reservation" /></template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'PENDING'">
            <el-button link type="success" @click="openAudit(row, 'APPROVED')">通过</el-button>
            <el-button link type="danger" @click="openAudit(row, 'REJECTED')">驳回</el-button>
          </template>
          <span v-else-if="row.audit_comment" class="comment">{{ row.audit_comment }}</span>
          <span v-else class="muted">—</span>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-model:current-page="page" :page-size="10" :total="total"
      layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end" @current-change="loadData" />
  </el-card>

  <el-dialog v-model="auditDialog" :title="auditForm.audit_result === 'APPROVED' ? '通过审核' : '驳回审核'" width="420px">
    <el-form label-width="80px">
      <el-form-item label="审核意见"><el-input v-model="auditForm.audit_comment" type="textarea" :rows="3" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="auditDialog = false">取消</el-button>
      <el-button :type="auditForm.audit_result === 'APPROVED' ? 'success' : 'danger'" @click="submitAudit">确定</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.filter { margin-bottom: 8px; }
.comment { font-size: 12px; color: #909399; }
.muted { color: #c0c4cc; }
</style>
