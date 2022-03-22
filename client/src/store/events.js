import axios from 'axios'
const state = () => ({
  events: [],
  newEvent: {
    title: '',
    description: '',
    reminders: [
      {
        date: null,
        times: []
      }
    ],
    new: true
  },
  newReminder: {
    date: null,
    times: []
  }
})

const getters = {
  events: (state) => state.events,
  newEvent: (state) => state.newEvent,
  newReminder: (state) => state.newReminder
}

const actions = {
    eventsPost (_, payload) {
        return axios.post('/events', payload).then(response => {
            return response.data
        }).catch(() => {
            return null
        })
    },
    eventsPut (_, payload) {
      return axios.put('/events', payload).then(response => {
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
    },
    eventsDelete (_, payload) {
      return axios.put('/events/delete', payload).then(response => {
          return response.data
      }).catch(() => {
          return null
      })
    },
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