import request from '@/utils/request'
import type { TimetableData, SemesterInfo } from '@/types'

export function getSemesterInfo() {
  return request.get<SemesterInfo>('/semester')
}

export function getTimetable(params: {
  week: number
  classroom_id?: number
  teacher_id?: string
}) {
  return request.get<TimetableData>('/timetable', { params })
}
