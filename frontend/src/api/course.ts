import request from '@/utils/request'
import type { Course, PageResult, Schedule } from '@/types'

export function getCourses(params?: Record<string, unknown>) {
  return request.get<PageResult<Course>>('/courses', { params })
}

export function createCourse(data: { course_name: string; teacher_id: string }) {
  return request.post('/courses', data)
}

export function updateCourse(id: number, data: Partial<Course>) {
  return request.put(`/courses/${id}`, data)
}

export function deleteCourse(id: number) {
  return request.delete(`/courses/${id}`)
}

export function getSchedules(params?: Record<string, unknown>) {
  return request.get<PageResult<Schedule>>('/schedules', { params })
}

export function createSchedule(data: Partial<Schedule>) {
  return request.post('/schedules', data)
}

export function updateSchedule(id: number, data: Partial<Schedule>) {
  return request.put(`/schedules/${id}`, data)
}

export function deleteSchedule(id: number) {
  return request.delete(`/schedules/${id}`)
}

export function getTeachers() {
  return request.get<{ user_id: string; name: string }[]>('/users/teachers')
}
