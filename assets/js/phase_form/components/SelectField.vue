<template>
    <div>
        <label :for="field.key" class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <select class="form-control" :id="field.key" :name="field.key" :value="value" v-on:input="$emit('input', $event.target.value)">
            <option></option>
            <option v-for="choice in field.args.choices" :key="choice" v-html="choice" :value="choice" />
        </select>
    </div>
</template>

<script>
export default {
    name: 'SelectField',
    props: {
        field: Object,
        value: { type: String }
    }
}
</script>
