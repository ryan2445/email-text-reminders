<template>
    <div>
        <v-card>
            <div class="d-flex flex-column pa-lg-8 pa-4">
                <div class="d-flex flex-row justify-space-between align-center">
                    <div class="d-flex flex-lg-row flex-column" style="width:100%">
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
                    <div class="text-right" style="width:50px;">
                        <v-btn v-if="!editing" @click="editing = true" icon
                            color="primary">
                            <v-icon>
                                mdi-pencil
                            </v-icon>
                        </v-btn>
                    </div>
                    <div class="text-right" style="width:50px;">
                        <v-btn v-if="!editing" @click="deleteEvent" icon
                            color="red lighten-2">
                            <v-icon>
                                mdi-delete
                            </v-icon>
                        </v-btn>
                    </div>
                </div>
                <div class="mt-4">
                    <div class="d-flex">
                        <div class="mr-4">
                            <v-checkbox v-model="temp.sendEmail" label="Send Email"
                                color="primary" :disabled="!editing" />
                        </div>
                        <div>
                            <v-checkbox v-model="temp.sendSms" label="Send SMS"
                                color="primary" :disabled="!editing" />
                        </div>
                    </div>
                </div>
                <div class="mt-8 mb-4">
                    <div class="d-flex flex-lg-row flex-column">
                        <div class="mr-4" style="max-width:500px;">
                            <v-menu ref="menu" v-model="temp.dateMenu"
                                :close-on-content-click="false"
                                transition="scale-transition" offset-y min-width="auto">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-combobox v-model="formattedDate" multiple chips
                                        small-chips label="Date(s)" outlined dense
                                        prepend-inner-icon="mdi-calendar" readonly
                                        :disabled="!editing" clearable v-bind="attrs"
                                        v-on="on">
                                    </v-combobox>
                                </template>
                                <v-date-picker v-model="temp.dates" multiple no-title
                                    scrollable color="primary">
                                    <v-spacer></v-spacer>
                                    <v-btn text color="primary"
                                        @click="temp.dateMenu = false">
                                        Cancel
                                    </v-btn>
                                    <v-btn text color="primary"
                                        @click="saveDates(temp.dates)">
                                        OK
                                    </v-btn>
                                </v-date-picker>
                            </v-menu>
                        </div>
                        <div style="max-width:500px;">
                            <v-autocomplete v-model="temp.times" @change="checkTimeLimit"
                                clearable :items="availableTimes" outlined dense chips
                                small-chips label="Time(s)" multiple :disabled="!editing"
                                prepend-inner-icon="mdi-clock">
                            </v-autocomplete>
                        </div>
                    </div>
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
                times.push(
                    `${i % 12 || 12}:00 ${i < 13 ? 'AM' : 'PM'}`,
                    `${i % 12 || 12}:30 ${i < 13 ? 'AM' : 'PM'}`
                )
            }
            return times
        },
        formattedDate: {
            set(value) {
                this.temp.dates = value
            },
            get() {
                if (!this.temp || !this.temp.dates) return null

                return this.temp.dates.map((date) => {
                    const [year, month, day] = date.split('-')
                    return `${month}/${day}/${year}`
                })
            }
        }
    },
    methods: {
        checkTimeLimit() {
            if (this.temp.times.length > 4) this.temp.times.pop()
        },
        saveDates(dates) {
            this.temp.dates = dates

            this.temp.dateMenu = false
        },
        cancel() {
            this.temp = cloneDeep(this.event)

            this.editing = false

            if (this.temp.new) this.$emit('cancel')
        },
        save() {
            if (this.temp.new) return this.createEvent()

            return this.saveEvent()
        },
        async createEvent() {
            this.loading = true

            const response = await this.$store.dispatch('eventsPost', this.temp)

            this.loading = false

            if (!response) return

            this.temp.uuid = response.event_id

            this.temp.new = false

            this.editing = false

            Object.assign(this.event, this.temp)
        },
        async saveEvent() {
            this.loading = true

            await this.$store.dispatch('eventsPut', this.temp)

            this.loading = false

            this.editing = false

            Object.assign(this.event, this.temp)
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