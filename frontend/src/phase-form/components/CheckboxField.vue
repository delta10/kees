<template>
  <div>
    <label class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <div class="form-check" :key="choice" v-for="(choice, index) in choices">
      <label :for="`${field.key}-${index}`" class="form-check-label">
        <input
            type="checkbox"
            class="form-check-input"
            :id="`${field.key}-${index}`"
            :name="field.key"
            :value="choice"
            :checked="currentValue.includes(choice)"
            :disabled="disabled"
            @change="onChange"
        />
        {{choice}}
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CheckboxField',
  props: {
    field: Object,
    value: { type: Array, default: () => [] },
    disabled: Boolean
  },
  data() {
    const value = this.value || []

    return {
      choices: [ ...new Set([ ...this.field.args.choices, ...value ]) ]
    }
  },
  methods: {
    onChange(e) {
      let newValue
      if (this.currentValue.includes(e.target.value)) {
        newValue = this.value.filter(choice => choice !== e.target.value)
      } else {
        newValue = [ ...this.currentValue, e.target.value ]
      }

      this.$emit('change', this.field.key, newValue)
    }
  },
  computed: {
    currentValue() {
      return Array.isArray(this.value) ? this.value : []
    }
  }
}
</script>
