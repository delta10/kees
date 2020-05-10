<template>
  <div>
    <label class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <div class="form-check" :key="choice" v-for="(choice, index) in choices">
      <label :for="`${field.key}-${index}`" class="form-check-label">
        <input
          type="radio"
          class="form-check-input"
          :id="`${field.key}-${index}`"
          :name="field.key"
          :value="choice"
          :checked="value == choice"
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
  name: 'RadioField',
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
    }
  }
}
</script>
