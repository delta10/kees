<template>
    <div>
        <div v-bind:key="field.key" v-for="field in fields" class="form-group">
            <InputField v-if="field.type === 'DateField'" type="date" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <InputField v-if="field.type === 'IntegerField'" type="number" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <InputField v-if="field.type === 'CharField' && field.widget === 'TextInput'" type="text" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <CheckboxField v-if="field.type === 'MultipleChoiceField'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <RadioField v-if="field.type === 'ChoiceField' && field.widget === 'RadioSelect'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <SelectField v-if="field.type === 'ChoiceField' && field.widget === 'Select'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <TextareaField v-if="field.type === 'CharField' && field.widget === 'Textarea'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" :arrayField="arrayField" />
            <ArrayField v-if="field.type === 'ArrayField'" :field="field" :value="data[field.key]" :initialValue="initialData[field.key]" />
        </div>
    </div>
</template>

<script>
import InputField from './InputField';
import CheckboxField from './CheckboxField';
import RadioField from './RadioField';
import SelectField from './SelectField';
import TextareaField from './TextareaField';
import ArrayField from './ArrayField';

export default {
    name: 'FormFields',
    components: {
        InputField,
        CheckboxField,
        RadioField,
        SelectField,
        TextareaField,
        ArrayField,
    },
    props: {
        fields: Array,
        data: Object,
        initialData: Object,
        arrayField: Object
    }
}
</script>
