<template>
    <form id="form" @submit="submitForm" method="POST">
        <router-link to="/" class="btn btn-light mb-4">
            <i class="fas fa-arrow-left mr-1"></i>
            Overzicht
        </router-link>
        <h2>{{ field.label }}</h2>
        <FormItems :formItems="field.args.formItems" :data="this.case.data[arrayField.key][arrayField.index]" :initialData="this.case.initialData" :arrayField="arrayField" />
        <button v-if="!isDisabled" type="submit" class="btn btn-primary">Opslaan en terug</button>
    </form>
</template>

<script>
import { mapState } from 'vuex'
import FormItems from '../components/FormItems'

export default {
    name: "Form",
    components: {
        'FormItems': FormItems,
    },
    computed: {
        arrayField() {
            return {
                key: this.$route.params.key,
                index: this.$route.params.index
            }
        },
        field() {
            const formItem = this.$store.state.formItems.find((item) => item.field && item.field.key === this.arrayField.key)
            return formItem.field
        },
        ...mapState({
            case_type: state => state.case_type,
            case: state => state.case,
            csrftoken: state => state.csrftoken,
            isDisabled: state => state.case.isClosed
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
