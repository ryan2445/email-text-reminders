<template>
    <div class="d-flex">
        <div style="width:600px;">
            <v-card class="elevation-12 pa-4">
                <v-card-text>
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
                        Log In
                    </v-btn>
                </v-card-actions>
            </v-card>
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

            this.$store.commit('tokenSet', cognito.response.AuthenticationResult)
        }
    }
}
</script>
