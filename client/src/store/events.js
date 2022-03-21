import axios from 'axios'
const state = () => ({
  events: []
})

const getters = {
  events: (state) => state.events
}

const actions = {
    eventsPost (_, payload) {
        return axios.post('/events', payload).then(response => {
            return response.data
        }).catch(() => {
            return null
        })
    },
    eventsGet ({ commit }) {
      return axios.get('/events').then(response => {
          commit('eventsSet', response.data.items)
          return response.data
      }).catch(() => {
          return null
      })
    }
}

const mutations = {
  eventsSet: (state, array) => state.events = array
}

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}