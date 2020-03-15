<template>
    <form id="form" @submit="submitForm" method="POST">
        <Alert v-if="alert" :type="alert.type" :message="alert.message" />
        <FormFields :fields="fields" :data="this.case.data" :initialData="this.case.initialData" />
        <button v-if="!isDisabled" type="submit" class="btn btn-primary" :disabled="loading">Opslaan</button>
    </form>
</template>

<script>
import { mapState } from 'vuex'
import Alert from '../components/Alert'
import FormFields from '../components/FormFields'

export default {
    name: "Form",
    components: {
        'Alert': Alert,
        'FormFields': FormFields,
    },
    data() {
        return {
            alert: null,
            loading: false
        }
    },
    computed: mapState({
        fields: state => state.fields,
        case_type: state => state.case_type,
        case: state => state.case,
        csrftoken: state => state.csrftoken,
        isDisabled: state => state.case.is_closed
    }),
    methods: {
        async submitForm(e) {
            e.preventDefault()

            this.alert = null
            this.loading = true

            const body = {
                data: this.case.data
            }

            if (!this.case.id) {
                body.case_type = this.case_type.id
            }

            try {
                const url = this.case.id ? `/api/cases/${this.case.id}/` : '/api/cases/'
                const method = this.case.id ? 'PATCH' : 'POST'

                const response = await fetch(url, {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrftoken,
                    },
                    body: JSON.stringify(body)
                })

                const data = await response.json()

                if (response.ok) {
                    this.$store.commit('setInitialData', this.case.data)

                    if (!this.case.id) {
                        window.location.href = `/cases/view/${data.id}`
                    } else {
                        this.showSuccessAlert()
                        scroll(0,0)
                    }
                } else {
                    this.showErrorAlert(data.detail)
                    scroll(0,0)
                }
            } catch(e) {
                console.error(e)
                this.showErrorAlert()
                scroll(0,0)
            }

            this.loading = false
        },
        showSuccessAlert() {
            this.alert = { type: 'success', message: 'Succesvol opgeslagen.' }
        },
        showErrorAlert(detail) {
            if (!detail) {
                detail = 'Controleer de verbinding en probeer het opnieuw.'
            }

            this.alert = { type: 'danger', message: `Fout opgetreden tijdens opslaan. ${detail}` }
        }
    }
}
</script>
