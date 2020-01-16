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
                    v-on:input="$emit('input', $event.target.value)"
                />
                {{choice}}
            </label>
        </div>
    </div>
</template>

<script>
export default {
    name: 'RadioField',
    props: {
        field: Object,
        value: { type: String }
    }
}
</script>
