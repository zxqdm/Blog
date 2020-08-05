import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    user: localStorage.getItem('user') ?  JSON.parse(localStorage.getItem('user')) : {},
    isLogin: localStorage.getItem('isLogin') === '1',
  },
  mutations: {
    changeLoginStatus(state) {
      state.user = JSON.parse(localStorage.getItem('user'))
      state.isLogin = localStorage.getItem('isLogin') === '1'
    }
  },
})

export default store
