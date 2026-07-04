import request from '@/utils/request'
import type { User } from '@/types'

export function login(user_id: string, password: string) {
  return request.post<{ token: string; user: User }>('/auth/login', { user_id, password })
}

export function getMe() {
  return request.get<User>('/auth/me')
}

export function logout() {
  return request.post('/auth/logout')
}
