import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import App from './App';

import FormFields from './components/FormFields';
import ArrayFieldForm from './pages/ArrayFieldForm';
import PhaseForm from './pages/PhaseForm';


document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#js-phase-form-entry-point');
    const data = document.querySelector('#js-phase-form-data');

    if (!el || !data) return;

    Vue.use(VueRouter)
    Vue.use(Vuex)

    Vue.component(
        FormFields
    )

    const router = new VueRouter({
        routes: [
            { path: '/', component: PhaseForm },
            { path: '/fields/:key/:index', component: ArrayFieldForm }
        ],
        scrollBehavior() {
            return {x: 0, y: 200}
        }
    })

    const store = new Vuex.Store({
        state: JSON.parse(data.innerHTML),
        mutations: {
            setData(state, payload) {
                if (payload.arrayField) {
                    state.case.data[payload.arrayField.key][payload.arrayField.index] = { ...state.case.data[payload.arrayField.key][payload.arrayField.index], ...payload.data }
                } else {
                    state.case.data = { ...state.case.data, ...payload.data }
                }
            }
        }
    })

    new Vue({
        el: '#js-phase-form-entry-point',
        router,
        store,
        render: (h) => h(App)
    });
});
