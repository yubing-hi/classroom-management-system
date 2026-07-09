<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const store = useUserStore()

const cards = [
  { title: '教室查询', desc: '浏览教室信息，按日期节次查询空闲教室', path: '/user/classrooms', color: '#409eff' },
  { title: '课程查询', desc: '查看课程安排与上课教室', path: '/user/courses', color: '#67c23a' },
  { title: '教室预约', desc: '提交预约申请，管理我的预约', path: '/user/reservations', color: '#e6a23c' },
  { title: '课表视图', desc: '按周查看排课与预约占用情况', path: '/user/timetable', color: '#909399' },
]
</script>

<template>
  <div>
    <el-card class="welcome">
      <h2>欢迎，{{ store.user?.name }}</h2>
      <p>请选择以下功能开始使用</p>
    </el-card>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6" v-for="c in cards" :key="c.path">
        <el-card shadow="hover" class="feature-card" @click="router.push(c.path)">
          <div class="icon" :style="{ background: c.color }">{{ c.title[0] }}</div>
          <h3>{{ c.title }}</h3>
          <p>{{ c.desc }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.welcome h2 { margin: 0 0 8px; }
.welcome p { margin: 0; color: #909399; }
.feature-card { cursor: pointer; text-align: center; padding: 12px 0; }
.feature-card h3 { margin: 12px 0 8px; }
.feature-card p { color: #909399; font-size: 13px; margin: 0; }
.icon {
  width: 48px; height: 48px; border-radius: 12px; margin: 0 auto;
  color: #fff; font-size: 22px; font-weight: 700; line-height: 48px;
}
</style>
