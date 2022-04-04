import axios from 'axios'
const state = () => ({
    userProfile: null
})

const getters = {
    userProfile: (state) => state.userProfile
}

const actions = {
    usersGet({commit}) {
        return axios.get('/users').then(response => {
            commit('userProfileSet', response.data)
            return response.data
        }).catch(() => {
            return null
        })
    },
    usersPost(_, payload) {
        return axios.post('/users', payload).then(response => {
            return response.data
        }).catch(() => {
            return null
        })
    }
}

const mutations = {
    userProfileSet: (state, object) => state.userProfile = object
}

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}