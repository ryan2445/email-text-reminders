<template>
    <div>
        <div class="d-flex mb-8">
            <div class="text-h6">
                Account Settings
            </div>
        </div>
        <div class="d-flex flex-column" style="max-width:300px;">
            <div class="d-flex">
                <div class="mr-4">
                    <v-text-field v-model="temp.firstname" label="First Name"
                        color="primary" />
                </div>
                <div>
                    <v-text-field v-model="temp.lastname" label="Last Name"
                        color="primary" />
                </div>
            </div>
            <div>
                <v-text-field v-model="temp.email" color="primary" label="Email" />
            </div>
            <div>
                <v-text-field v-model="temp.phone" color="primary" label="Phone Number" />
            </div>
            <div class="d-flex justify-space-between mt-4">
                <div>
                    <v-btn color="grey lighten-1" :disabled="!changed" small>
                        Cancel
                    </v-btn>
                </div>
                <div>
                    <v-btn color="primary" small>
                        Save
                    </v-btn>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { cloneDeep, isEqual } from 'lodash'
export default {
    data() {
        return {
            temp: {
                email: '',
                firstname: '',
                lastname: '',
                phone: ''
            }
        }
    },
    async mounted() {
        if (!this.userProfile) {
            this.temp = cloneDeep(await this.$store.dispatch('usersGet'))
        } else {
            this.temp = this.userProfile
        }
    },
    computed: {
        ...mapGetters(['userProfile']),
        changed() {
            return !isEqual(this.temp, this.userProfile)
        }
    },
    methods: {}
}
</script>