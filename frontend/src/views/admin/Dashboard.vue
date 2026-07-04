<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getClassrooms } from '@/api/classroom'
import { getCourses } from '@/api/course'
import { getReservations } from '@/api/reservation'

const router = useRouter()
const stats = ref({ classrooms: 0, courses: 0, pending: 0 })

onMounted(async () => {
  const [c, co, r] = await Promise.all([
    getClassrooms({ page_size: 1 }),
    getCourses({ page_size: 1 }),
    getReservations({ status: 'PENDING', page_size: 1 }),
  ])
  stats.value = { classrooms: c.total, courses: co.total, pending: r.total }
})
</script>

<template>
  <div>
    <h3 style="margin-top: 0">管理概览</h3>
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card" @click="router.push('/admin/classrooms')">
          <div class="num">{{ stats.classrooms }}</div>
          <div class="label">教室总数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card" @click="router.push('/admin/courses')">
          <div class="num">{{ stats.courses }}</div>
          <div class="label">课程总数</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card" @click="router.push('/admin/reservations')">
          <div class="num" style="color: #e6a23c">{{ stats.pending }}</div>
          <div class="label">待审核预约</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.stat-card { text-align: center; cursor: pointer; }
.num { font-size: 36px; font-weight: 700; color: #409eff; }
.label { color: #909399; margin-top: 8px; }
</style>
