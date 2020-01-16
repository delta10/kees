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
                    v-model="value"
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
    }
}
</script>
