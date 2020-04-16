<template>
    <div class="mt-4 mb-5">
        <h5>{{field.label}}<span v-if="field.args.required !== false">*</span></h5>
        <hr />

        <table class="table table-borderless table-hover">
            <tbody>
                <tr :key="index" v-for="(item, index) in value">
                    <td scope="row">
                        <span :key="`${index}-${itemIndex}`" v-for="(item, itemIndex) in firstFormItem">
                            <b>{{ item.field.label }}</b>: {{ displayValue(item.field, value[index][item.field.key]) }}
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
            this.field.args.formItems.forEach((item) => {
                if (item.field) {
                    if (this.case.data[item.field.key]) {
                        newItem[item.field.key] = this.case.data[item.field.key]
                    } else {
                        if (item.field.type === "DateField") {
                            const now = new Date()
                            newItem[item.field.key] = now.toISOString().substring(0, 10)
                        }
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
        firstFormItem() {
            return this.field.args.formItems.slice(0, 1)
        },
        ...mapState({
            case: state => state.case,
            isDisabled: state => state.case.isClosed
        })
    }
}
</script>
