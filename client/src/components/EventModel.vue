<template>
    <div>
        <v-card>
            <div class="d-flex flex-column pa-8">
                <div class="d-flex flex-row justify-space-between align-center">
                    <div class="d-flex flex-row" style="width:100%">
                        <div class="mr-8" style="max-width:200px;">
                            <div v-if="editing">
                                <v-text-field v-model="temp.title" color="primary"
                                    label="Event Title" />
                            </div>
                            <div v-else>
                                <div class="mb-2">
                                    <b>Event Title</b>
                                </div>
                                <div>
                                    {{ temp.title }}
                                </div>
                            </div>
                        </div>
                        <div style="width:100%; max-width:600px;">
                            <div v-if="editing">
                                <v-text-field v-model="temp.description" color="primary"
                                    label="Event Description" />
                            </div>
                            <div v-else>
                                <div class="mb-2">
                                    <b>Event Description</b>
                                </div>
                                <div>
                                    {{ temp.description }}
                                </div>
                            </div>
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
                <div class="mt-8 mb-4">
                    <div v-for="(reminder, i) in event.reminders" :key="i" class="my-2">
                        <div class="mb-2 grey--text text--darken-2">
                            Reminder #{{i + 1}}
                        </div>
                        <div class="d-flex">
                            <div class="mr-4">
                                <v-menu v-model="event.dateMenu"
                                    :close-on-content-click="false"
                                    transition="scale-transition" right offset-y
                                    max-width="290px" min-width="auto">
                                    <template v-slot:activator="{ on, attrs }">
                                        <div style="width:200px;">
                                            <v-text-field
                                                :value="formattedDate(event.date)"
                                                label="Date" prepend-icon="mdi-calendar"
                                                hide-details readonly outlined dense
                                                color="primary" v-bind="attrs"
                                                v-on="on" />
                                        </div>
                                    </template>
                                    <v-date-picker v-model="event.date" no-title
                                        color="primary" @input="event.dateMenu = false" />
                                </v-menu>
                            </div>
                            <div style="width:400px;">
                                <v-autocomplete v-model="event.times"
                                    :items="availableTimes" outlined dense chips
                                    small-chips label="Time(s)" multiple>
                                </v-autocomplete>
                            </div>
                        </div>
                    </div>
                    <v-btn v-if="editing" @click="addReminder" class="mt-8"
                        color="primary" small>
                        <v-icon small>
                            mdi-plus
                        </v-icon>
                        Add Reminder
                    </v-btn>
                </div>
                <div v-if="editing" class="text-right d-flex justify-end">
                    <v-btn @click="cancel" color="grey lighten-1" class="mr-4"
                        :loading="loading" :disabled="loading" small>
                        Cancel
                    </v-btn>
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
    computed: {
        availableTimes() {
            let times = []
            for (let i = 1; i <= 24; i++) {
                times.push(`${i % 12 || 12}:00 ${i < 13 ? 'AM' : 'PM'}`)
            }
            return times
        }
    },
    methods: {
        addReminder() {
            this.event.reminders.push(this.$store.getters.newReminder)
        },
        cancel() {
            this.temp = cloneDeep(this.event)

            this.editing = false

            if (this.event.new) this.$emit('cancel')
        },
        edit() {
            this.editing = true
        },
        formattedDate(date) {
            if (!date) return null
            const [year, month, day] = date.split('-')
            return `${month}/${day}/${year}`
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