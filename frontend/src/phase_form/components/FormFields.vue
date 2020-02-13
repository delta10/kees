<template>
    <div>
        <div v-bind:key="field.key" v-for="field in fields" class="form-group">
            <InputField v-if="field.type === 'DateField'" type="date" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <InputField v-if="field.type === 'IntegerField'" type="number" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <InputField v-if="field.type === 'CharField' && field.widget === 'TextInput'" type="text" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <CheckboxField v-if="field.type === 'MultipleChoiceField'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <RadioField v-if="field.type === 'ChoiceField' && field.widget === 'RadioSelect'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <SelectField v-if="field.type === 'ChoiceField' && field.widget === 'Select'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
            <TextareaField v-if="field.type === 'CharField' && field.widget === 'Textarea'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
        </div>
    </div>
</template>

<script>
import InputField from './InputField';
import CheckboxField from './CheckboxField';
import RadioField from './RadioField';
import SelectField from './SelectField';
import TextareaField from './TextareaField';

export default {
    name: 'FormFields',
    components: {
        InputField,
        CheckboxField,
        RadioField,
        SelectField,
        TextareaField,
    },
    props: {
        fields: Array,
        data: Object,
        initialData: Object
    }
}
</script>
