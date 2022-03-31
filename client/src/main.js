import Vue from 'vue'
import App from './App.vue'
import store from './store/index'
import axios from 'axios'
import vuetify from './plugins/vuetify'
import router from './views/router'
import './components/components'

axios.defaults.baseURL = 'https://78pgs8st41.execute-api.us-west-2.amazonaws.com/Prod'

window.queryString = (params) => '?' + Object.keys(params).map(key => key + '=' + params[key]).join('&')

window.flatten = (object, curr = null, result = {}) => {
    for(var key in object) {
        var value = object[key]
        var prepend = curr ? `${curr}.${key}` : key
        if (value && typeof value === "object") {
            return flatten(value, prepend, result)
        } else {
            result[prepend] = value
        }
    }
    return result
}

new Vue({
  render: h => h(App),
  vuetify,
  router,
  store
}).$mount('#app')
