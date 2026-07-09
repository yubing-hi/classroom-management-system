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
    <div class="login-left">
      <div class="brand">
        <h1>高校教室管理系统</h1>
        <p>高效管理教室资源，便捷查询与预约</p>
        <ul class="features">
          <li>教室空闲查询</li>
          <li>课程安排浏览</li>
          <li>在线预约申请</li>
          <li>课表视图展示</li>
        </ul>
      </div>
    </div>
    <div class="login-right">
      <div class="login-form">
        <h2>用户登录</h2>
        <p class="subtitle">请使用学号/工号登录</p>
        <el-form @submit.prevent="handleLogin" label-position="top">
          <el-form-item label="账号">
            <el-input v-model="form.user_id" placeholder="学号或工号" size="large" />
          </el-form-item>
          <el-form-item label="密码">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="密码"
              show-password
              size="large"
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="handleLogin">
            登 录
          </el-button>
        </el-form>
        <div class="hint">
          <p>测试账号：管理员 9001 / 教师 1001 / 学生 2001</p>
          <p>密码均为 123456</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
}
.login-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}
.brand { max-width: 420px; }
.brand h1 { font-size: 32px; font-weight: 700; margin: 0 0 16px; line-height: 1.3; }
.brand > p { font-size: 16px; opacity: 0.9; margin: 0 0 32px; line-height: 1.6; }
.features { list-style: none; padding: 0; margin: 0; }
.features li {
  padding: 10px 0; font-size: 15px; opacity: 0.85;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}
.features li:last-child { border-bottom: none; }
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: #fff;
}
.login-form { width: 100%; max-width: 400px; }
.login-form h2 { margin: 0 0 8px; color: #303133; font-size: 26px; }
.subtitle { color: #909399; margin-bottom: 32px; font-size: 14px; }
.hint { margin-top: 24px; font-size: 12px; color: #909399; text-align: center; line-height: 1.8; }
</style>
