<template>
    <div>
        <div v-bind:key="index" v-for="(item, index) in formItems" class="form-group">
            <h5 v-if="item.heading">{{item.heading}}</h5>
            <hr v-if="item.heading" />
            <InputField v-if="item.field && item.field.type === 'DateField'" type="date" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <InputField v-if="item.field && item.field.type === 'IntegerField'" type="number" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <InputField v-if="item.field && item.field.type === 'CharField' && item.field.widget === 'TextInput'" type="text" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <CheckboxField v-if="item.field && item.field.type === 'MultipleChoiceField'" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <RadioField v-if="item.field && item.field.type === 'ChoiceField' && item.field.widget === 'RadioSelect'" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <SelectField v-if="item.field && item.field.type === 'ChoiceField' && item.field.widget === 'Select'" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <TextareaField v-if="item.field && item.field.type === 'CharField' && item.field.widget === 'Textarea'" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" :arrayField="arrayField" />
            <ArrayField v-if="item.field && item.field.type === 'ArrayField'" :field="item.field" :value="data[item.field.key]" :initialValue="initialData[item.field.key]" />
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
    name: 'FormItems',
    components: {
        InputField,
        CheckboxField,
        RadioField,
        SelectField,
        TextareaField,
        ArrayField,
    },
    props: {
        formItems: Array,
        data: Object,
        initialData: Object,
        arrayField: Object
    }
}
</script>
