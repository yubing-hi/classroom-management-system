<script setup lang="ts">
const model = defineModel<number>({ default: 0 })

const options = [
  { label: '全部', value: 0 },
  { label: '周一', value: 1 },
  { label: '周二', value: 2 },
  { label: '周三', value: 3 },
  { label: '周四', value: 4 },
  { label: '周五', value: 5 },
  { label: '周六', value: 6 },
  { label: '周日', value: 7 },
]
</script>

<template>
  <el-select v-model="model" style="width: 120px" clearable placeholder="星期">
    <el-option v-for="o in options" :key="o.value" :label="o.label" :value="o.value" />
  </el-select>
</template>
