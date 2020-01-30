<template>
    <div>
        <label v-bind:for="field.key" class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <input
            class="form-control"
            :type="type"
            :id="field.key"
            :name="field.key"
            :value="value"
            v-on:input="$emit('input', $event.target.value)"
        />
    </div>
</template>

<script>
export default {
    name: 'InputField',
    props: {
        field: Object,
        type: { type: String, default: 'text' },
        value: { type: [ String, Number ] }
    }
}
</script>
