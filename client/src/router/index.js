import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store/index'
Vue.use(VueRouter)

import SignUp from '../views/SignUp.vue'
import SignIn from '../views/SignIn.vue'

const routes = [
  {
    path: '/signup',
    name: 'signup',
    component: SignUp
  },
  {
    path: '/signin',
    name: 'signin',
    component: SignIn
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

  const cognito = await store.dispatch('getUser', token)

  if (!cognito) return next('/signin')

  store.commit('tokenSet', { AccessToken: localStorage.AccessToken, IdToken: localStorage.IdToken })
  store.commit('userSet', cognito.response.Username)

  return next()
})

export default router
