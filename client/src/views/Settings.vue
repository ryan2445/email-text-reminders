<template>
    <div class="d-flex justify-center ma-lg-8 ma-4">
        <v-card v-if="userProfile" class="pa-10">
            <div class="text-center mb-8"
                style="font-size:30px; font-family:'Playfair Display', serif; font-weight:700;">
                Account Settings
            </div>
            <div class="d-flex flex-column" style="max-width: 300px">
                <div class="d-flex">
                    <div class="mr-4" style="flex:1;">
                        <v-text-field v-model="temp.firstname" label="First Name"
                            color="primary" />
                    </div>
                    <div style="flex:1;">
                        <v-text-field v-model="temp.lastname" label="Last Name"
                            color="primary" />
                    </div>
                </div>
                <div>
                    <v-text-field v-model="temp.email" color="primary" label="Email" />
                </div>
                <div>
                    <v-text-field v-model="temp.phone" v-mask="'(###) ###-####'"
                        color="primary" label="Phone Number" />
                </div>
                <div class="d-flex justify-end mt-4">
                    <div class="mx-2">
                        <v-btn @click="cancel" :disabled="!changed" small text>
                            Cancel
                        </v-btn>
                    </div>
                    <div class="mx-2">
                        <v-btn @click="save" color="primary" :disabled="loading"
                            :loading="loading" small>
                            Save
                        </v-btn>
                    </div>
                </div>
            </div>
        </v-card>
        <div v-else>
            <v-progress-circular indeterminate color="primary" />
        </div>
        <v-snackbar v-model="snackbar" color="primary">
            <v-icon>mdi-check</v-icon> Account settings saved!
        </v-snackbar>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { cloneDeep } from 'lodash'
export default {
    data() {
        return {
            loading: false,
            temp: {
                email: '',
                firstname: '',
                lastname: '',
                phone: ''
            },
            snackbar: false
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
            if (!this.userProfile) return null

            const keys = Object.keys(this.temp)

            for (const key of keys) {
                if (this.temp[key] != this.userProfile[key]) {
                    return true
                }
            }

            return false
        }
    },
    methods: {
        cancel() {
            this.temp = this.userProfile
        },
        async save() {
            this.loading = true

            await this.$store.dispatch('usersPut', this.temp)

            this.$store.commit('userProfileSet', this.temp)

            this.loading = false

            this.snackbar = true
        }
    }
}
</script>
