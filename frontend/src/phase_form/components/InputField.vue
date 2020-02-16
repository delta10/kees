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
            :disabled="isDisabled"
            :step="(type == 'number') ? '0.01' : null"
            @input="updateValue"
        />
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'InputField',
    props: {
        field: Object,
        type: { type: String, default: 'text' },
        value: { type: [ String, Number ] },
        initialValue: { type: [ String, Number ] },
        arrayField: { type: Object }
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { data: { [this.field.key]: e.target.value }, arrayField: this.arrayField })
        }
    },
    computed: mapState({
        isDisabled: state => state.case.is_closed
    })
}
</script>
