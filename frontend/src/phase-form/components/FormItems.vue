<template>
  <div>
    <component v-for="item in formItems"
      class="form-group"
      :is="item.field.type"
      :key="item.key"
      :field="item.field"
      :value="data[item.field.key]"
      :disabled="disabled"
      @change="onChange"
    />
  </div>
</template>

<script>
import ArrayField from './ArrayField';
import CheckboxField from './CheckboxField';
import DateField from './DateField';
import Heading from './Heading';
import NumberField from './NumberField';
import RadioField from './RadioField';
import SelectField from './SelectField';
import TextareaField from './TextareaField';
import TextField from './TextField';

export default {
  name: 'FormItems',
  components: {
    ArrayField,
    CheckboxField,
    DateField,
    Heading,
    NumberField,
    RadioField,
    SelectField,
    TextareaField,
    TextField,
  },
  props: {
    formItems: Array,
    data: Object,
    disabled: Boolean,
  },
  methods: {
    onChange(key, value) {
      this.$emit('change', key, value)
    }
  }
}
</script>
