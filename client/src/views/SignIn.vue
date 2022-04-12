<template>
    <div class="d-lg-flex">
        <div :style="{minWidth: $vuetify.breakpoint.lgAndUp ? '400px' : '100%'}">
            <v-card class="elevation-12 pa-4" style="height:100%;">
                <v-card-text>
                    <div class="mb-8 font-weight-bold text-h5">
                        Sign In
                    </div>
                    <validation-observer v-slot="{ handleSubmit }">
                        <v-form @submit.prevent="handleSubmit(signIn)" id="signIn">
                            <validation-provider name="Username" rules="required|email"
                                v-slot="{ errors }">
                                <v-text-field v-model="username"
                                    prepend-icon="mdi-account" label="Username"
                                    type="email" :error-messages="errors" />
                            </validation-provider>
                            <validation-provider name="Password"
                                rules="required|min:8|max:99" v-slot="{ errors }">
                                <v-text-field v-model="password" prepend-icon="mdi-lock"
                                    label="Password" type="password"
                                    :error-messages="errors" />
                            </validation-provider>
                        </v-form>
                    </validation-observer>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn type="submit" form="signIn" color="primary" :loading="loading"
                        :disabled="loading">
                        Sign In
                    </v-btn>
                </v-card-actions>
            </v-card>
        </div>
        <div class="d-lg-flex d-none">
            <img src="@/assets/images/mountains_sunset.jpg" style="height:100vh;" />
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            username: null,
            password: null,
            loading: null
        }
    },
    methods: {
        async signIn() {
            this.loading = true

            const cognito = await this.$store.dispatch('signIn', {
                username: this.username,
                password: this.password
            })

            this.loading = false

            if (!cognito) return

            this.$store.commit('tokenSet', cognito.AuthenticationResult)

            this.$router.push('/home')
        }
    }
}
</script>
