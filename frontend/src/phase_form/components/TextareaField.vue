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
            @input="updateValue"
        />
    </div>
</template>

<script>
export default {
    name: 'TextareaField',
    props: {
        field: Object,
        value: String
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { [this.field.key]: e.target.value })
        }
    }
}
</script>
