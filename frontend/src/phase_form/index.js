import Vue from 'vue';
import Vuex from 'vuex';
import Form from './components/Form';
import FormFields from './components/FormFields';

document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#js-phase-form-entry-point');
    const data = document.querySelector('#js-phase-form-data');

    if (!el || !data) return;

    Vue.component(
        FormFields
    )

    const store = new Vuex.Store({
        state: JSON.parse(data.innerHTML),
        mutations: {
            setData(state, newData) {
                state.case.data = { ...state.case.data, ...newData }
            }
        }
    })

    new Vue({
        el: '#js-phase-form-entry-point',
        store,
        render: (h) => h(Form)
    });
});
