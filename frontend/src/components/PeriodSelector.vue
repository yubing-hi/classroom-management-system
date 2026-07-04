<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: number
  endValue?: number
  range?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number]
  'update:endValue': [value: number]
}>()

const periods = Array.from({ length: 13 }, (_, i) => i + 1)

const end = computed({
  get: () => props.endValue ?? props.modelValue,
  set: (v) => emit('update:endValue', v),
})
</script>

<template>
  <template v-if="range">
    <el-select :model-value="modelValue" style="width: 90px" @update:model-value="emit('update:modelValue', $event)">
      <el-option v-for="p in periods" :key="p" :label="`第${p}节`" :value="p" />
    </el-select>
    <span style="margin: 0 6px">至</span>
    <el-select v-model="end" style="width: 90px">
      <el-option v-for="p in periods" :key="p" :label="`第${p}节`" :value="p" :disabled="p < modelValue" />
    </el-select>
  </template>
  <el-select v-else :model-value="modelValue" style="width: 120px" @update:model-value="emit('update:modelValue', $event)">
    <el-option v-for="p in periods" :key="p" :label="`第${p}节`" :value="p" />
  </el-select>
</template>
