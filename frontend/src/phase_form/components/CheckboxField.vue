<template>
    <div>
        <label class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <div class="form-check" :key="choice" v-for="(choice, index) in field.args.choices">
            <label :for="`${field.key}-${index}`" class="form-check-label">
                <input
                    type="checkbox"
                    class="form-check-input"
                    :id="`${field.key}-${index}`"
                    :name="field.key"
                    :value="choice"
                    :checked="value.includes(choice)"
                    @input="updateValue"
                />
                {{choice}}
            </label>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CheckboxField',
    props: {
        field: Object,
        value: { type: Array }
    },
    methods: {
        updateValue(e) {
            let newValue
            if (this.value.includes(e.target.value)) {
                newValue = this.value.filter(choice => choice !== e.target.value)
            } else {
                newValue = [ ...this.value, e.target.value ]
            }

            this.$store.commit('setData', { [this.field.key]: newValue })
        }
    }
}
</script>
