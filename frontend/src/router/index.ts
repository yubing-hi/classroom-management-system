import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/Login.vue'),
      meta: { public: true },
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      meta: { role: 'ADMIN' },
      children: [
        { path: '', name: 'AdminDashboard', component: () => import('@/views/admin/Dashboard.vue') },
        { path: 'classrooms', name: 'AdminClassrooms', component: () => import('@/views/admin/ClassroomManage.vue') },
        { path: 'courses', name: 'AdminCourses', component: () => import('@/views/admin/CourseManage.vue') },
        { path: 'reservations', name: 'AdminReservations', component: () => import('@/views/admin/ReservationAudit.vue') },
        { path: 'timetable', name: 'AdminTimetable', component: () => import('@/views/shared/TimetableView.vue') },
      ],
    },
    {
      path: '/user',
      component: () => import('@/layouts/UserLayout.vue'),
      meta: { role: 'USER' },
      children: [
        { path: '', name: 'UserHome', component: () => import('@/views/user/Home.vue') },
        { path: 'classrooms', name: 'UserClassrooms', component: () => import('@/views/user/ClassroomQuery.vue') },
        { path: 'courses', name: 'UserCourses', component: () => import('@/views/user/CourseQuery.vue') },
        { path: 'reservations', name: 'UserReservations', component: () => import('@/views/user/Reservation.vue') },
        { path: 'timetable', name: 'UserTimetable', component: () => import('@/views/shared/TimetableView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const store = useUserStore()
  if (to.meta.public) return true
  if (!store.isLoggedIn) return '/login'

  const role = store.user?.role
  if (to.meta.role === 'ADMIN' && role !== 'ADMIN') return '/user'
  if (to.meta.role === 'USER' && role === 'ADMIN') return '/admin'
  return true
})

export default router
