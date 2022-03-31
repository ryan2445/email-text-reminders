<template>
    <div>
        <div class="d-flex flex-row justify-space-between mb-8">
            <div class="text-h6">
                Current Events
            </div>
            <div>
                <v-btn @click="addEvent" color="primary">
                    <v-icon class="mr-2">
                        mdi-calendar-plus
                    </v-icon>
                    Add Event
                </v-btn>
            </div>
        </div>
        <div class="">
            <div v-for="(event, i) in events" :key="i">
                <event-model :event="event" @cancel="events.pop()"
                    @delete="deleteEvent($event)" class="my-4" />
            </div>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            events: []
        }
    },
    async mounted() {
        const response = await this.$store.dispatch('eventsGet')

        this.events = response.items
    },
    methods: {
        addEvent() {
            this.events.push(this.$store.getters.newEvent)
        },
        deleteEvent(uuid) {
            this.events.pop(this.events.findIndex((event) => event.uuid == uuid))
        }
    }
}
</script>