import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'
Vue.use(VueRouter)

import Home from './Home.vue'
import Settings from './Settings.vue'
import SignUp from './SignUp.vue'
import SignIn from './SignIn.vue'

const routes = [
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings
  },
  {
    path: '/signin',
    name: 'signin',
    component: SignIn
  },
  {
    path: '/home',
    name: 'home',
    component: Home
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.path == '/signup' || to.path == '/signin') return next()

  const token = localStorage.AccessToken

  if (!token) return next('/signin')

  store.commit('tokenSet', { AccessToken: localStorage.AccessToken, IdToken: localStorage.IdToken })
  
  if (!store.getters.user) await store.dispatch('getUser', token)

  if (!store.getters.userProfile) await store.dispatch('usersGet')

  return next()
})

export default router
