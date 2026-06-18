import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../components/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'lawyers',
        name: 'LawyerList',
        component: () => import('../views/LawyerList.vue')
      },
      {
        path: 'lawyer/:id',
        name: 'LawyerDetail',
        component: () => import('../views/LawyerDetail.vue')
      },
      {
        path: 'consultation',
        name: 'ConsultationWizard',
        component: () => import('../views/ConsultationWizard.vue')
      },
      {
        path: 'appointments',
        name: 'AppointmentList',
        component: () => import('../views/AppointmentList.vue')
      }
    ]
  },
  {
    path: '/lawyer',
    component: () => import('../components/Layout.vue'),
    meta: { requiresAuth: true, role: 'lawyer' },
    children: [
      {
        path: 'cases',
        name: 'LawyerCases',
        component: () => import('../views/lawyer/Cases.vue')
      },
      {
        path: 'documents',
        name: 'LawyerDocuments',
        component: () => import('../views/lawyer/Documents.vue')
      },
      {
        path: 'knowledge',
        name: 'LawyerKnowledge',
        component: () => import('../views/lawyer/Knowledge.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: () => import('../components/Layout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue')
      },
      {
        path: 'verifications',
        name: 'AdminVerifications',
        component: () => import('../views/admin/Verifications.vue')
      },
      {
        path: 'complaints',
        name: 'AdminComplaints',
        component: () => import('../views/admin/Complaints.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.role && userStore.userInfo?.role !== to.meta.role) {
    next({ name: 'Home' })
  } else {
    next()
  }
})

export default router
