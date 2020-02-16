<template>
    <div>
        <label class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <div class="form-check" :key="choice" v-for="(choice, index) in choices">
            <label :for="`${field.key}-${index}`" class="form-check-label">
                <input
                    type="checkbox"
                    class="form-check-input"
                    :id="`${field.key}-${index}`"
                    :name="field.key"
                    :value="choice"
                    :checked="currentValue.includes(choice)"
                    :disabled="isDisabled"
                    @input="updateValue"
                />
                {{choice}}
            </label>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'CheckboxField',
    props: {
        field: Object,
        value: { type: Array, default: () => [] },
        initialValue: { type: Array, default: () => [] },
        arrayField: { type: Object }
    },
    methods: {
        updateValue(e) {
            let newValue
            if (this.currentValue.includes(e.target.value)) {
                newValue = this.value.filter(choice => choice !== e.target.value)
            } else {
                newValue = [ ...this.currentValue, e.target.value ]
            }

            this.$store.commit('setData', { data: { [this.field.key]: newValue }, arrayField: this.arrayField })
        }
    },
    computed: {
        currentValue() {
            return Array.isArray(this.value) ? this.value : []
        },
        choices() {
            if (!this.initialValue) {
                return this.field.args.choices
            }

            return [...new Set([...this.field.args.choices, ...this.initialValue])]
        },
        ...mapState({
            isDisabled: state => state.case.is_closed
        })
    }
}
</script>
