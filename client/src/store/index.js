
import Vue from 'vue'
import Vuex from 'vuex'
import auth from './auth'
import dialogs from './dialogs'
import events from './events'
import users from './users'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    dialogs,
    events,
    users
  }
})