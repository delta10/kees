import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import App from './App';

import FormItems from './components/FormItems';
import ArrayFieldForm from './pages/ArrayFieldForm';
import PhaseForm from './pages/PhaseForm';


document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#js-phase-form-entry-point');
    const data = document.querySelector('#js-phase-form-data');

    if (!el || !data) return;

    Vue.use(VueRouter)
    Vue.use(Vuex)

    Vue.component(
        FormItems
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
            },
            setInitialData(state, payload) {
                state.case.initialData = payload
            }
        }
    })

    new Vue({
        el: '#js-phase-form-entry-point',
        router,
        store,
        render: (h) => h(App),
        created() {
            window.addEventListener('beforeunload', this.beforeUnload)
        },
        methods: {
            beforeUnload(e) {
                const initialData = JSON.stringify(this.$store.state.case.initialData)
                const currentData = JSON.stringify(this.$store.state.case.data)

                if (initialData === currentData) {
                    return
                }

                const message = 'Site verlaten? Wijzigingen die je hebt aangebracht, worden niet opgeslagen.'
                e.returnValue = message
                return message
            }
        }
    });
});
