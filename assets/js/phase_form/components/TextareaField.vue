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
            v-on:input="$emit('input', $event.target.value)"
        />
    </div>
</template>

<script>
export default {
    name: 'TextareaField',
    props: {
        field: Object,
        value: String
    }
}
</script>
