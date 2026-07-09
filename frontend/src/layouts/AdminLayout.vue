<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { OfficeBuilding, Reading, Calendar, DataBoard, Grid } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/auth'

const router = useRouter()
const route = useRoute()
const store = useUserStore()

const active = ref(route.path)

const menus = [
  { path: '/admin', label: '概览', icon: DataBoard },
  { path: '/admin/classrooms', label: '教室管理', icon: OfficeBuilding },
  { path: '/admin/courses', label: '课程管理', icon: Reading },
  { path: '/admin/reservations', label: '预约审核', icon: Calendar },
  { path: '/admin/timetable', label: '课表视图', icon: Grid },
]

async function handleLogout() {
  await ElMessageBox.confirm('确定退出登录？', '提示')
  try { await logout() } catch { /* ignore */ }
  store.clearAuth()
  router.push('/login')
}
</script>

<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="aside">
      <div class="logo">教室管理系统</div>
      <el-menu :default-active="active" router background-color="#1d2b3a" text-color="#bfcbd9" active-text-color="#409eff">
        <el-menu-item v-for="m in menus" :key="m.path" :index="m.path">
          <el-icon><component :is="m.icon" /></el-icon>
          <span>{{ m.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span>管理员端</span>
        <div class="user-bar">
          <span>{{ store.user?.name }}</span>
          <el-button link type="primary" @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.admin-layout { height: 100vh; }
.aside { background: #1d2b3a; }
.logo {
  height: 60px; line-height: 60px; text-align: center;
  color: #fff; font-size: 16px; font-weight: 600;
  border-bottom: 1px solid #2d3f52;
}
.header {
  display: flex; justify-content: space-between; align-items: center;
  background: #fff; border-bottom: 1px solid #ebeef5;
}
.user-bar { display: flex; align-items: center; gap: 12px; }
.main { background: #f5f7fa; }
</style>
