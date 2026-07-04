import request from '@/utils/request'
import type { Classroom, PageResult } from '@/types'

export function getClassrooms(params?: Record<string, unknown>) {
  return request.get<PageResult<Classroom>>('/classrooms', { params })
}

export function getAvailableClassrooms(params: Record<string, unknown>) {
  return request.get<{ items: Classroom[]; total: number }>('/classrooms/available', { params })
}

export function createClassroom(data: Partial<Classroom>) {
  return request.post('/classrooms', data)
}

export function updateClassroom(id: number, data: Partial<Classroom>) {
  return request.put(`/classrooms/${id}`, data)
}

export function deleteClassroom(id: number) {
  return request.delete(`/classrooms/${id}`)
}
