import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import WelCome from '@/views/WelCome.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: WelCome,
      children: [
        {
          path: '/about',
          name: '/about',
          component: () => import('../views/AboutView.vue'),
        },
        {
          path: '/hello',
          name: 'hello',
          component: HomeView,
         }
      ],
      redirect: '/hello'
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
    {
      path: '/login',
      name: 'login',
      component: () => import ('@/views/LoginView.vue')
    }
  ],
})

export default router
