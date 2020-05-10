<template>
  <div>
    <label :for="field.key" class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <select
      class="form-control"
      :id="field.key"
      :name="field.key"
      :value="value"
      :disabled="disabled"
      @change="onChange"
    >
      <option></option>
      <option v-for="choice in choices" :key="choice" v-html="choice" :value="choice" />
    </select>
  </div>
</template>

<script>
export default {
  name: 'SelectField',
  props: {
    field: Object,
    value: String,
    disabled: Boolean,
  },
  data() {
    const value = this.value ? [this.value] : []

    return {
      choices: [ ...new Set([ ...this.field.args.choices, ...value ]) ]
    }
  },
  methods: {
    onChange(e) {
      this.$emit('change', this.field.key, e.target.value)

      if (this.field.args.prefill) {
        this.prefill(e.target.value)
      }
    },
    prefill(value) {
      const { prefill } = this.field.args

      if (!prefill[value]) {
        return
      }

      Object.keys(prefill[value]).forEach((prefillKey) => {
        this.$emit('change', prefillKey, prefill[value][prefillKey])
      })
    }
  }
}
</script>
