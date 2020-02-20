<template>
    <div>
        <label :for="field.key" class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <select
            class="form-control"
            :id="field.key"
            :name="field.key"
            :value="value"
            :disabled="isDisabled"
            @change="updateValue"
        >
            <option></option>
            <option v-for="choice in choices" :key="choice" v-html="choice" :value="choice" />
        </select>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'SelectField',
    props: {
        field: Object,
        value: { type: String },
        initialValue: { type: String },
        arrayField: { type: Object }
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { data: { [this.field.key]: e.target.value }, arrayField: this.arrayField })

            if (this.field.args.prefill) {
                this.prefill(e.target.value)
            }
        },
        prefill(value) {
            const { prefill } = this.field.args

            if (!prefill[value]) {
                return
            }

            this.$store.commit('setData', { data: prefill[value], arrayField: this.arrayField })
        }
    },
    computed: {
        choices() {
            if (!this.initialValue) {
                return this.field.args.choices
            }

            return [...new Set([...this.field.args.choices, this.initialValue])]
        },
        ...mapState({
            isDisabled: state => state.case.is_closed
        }),
    }
}
</script>
