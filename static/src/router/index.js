import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },

    {
      path: '/projects',
      name: 'projects',
      component: () => import('../views/ProjectsView.vue')
    },

    {
      path: '/projects/:project_id',
      name: 'project',
      props: true,
      component: () => import('../views/ProjectView.vue')
    },

    {
      path: '/projects/invites/:link',
      name: 'invite',
      props: true,
      component: () => import('../views/invite.vue')
    },

    {
      path: '/auth/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },

    {
      path: '/auth/signup',
      name: 'signup',
      component: () => import('../views/SignupView.vue')
    }
  ]
})

export default router
