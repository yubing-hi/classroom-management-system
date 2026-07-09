<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/auth'

const router = useRouter()
const store = useUserStore()

const navs = [
  { path: '/user', label: '首页' },
  { path: '/user/classrooms', label: '教室查询' },
  { path: '/user/courses', label: '课程查询' },
  { path: '/user/reservations', label: '我的预约' },
  { path: '/user/timetable', label: '课表视图' },
]

async function handleLogout() {
  await ElMessageBox.confirm('确定退出登录？', '提示')
  try { await logout() } catch { /* ignore */ }
  store.clearAuth()
  router.push('/login')
}
</script>

<template>
  <el-container class="user-layout">
    <el-header class="header">
      <div class="brand" @click="router.push('/user')">高校教室管理系统</div>
      <el-menu mode="horizontal" :ellipsis="false" router :default-active="$route.path" class="nav">
        <el-menu-item v-for="n in navs" :key="n.path" :index="n.path">{{ n.label }}</el-menu-item>
      </el-menu>
      <div class="user-bar">
        <span>{{ store.user?.name }}</span>
        <el-tag size="small" type="info">{{ store.user?.role === 'TEACHER' ? '教师' : '学生' }}</el-tag>
        <el-button link type="primary" @click="handleLogout">退出</el-button>
      </div>
    </el-header>
    <el-main class="main" :class="{ 'wide-main': $route.path.includes('timetable') }">
      <router-view />
    </el-main>
  </el-container>
</template>

<style scoped>
.user-layout { min-height: 100vh; background: #f0f2f5; }
.header {
  display: flex; align-items: center; background: #fff;
  border-bottom: 1px solid #e4e7ed; padding: 0 24px; gap: 24px;
}
.brand { font-size: 18px; font-weight: 600; color: #303133; cursor: pointer; white-space: nowrap; }
.nav { flex: 1; border-bottom: none; }
.user-bar { display: flex; align-items: center; gap: 10px; white-space: nowrap; }
.main { max-width: 1200px; margin: 0 auto; width: 100%; }
.main.wide-main { max-width: 1400px; }
</style>
