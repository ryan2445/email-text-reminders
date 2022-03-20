
import Vue from 'vue'
import Vuex from 'vuex'
import auth from './auth'
import dialogs from './dialogs'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    auth,
    dialogs
  }
})