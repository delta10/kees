<template>
    <form id="form" @submit="submitForm" method="POST">
        <Alert v-if="alert" :type="alert.type" :message="alert.message" />
        <FormFields :fields="fields" v-model="value" />
        <button type="submit" class="btn btn-primary" :disabled="loading">Opslaan</button>
    </form>
</template>

<script>
import Alert from './Alert'
import FormFields from './FormFields'

export default {
    name: "Form",
    components: {
        'Alert': Alert,
        'FormFields': FormFields,
    },
    data() {
        return {
            alert: null,
            loading: false,
            fields: this.$root.fields,
            case: {
                id: this.$root.case.id
            },
            value: this.$root.case.data,
            csrftoken: this.$root.csrftoken
        }
    },
    methods: {
        async submitForm(e) {
            e.preventDefault()

            this.alert = null
            this.loading = true

            const body = {
                data: this.value
            }

            try {
                const response = await fetch(`/api/cases/${this.case.id}/`, {
                    method: 'patch',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrftoken,
                    },
                    body: JSON.stringify(body)
                })

                if (response.ok) {
                    this.showSuccessAlert()
                } else {
                    this.showErrorAlert()
                }
            } catch(e) {
                this.showErrorAlert()
            }

            this.loading = false
            scroll(0,0)
        },
        showSuccessAlert() {
            this.alert = { type: 'success', message: 'Succesvol opgeslagen.' }
        },
        showErrorAlert() {
            this.alert = { type: 'danger', message: 'Fout opgetreden tijdens opslaan. Controleer de verbinding en probeer het opnieuw.' }
        }
    }
}
</script>
