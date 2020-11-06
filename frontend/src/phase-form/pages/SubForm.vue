<template>
    <form id="form" @submit="submitForm" method="POST">
        <router-link to="/" class="btn btn-light mb-4">
          <i class="fas fa-arrow-left mr-1"></i>
          Overzicht
        </router-link>
        <h2 class="mb-5">{{ field.label }}</h2>
        <FormItems
          :formItems="field.args.formItems"
          :data="this.case.data[arrayField.key][arrayField.index]"
          :disabled="disabled"
          @change="onChange"
        />
        <button v-if="!disabled" type="submit" class="btn btn-primary">Opslaan en terug</button>
    </form>
</template>

<script>
import { mapState } from 'vuex'
import FormItems from '../components/FormItems'

export default {
    name: 'ArrayFieldForm',
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
        case: state => state.case,
        caseType: state => state.caseType,
        formItems: state => state.formItems,
        csrftoken: state => state.csrftoken,
        disabled: state => state.disabled
      })
    },
    methods: {
      onChange(key, value) {
        this.$store.commit('setData', {
          arrayField: this.arrayField,
          data: {
            [key]: value
          }
        })
      },
      submitForm(e) {
        e.preventDefault()
        this.$emit('submit-form')
        this.$router.go(-1)
      }
    }
}
</script>
