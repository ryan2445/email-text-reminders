const state = () => ({
    dialogs: []
})

const getters = {
    dialogs: (state) => state.dialogs
}

const actions = {
    dialogOpen ({ commit }, params) {
        commit('dialogsPush', params)
    },
    dialogClose({commit}) {
        commit('dialogsPop')
    }
}

const mutations = {
    dialogsPush: (state, object) => state.dialogs.push(object),
    dialogsPop: (state) => state.dialogs.pop()
}

export default {
  namespaced: false,
  state,
  getters,
  actions,
  mutations
}