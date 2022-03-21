<template>
    <div>
        <v-card>
            <div class="d-flex flex-column pa-8">
                <div class="d-flex flex-row justify-space-between align-center">
                    <div class="d-flex flex-row" style="width:100%">
                        <div class="mr-8" style="max-width:200px;">
                            <span v-if="temp.editing">
                                <v-text-field v-model="temp.title" color="primary"
                                    label="Event Title" />
                            </span>
                            <span v-else>
                                {{ temp.title }}
                            </span>
                        </div>
                        <div style="width:100%; max-width:600px;">
                            <span v-if="temp.editing">
                                <v-text-field v-model="temp.description" color="primary"
                                    label="Event Description" />
                            </span>
                            <span v-else>
                                {{ temp.description }}
                            </span>
                        </div>
                    </div>
                    <div style="width:100px;">
                        <v-btn v-if="!temp.editing" @click="edit" icon color="primary">
                            <v-icon>
                                mdi-application-edit
                            </v-icon>
                        </v-btn>
                    </div>
                </div>
                <div v-if="temp.editing" class="text-right">
                    <v-btn @click="save" color="primary">
                        <v-icon class="mr-2">
                            mdi-content-save
                        </v-icon>
                        Save
                    </v-btn>
                </div>
            </div>
        </v-card>
    </div>
</template>
<script>
import { cloneDeep } from 'lodash'
export default {
    props: {
        event: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            temp: cloneDeep(this.event)
        }
    },
    methods: {
        edit() {
            this.temp.editing = true
        },
        createEvent() {
            this.$store.dispatch('eventsPost', this.temp)
        },
        save() {
            this.temp.editing = false

            if (this.temp.new) this.createEvent()

            this.temp.new = false
        }
    }
}
</script>