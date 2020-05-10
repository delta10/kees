<template>
  <div>
    <label v-bind:for="field.key" class="col-form-label">
      {{field.label}}<span v-if="field.args.required !== false">*</span>
    </label>
    <div v-for="(item, index) in internalValue" :key="index" class="d-flex mb-1">
      <input
        class="form-control"
        type="text"
        :id="field.key"
        :name="`${field.key}.${index}`"
        :value="item"
        :disabled="disabled"
        @change="(e) => onChangeItem(e, index)"
      />
      <button v-if="!disabled" type="button" @click="(e) => deleteItem(e, index)" class="btn btn-link" :aria-label="`Veld ${item} verwijderen`">
        <i class="fas fa-times text-secondary"></i>
      </button>
    </div>
    <div class="mt-2">
      <button v-if="!disabled" type="button" @click="addItem" class="btn btn-outline-secondary">
        Veld toevoegen
      </button>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';

export default {
  name: 'ArrayTextField',
  props: {
    field: Object,
    value: [ Array, String ],
    disabled: Boolean,
  },
  data() {
    if (Array.isArray(this.value)) {
      return { internalValue: this.value }
    }

    return { internalValue: [this.value] }
  },
  methods: {
    addItem(e) {
      e.preventDefault()
      this.internalValue = [ ...this.internalValue, "" ]
      this.$emit('change', this.field.key, this.internalValue)
    },
    deleteItem(e, index) {
      e.preventDefault()
      this.internalValue = this.internalValue.filter((i, j) => index !== j)
      this.$emit('change', this.field.key, this.internalValue)
    },
    onChangeItem(e, index) {
      Vue.set(this.internalValue, index, e.target.value)
      this.$emit('change', this.field.key, this.internalValue)
    }
  }
}
</script>
