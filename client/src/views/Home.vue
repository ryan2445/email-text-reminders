<template>
    <div class="d-flex justify-center ma-lg-8 ma-4">
        <div :style="$vuetify.breakpoint.smAndDown ? 'width:100%' : 'min-width:1000px;'">
            <div class="d-flex flex-row justify-space-between mb-8">
                <div style="font-size:30px; font-family:'Libre Bodini'; font-weight:700;">
                    Events List
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
            <div v-if="events" class="">
                <div v-for="(event, i) in events" :key="i">
                    <event-model :event="event" @cancel="events.pop()"
                        @delete="deleteEvent($event)" class="my-4" />
                </div>
            </div>
            <div v-else>
                <v-progress-circular indeterminate color="primary" />
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
            this.events.splice(
                this.events.findIndex((event) => event.uuid == uuid),
                1
            )
        }
    }
}
</script>
