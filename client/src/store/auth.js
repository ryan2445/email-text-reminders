import axios from 'axios'
const state = () => ({
  user: null
})

const getters = {
  user: (state) => state.user
}

const actions = {
    signUp (_, payload) {
        return axios.post('/auth/signup', payload).then(response => {
            return response.data
        }).catch(() => {
            return null
        })
    },
    signUpConfirm (_, payload) {
      return axios.post('/auth/signupconfirm', payload).then(response => {
          return response.data
      }).catch(() => {
          return null
      })
    },
    signIn (_, payload) {
        return axios.post('/auth/signin', payload).then(response => {
            return response.data
        }).catch(() => {
            return null
        })
    },
    getUser ({commit}, token) {
      return axios.get(`/auth/user?token=${token}`).then(response => {
          commit('userSet', response.data.UserAttributes.find(attr => attr.Name == 'email').Value)
          return response.data
      }).catch(() => {
          return null
      })
    },
    signOut ({ commit }, payload) {
      return axios.post('/auth/signout', payload).then(response => {
          commit('userSet', null)
          return response.data
      }).catch(() => {
          return null
      })
    }
}

const mutations = {
  userSet: (state, object) => state.user = object,
  tokenReset: (_) => {
    localStorage.clear()
    axios.defaults.headers.common['Authorization'] = ''
  },
  tokenSet: (_, AuthenticationResult) => {
    localStorage.AccessToken = AuthenticationResult.AccessToken
    localStorage.IdToken = AuthenticationResult.IdToken
    axios.defaults.headers.common['Authorization'] = `Bearer ${AuthenticationResult.IdToken}`
  }
}

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}
