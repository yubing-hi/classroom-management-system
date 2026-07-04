<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getClassrooms, createClassroom, updateClassroom, deleteClassroom } from '@/api/classroom'
import StatusTag from '@/components/StatusTag.vue'
import { formatClassroom } from '@/utils/period'
import type { Classroom } from '@/types'

const loading = ref(false)
const list = ref<Classroom[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 10

const query = reactive({ building: '', room_number: '', capacity_min: undefined as number | undefined, floor: undefined as number | undefined, status: '' })

const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref<Partial<Classroom>>({})
const deviceDialog = ref(false)
const currentDevices = ref<Classroom['devices']>([])

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (query.building) params.building = query.building
    if (query.room_number) params.room_number = query.room_number
    if (query.capacity_min) params.capacity_min = query.capacity_min
    if (query.floor !== undefined) params.floor = query.floor
    if (query.status) params.status = query.status
    const res = await getClassrooms(params)
    list.value = res.items
    total.value = res.total
  } finally {
    loading.value = false
  }
}

function openCreate() {
  isEdit.value = false
  form.value = { building: '', room_number: '', capacity: 60, floor: 1, status: 'AVAILABLE' }
  dialogVisible.value = true
}

function openEdit(row: Classroom) {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

function showDevices(row: Classroom) {
  currentDevices.value = row.devices || []
  deviceDialog.value = true
}

async function handleSubmit() {
  const f = form.value
  if (!f.building || !f.room_number || !f.capacity || f.floor === undefined) {
    ElMessage.warning('请填写完整信息')
    return
  }
  if (isEdit.value && f.classroom_id) {
    await updateClassroom(f.classroom_id, f)
    ElMessage.success('更新成功')
  } else {
    await createClassroom(f)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

async function handleDelete(row: Classroom) {
  await ElMessageBox.confirm(`确定删除教室 ${formatClassroom(row.building, row.room_number)}？`, '警告', { type: 'warning' })
  await deleteClassroom(row.classroom_id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>

<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>教室管理</span>
        <el-button type="primary" @click="openCreate">新增教室</el-button>
      </div>
    </template>

    <el-form :inline="true" class="filter">
      <el-form-item label="楼宇"><el-input v-model="query.building" clearable /></el-form-item>
      <el-form-item label="房间号"><el-input v-model="query.room_number" clearable /></el-form-item>
      <el-form-item label="容量≥"><el-input-number v-model="query.capacity_min" :min="1" /></el-form-item>
      <el-form-item label="楼层"><el-input-number v-model="query.floor" :min="0" /></el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" clearable style="width: 120px">
          <el-option label="可用" value="AVAILABLE" />
          <el-option label="维护中" value="MAINTENANCE" />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type="primary" @click="loadData">查询</el-button></el-form-item>
    </el-form>

    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="classroom_id" label="编号" width="70" />
      <el-table-column label="位置" width="120">
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
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="showDevices(row)">设备</el-button>
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-model:current-page="page" :page-size="pageSize" :total="total"
      layout="total, prev, pager, next" style="margin-top: 16px; justify-content: flex-end"
      @current-change="loadData"
    />
  </el-card>

  <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑教室' : '新增教室'" width="480px">
    <el-form label-width="80px">
      <el-form-item label="楼宇"><el-input v-model="form.building" /></el-form-item>
      <el-form-item label="房间号"><el-input v-model="form.room_number" /></el-form-item>
      <el-form-item label="容量"><el-input-number v-model="form.capacity" :min="1" /></el-form-item>
      <el-form-item label="楼层"><el-input-number v-model="form.floor" :min="0" /></el-form-item>
      <el-form-item label="状态">
        <el-select v-model="form.status">
          <el-option label="可用" value="AVAILABLE" />
          <el-option label="维护中" value="MAINTENANCE" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="deviceDialog" title="教室设备" width="400px">
    <el-table :data="currentDevices" size="small">
      <el-table-column prop="device_name" label="设备" />
      <el-table-column prop="device_type" label="类型" />
      <el-table-column prop="quantity" label="数量" width="70" />
    </el-table>
  </el-dialog>
</template>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.filter { margin-bottom: 8px; }
.muted { color: #c0c4cc; }
</style>
