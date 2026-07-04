<script setup lang="ts">
defineProps<{ status: string; type?: 'classroom' | 'reservation' }>()

const classroomMap: Record<string, { label: string; type: '' | 'success' | 'warning' | 'danger' | 'info' }> = {
  AVAILABLE: { label: '可用', type: 'success' },
  MAINTENANCE: { label: '维护中', type: 'danger' },
}

const reservationMap: Record<string, { label: string; type: '' | 'success' | 'warning' | 'danger' | 'info' }> = {
  PENDING: { label: '待审核', type: 'warning' },
  APPROVED: { label: '已通过', type: 'success' },
  REJECTED: { label: '已驳回', type: 'danger' },
  CANCELLED: { label: '已取消', type: 'info' },
}
</script>

<template>
  <el-tag
    :type="(type === 'classroom' ? classroomMap : reservationMap)[status]?.type || 'info'"
    size="small"
  >
    {{ (type === 'classroom' ? classroomMap : reservationMap)[status]?.label || status }}
  </el-tag>
</template>
