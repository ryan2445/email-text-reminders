<template>
    <div>
        <div class="d-flex flex-row justify-space-between">
            <div class="text-h6">
                Current Reminders
            </div>
            <div>
                <v-btn color="primary">
                    <v-icon class="mr-2">
                        mdi-plus
                    </v-icon>
                    Add Reminder
                </v-btn>
            </div>
        </div>
        <div>
            <div v-for="(event, i) in events" :key="i">
                event
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {}
    },
    mounted() {
        this.$store.dispatch('eventsGet')
    },
    computed: {
        ...mapGetters(['events'])
    }
}
</script>