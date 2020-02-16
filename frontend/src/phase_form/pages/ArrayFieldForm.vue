<template>
    <form id="form" @submit="submitForm" method="POST">
        <router-link to="/" class="btn btn-light mb-4">
            <i class="fas fa-arrow-left mr-1"></i>
            Overzicht
        </router-link>
        <h2>{{ field.label }}</h2>
        <FormFields :fields="field.args.fields" :data="this.case.data[arrayField.key][arrayField.index]" :initialData="this.case.initialData" :arrayField="arrayField" />
        <button v-if="!isDisabled" type="submit" class="btn btn-primary">Opslaan en terug</button>
    </form>
</template>

<script>
import { mapState } from 'vuex'
import FormFields from '../components/FormFields'

export default {
    name: "Form",
    components: {
        'FormFields': FormFields,
    },
    computed: {
        arrayField() {
            return {
                key: this.$route.params.key,
                index: this.$route.params.index
            }
        },
        field() {
            return this.$store.state.fields.find((f) => f.key === this.arrayField.key)
        },
        ...mapState({
            case_type: state => state.case_type,
            case: state => state.case,
            csrftoken: state => state.csrftoken,
            isDisabled: state => state.case.is_closed
        })
    },
    methods: {
        submitForm(e) {
            e.preventDefault()
            this.$router.go(-1)
        }
    }
}
</script>
