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
            @input="updateValue"
        >
            <option></option>
            <option v-for="choice in field.args.choices" :key="choice" v-html="choice" :value="choice" />
        </select>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'SelectField',
    props: {
        field: Object,
        value: { type: String }
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { [this.field.key]: e.target.value })

            if (this.field.args.prefill) {
                this.prefill(e.target.value)
            }
        },
        prefill(value) {
            const { prefill } = this.field.args

            if (!prefill[value]) {
                return
            }

            this.$store.commit('setData', prefill[value])
        }
    },
    computed: mapState({
        isDisabled: state => state.case.is_closed
    })
}
</script>
