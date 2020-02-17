<template>
    <div class="mb-5">
        <label class="col-form-label mb-3">
            {{field.label}}<span v-if="field.args.required !== false">*</span>
        </label>
        <table class="table table-hover">
            <tbody>
                <tr :key="index" v-for="(item, index) in value">
                    <td scope="row">
                        <span :key="`${index}-${fieldIndex}`" v-for="(field, fieldIndex) in firstField">
                            <b>{{ field.label }}</b>: {{ displayValue(field, value[index][field.key]) }}
                        </span>
                    </td>
                    <td>
                        <router-link :to="`/fields/${field.key}/${index}`" class="btn btn-light">Bekijken</router-link>&nbsp;
                        <button v-if="!isDisabled" type="button" @click="deleteItem(index)" class="btn btn-light">Verwijderen</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <button v-if="!isDisabled" type="button" @click="addItem()" class="btn btn-light">{{field.label}} toevoegen</button>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'ArrayField',
    props: {
        field: Object,
        value: { type: [ Array ] },
        initialValue: { type: [ Array ] }
    },
    methods: {
        addItem() {
            let newItem = {}
            this.field.args.fields.forEach((field) => {
                if (this.case.data[field.key]) {
                    newItem[field.key] = this.case.data[field.key]
                } else {
                    if (field.type === "DateField") {
                        const now = new Date()
                        newItem[field.key] = now.toISOString().substring(0, 10)
                    }
                }
            })

            this.$store.commit('setData', {
                data: {
                    [this.field.key]: [ ...this.value || [], newItem ]
                }
            })
        },
        deleteItem(index) {
            if (!confirm('Weet je zeker dat je dit item wil verwijderen?')) {
                return
            }

            this.$store.commit('setData', {
                data: {
                    [this.field.key]: this.value.filter((i, j) => index !== j)
                }
            })
        },
        updateValue(e) {
            this.$store.commit('setData', {
                data: {
                    [this.field.key]: e.target.value
                }
            })
        },
        displayValue(field, value) {
            switch (field.type) {
                case "DateField":
                    return new Date(value).toLocaleDateString('nl-NL', { day: '2-digit', month: '2-digit', year: 'numeric' })
                case "DateTimeField":
                    return new Date(value).toLocaleDateString('nl-NL', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
                default:
                    return value
            }
        }
    },
    computed: {
        firstField() {
            return this.field.args.fields.slice(0, 1)
        },
        ...mapState({
            case: state => state.case,
            isDisabled: state => state.case.is_closed
        })
    }
}
</script>
