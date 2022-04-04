<template>
    <div>
        <div class="d-flex mb-8">
            <div class="text-h6">
                Account Settings
            </div>
        </div>
        <div class="">
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { cloneDeep } from 'lodash'
export default {
    data() {
        return {
            temp: null,
            user: null
        }
    },
    async mounted() {
        // this.user = await this.$store.dispatch('usersGet')
    },
    computed: {},
    methods: {}
}
</script>