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
    initialValue: String,
    disabled: Boolean,
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
  },
  computed: {
    choices() {
      if (!this.initialValue) {
        return this.field.args.choices
      }

      return [...new Set([...this.field.args.choices, this.initialValue])]
    }
  }
}
</script>
