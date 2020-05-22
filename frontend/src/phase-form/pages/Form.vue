<template>
  <form id="form" @submit="submitForm" method="POST">
    <FormItems
      :formItems="formItems"
      :data="this.case.data"
      :disabled="disabled"
      @change="onChange"
    />
    <button v-if="showSubmitButton" type="submit" class="btn btn-primary" :disabled="loading">Opslaan</button>
  </form>
</template>

<script>
import { mapState } from 'vuex';
import FormItems from '../components/FormItems';

export default {
  name: 'Form',
  props: {
    loading: Boolean
  },
  components: {
    'FormItems': FormItems,
  },
  computed: {
    showSubmitButton() {
      if (this.disabled) {
        return false
      }

      if (this.formItems.length === 0) {
        return false
      }

      return true
    },
    ...mapState({
      case: state => state.case,
      caseType: state => state.caseType,
      formItems: state => state.formItems,
      disabled: state => state.disabled
    })
  },
  methods: {
    onChange(key, value) {
      this.$store.commit('setData', {
        data: {
          [key]: value
        }
      })
    },
    submitForm(e) {
      e.preventDefault()
      this.$emit('submitForm')
    }
  }
}
</script>