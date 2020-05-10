<template>
  <div>
    <label v-bind:for="field.key" class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <input
      class="form-control"
      type="date"
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
  name: 'NumberField',
  props: {
    field: Object,
    value: String,
    initialValue: String,
    disabled: Boolean,
  },
  methods: {
    onChange(e) {
      this.$emit('change', this.field.key, e.target.value)
    }
  }
}
</script>
