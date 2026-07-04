export type UserRole = 'ADMIN' | 'TEACHER' | 'STUDENT'

export interface User {
  user_id: string
  name: string
  role: UserRole
  status?: string
}

export interface Classroom {
  classroom_id: number
  building: string
  room_number: string
  capacity: number
  floor: number
  status: 'AVAILABLE' | 'MAINTENANCE'
  devices?: ClassroomDevice[]
}

export interface ClassroomDevice {
  device_id: number
  device_name: string
  device_type: string
  quantity: number
}

export interface Course {
  course_id: number
  course_name: string
  teacher_id: string
  teacher_name?: string
}

export interface Schedule {
  schedule_id: number
  course_id: number
  course_name?: string
  teacher_name?: string
  classroom_id: number
  building?: string
  room_number?: string
  weekday: number
  start_period: number
  end_period: number
  start_week: number
  end_week: number
}

export interface Reservation {
  reservation_id: number
  user_id: string
  user_name?: string
  classroom_id: number
  building?: string
  room_number?: string
  reservation_date: string
  start_period: number
  end_period: number
  purpose: string
  apply_time: string
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'CANCELLED'
  audit_comment?: string
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}
