<template>
  <div>
    <label v-bind:for="field.key" class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <textarea
      cols="40"
      rows="10"
      class="textarea form-control"
      :id="field.key"
      :name="field.key"
      :value="value"
      :disabled="disabled"
      @change="onChange"
    />
  </div>
</template>

<script>
export default {
  name: 'TextareaField',
  props: {
    field: Object,
    value: String,
    initialValue: String,
    arrayField: Object,
    disabled: Boolean,
  },
  methods: {
    onChange(e) {
      this.$emit('change', this.field.key, e.target.value)
    }
  }
}
</script>
