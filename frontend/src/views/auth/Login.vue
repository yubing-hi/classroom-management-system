<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const store = useUserStore()

const form = ref({ user_id: '', password: '' })
const loading = ref(false)

async function handleLogin() {
  if (!form.value.user_id || !form.value.password) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    const res = await login(form.value.user_id, form.value.password)
    store.setAuth(res.token, res.user)
    ElMessage.success('登录成功')
    router.push(res.user.role === 'ADMIN' ? '/admin' : '/user')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <el-card class="login-card" shadow="hover">
      <h2>高校教室管理系统</h2>
      <p class="subtitle">请使用学号/工号登录</p>
      <el-form @submit.prevent="handleLogin">
        <el-form-item label="账号">
          <el-input v-model="form.user_id" placeholder="学号或工号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" style="width: 100%" :loading="loading" @click="handleLogin">登 录</el-button>
      </el-form>
      <div class="hint">
        <p>测试账号：管理员 9001 / 教师 1001 / 学生 2001</p>
        <p>密码均为 123456</p>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card { width: 400px; padding: 12px; }
.login-card h2 { text-align: center; margin: 0 0 8px; color: #303133; }
.subtitle { text-align: center; color: #909399; margin-bottom: 24px; font-size: 14px; }
.hint { margin-top: 20px; font-size: 12px; color: #909399; text-align: center; line-height: 1.8; }
</style>
