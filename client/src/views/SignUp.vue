<template>
    <div class="d-lg-flex">
        <div :style="{minWidth: $vuetify.breakpoint.lgAndUp ? '400px' : '100%'}">
            <v-stepper v-model="step" style="height:100%;">
                <v-stepper-content step="1">
                    <v-card class="elevation-12">
                        <v-card-text>
                            <div class="mb-8 font-weight-bold text-h5">
                                Sign Up
                            </div>
                            <validation-observer v-slot="{ handleSubmit }">
                                <v-form @submit.prevent="handleSubmit(signUp)"
                                    id="signUp">
                                    <validation-provider name="Username"
                                        rules="required|email" v-slot="{ errors }">
                                        <v-text-field v-model="username"
                                            prepend-icon="mdi-account" label="Username"
                                            type="email" :error-messages="errors" />
                                    </validation-provider>
                                    <validation-provider name="Password"
                                        rules="required|min:8|max:99" v-slot="{ errors }">
                                        <v-text-field v-model="password"
                                            prepend-icon="mdi-lock" label="Password"
                                            type="password" :error-messages="errors" />
                                    </validation-provider>
                                </v-form>
                            </validation-observer>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn type="submit" form="signUp" color="primary"
                                :loading="loading" :disabled="loading">
                                Sign Up
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-stepper-content>
                <v-stepper-content step="2">
                    <v-card class="elevation-12 pa-4">
                        <v-card-text>
                            <div class="mb-8 font-weight-bold text-h5">
                                Enter your 6-digit verification code
                            </div>
                            <validation-observer v-slot="{ handleSubmit }">
                                <v-form @submit.prevent="handleSubmit(signUpConfirm)"
                                    id="signUpConfirm">
                                    <validation-provider name="Verification Code"
                                        rules="required|digits:6" v-slot="{ errors }">
                                        <v-text-field v-model="code"
                                            prepend-icon="mdi-pound"
                                            label="Verification Code"
                                            :error-messages="errors" />
                                    </validation-provider>
                                </v-form>
                            </validation-observer>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn type="submit" form="signUpConfirm" color="primary"
                                :loading="loading" :disabled="loading">
                                Verify
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-stepper-content>
            </v-stepper>
        </div>
        <div class="d-lg-flex d-none">
            <img src="@/assets/images/mountains_snow.jpg" />
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            username: null,
            password: null,
            code: null,
            step: 1,
            loading: null
        }
    },
    methods: {
        async signUp() {
            this.loading = true

            const cognito = await this.$store.dispatch('signUp', {
                username: this.username,
                password: this.password
            })

            this.loading = false

            if (!cognito) return

            this.step = 2
        },
        async signUpConfirm() {
            this.loading = true

            const cognito = await this.$store.dispatch('signUpConfirm', {
                username: this.username,
                code: this.code
            })

            this.loading = false

            if (!cognito) return

            this.loading = true

            const cognito2 = await this.$store.dispatch('signIn', {
                username: this.username,
                password: this.password
            })

            this.loading = false

            if (!cognito2) return

            this.$store.commit('tokenSet', cognito2.response.AuthenticationResult)

            this.$router.push('/home')
        }
    }
}
</script>
