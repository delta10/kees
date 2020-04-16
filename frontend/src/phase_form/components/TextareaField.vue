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
            :disabled="isDisabled"
            @change="updateValue"
        />
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'TextareaField',
    props: {
        field: Object,
        value: String,
        initialValue: String,
        arrayField: { type: Object }
    },
    methods: {
        updateValue(e) {
            this.$store.commit('setData', { data: { [this.field.key]: e.target.value }, arrayField: this.arrayField })
        }
    },
    computed: mapState({
        isDisabled: state => state.case.isClosed
    })
}
</script>
