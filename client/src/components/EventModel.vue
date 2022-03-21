<template>
    <div>
        <v-card>
            <div class="d-flex flex-column pa-8">
                <div class="d-flex flex-row justify-space-between align-center">
                    <div class="d-flex flex-row" style="width:100%">
                        <div class="mr-8" style="max-width:200px;">
                            <span v-if="editing">
                                <v-text-field v-model="temp.title" color="primary"
                                    label="Event Title" />
                            </span>
                            <span v-else>
                                {{ temp.title }}
                            </span>
                        </div>
                        <div style="width:100%; max-width:600px;">
                            <span v-if="editing">
                                <v-text-field v-model="temp.description" color="primary"
                                    label="Event Description" />
                            </span>
                            <span v-else>
                                {{ temp.description }}
                            </span>
                        </div>
                    </div>
                    <div class="text-right" style="width:100px;">
                        <v-btn v-if="!editing" @click="edit" icon color="primary">
                            <v-icon>
                                mdi-pencil
                            </v-icon>
                        </v-btn>
                    </div>
                    <div class="text-right" style="width:100px;">
                        <v-btn v-if="!editing" @click="deleteEvent" icon
                            color="red lighten-2">
                            <v-icon>
                                mdi-delete
                            </v-icon>
                        </v-btn>
                    </div>
                </div>
                <div v-if="editing" class="text-right">
                    <v-btn @click="save" color="primary" :loading="loading"
                        :disabled="loading" small>
                        <v-icon class="mr-2" small>
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
            editing: false,
            loading: false,
            temp: cloneDeep(this.event)
        }
    },
    mounted() {
        if (this.event.new) this.editing = true
    },
    methods: {
        edit() {
            this.editing = true
        },
        save() {
            if (this.temp.new) {
                return this.createEvent()
            }

            return this.saveEvent()
        },
        async createEvent() {
            this.loading = true

            const response = await this.$store.dispatch('eventsPost', this.temp)

            this.loading = false

            this.temp.uuid = response.event_id

            this.temp.new = false

            this.editing = false
        },
        async saveEvent() {
            this.loading = true

            await this.$store.dispatch('eventsPut', this.temp)

            this.loading = false

            this.editing = false
        },
        async deleteEvent() {
            this.loading = true

            await this.$store.dispatch('eventsDelete', this.temp)

            this.loading = false

            this.$emit('delete', this.temp.uuid)
        }
    }
}
</script>