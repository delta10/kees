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
        value: { type: [ String, Number ] }
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { [this.field.key]: e.target.value })
        }
    },
    computed: mapState({
        isDisabled: state => state.case.is_closed
    })
}
</script>
