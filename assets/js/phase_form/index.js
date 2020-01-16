import Vue from 'vue';
import Form from './components/Form';
import FormFields from './components/FormFields';

document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#js-phase-form-entry-point');
    const data = document.querySelector('#js-phase-form-data');

    if (!el || !data) return;

    Vue.component(
        FormFields
    )

    new Vue({
        el: '#js-phase-form-entry-point',
        data: JSON.parse(data.innerHTML),
        render: (h) => h(Form)
    });
});
