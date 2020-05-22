import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';

import App from './App';
import Form from './pages/Form';
import SubForm from './pages/SubForm';

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#js-phase-form-entry-point')
  const data = document.querySelector('#js-phase-form-data')
  if (!el || !data) return;

  Vue.use(VueRouter)
  Vue.use(Vuex)

  const store = new Vuex.Store({
    state: JSON.parse(data.innerHTML),
    mutations: {
      setData(state, payload) {
        const { arrayField, data } = payload

        if (arrayField) {
          return Vue.set(state.case.data[arrayField.key], arrayField.index, {
            ...state.case.data[arrayField.key][arrayField.index],
            ...data
          })
        }

        state.case.data = {
          ...state.case.data,
          ...data
        }
      },
      setInitialData(state, initialData) {
        state.case.initialData = initialData
      }
    }
  })

  const router = new VueRouter({
    routes: [
      { path: '/', component: Form },
      { path: '/fields/:key/:index', component: SubForm }
    ],
    scrollBehavior() {
      return { x: 0, y: 0 }
    }
  })

  new Vue({
    el: '#js-phase-form-entry-point',
    router,
    store,
    render: (c) => c(App),
  })
})
