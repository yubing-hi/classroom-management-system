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
  <div class="home-page">
    <el-card class="welcome">
      <h2>欢迎，{{ store.user?.name }}</h2>
      <p>请选择以下功能开始使用</p>
    </el-card>
    <div class="card-grid">
      <el-card
        v-for="c in cards"
        :key="c.path"
        shadow="hover"
        class="feature-card"
        @click="router.push(c.path)"
      >
        <div class="icon" :style="{ background: c.color }">{{ c.title[0] }}</div>
        <h3>{{ c.title }}</h3>
        <p class="desc">{{ c.desc }}</p>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.home-page { padding: 4px 0; }
.welcome { margin-bottom: 24px; }
.welcome h2 { margin: 0 0 8px; font-size: 22px; }
.welcome p { margin: 0; color: #909399; font-size: 15px; }

.card-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.feature-card {
  cursor: pointer;
  height: 260px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.feature-card:hover {
  transform: translateY(-4px);
}
.feature-card :deep(.el-card__body) {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 36px 24px;
  box-sizing: border-box;
}

.icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  color: #fff;
  font-size: 32px;
  font-weight: 700;
  line-height: 72px;
  flex-shrink: 0;
}

.feature-card h3 {
  margin: 20px 0 12px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  flex-shrink: 0;
}

.feature-card .desc {
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
