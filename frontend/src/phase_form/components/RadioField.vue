<template>
    <div>
        <label class="col-form-label">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <div class="form-check" :key="choice" v-for="(choice, index) in field.args.choices">
            <label :for="`${field.key}-${index}`" class="form-check-label">
                <input
                    type="radio"
                    class="form-check-input"
                    :id="`${field.key}-${index}`"
                    :name="field.key"
                    :value="choice"
                    :checked="value == choice"
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
    name: 'RadioField',
    props: {
        field: Object,
        value: { type: String }
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
