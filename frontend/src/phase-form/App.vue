<template>
  <div>
    <Alert v-if="alert" :type="alert.type" :message="alert.message" />
    <router-view @submit-form="submitForm"></router-view>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { objectDiff } from './lib'
import Alert from './components/Alert'

export default {
  name: 'App',
  components: {
    'Alert': Alert,
  },
  data() {
    return {
      alert: null,
      loading: false
    }
  },
  computed: {
    ...mapState({
      case: state => state.case,
      caseType: state => state.caseType,
      csrftoken: state => state.csrftoken,
      disabled: state => state.disabled
    })
  },
  created() {
    window.addEventListener('beforeunload', this.beforeUnload)
  },
  watch: {
    $route() {
      this.alert = null
    }
  },
  methods: {
    async submitForm() {
      this.alert = null
      this.loading = true

      const body = {
        data: objectDiff(this.case.initialData, this.case.data)
      }

      if (!this.case.id) {
        body.case_type = this.caseType.id
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
          this.$store.commit('setInitialData', data.data)

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
    },
    beforeUnload(e) {
      const initialData = JSON.stringify(this.case.initialData)
      const data = JSON.stringify(this.case.data)
      if (initialData === data) {
        return
      }

      const message = 'Pagina verlaten? Wijzigingen die je hebt aangebracht, worden niet opgeslagen.'

      e.returnValue = message
      return message
    }
  }
}
</script>
