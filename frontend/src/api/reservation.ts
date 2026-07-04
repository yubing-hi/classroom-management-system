import request from '@/utils/request'
import type { PageResult, Reservation } from '@/types'

export function getReservations(params?: Record<string, unknown>) {
  return request.get<PageResult<Reservation>>('/reservations', { params })
}

export function createReservation(data: {
  classroom_id: number
  reservation_date: string
  start_period: number
  end_period: number
  purpose: string
}) {
  return request.post('/reservations', data)
}

export function cancelReservation(id: number) {
  return request.put(`/reservations/${id}/cancel`)
}

export function auditReservation(id: number, data: { audit_result: string; audit_comment?: string }) {
  return request.post(`/reservations/${id}/audit`, data)
}
