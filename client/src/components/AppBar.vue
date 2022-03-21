<template>
    <v-app-bar color="primary" class="white--text" app clipped-left flat>
        <v-app-bar-nav-icon>
            <v-icon color="white">mdi-menu</v-icon>
        </v-app-bar-nav-icon>
        <v-toolbar-title>{{ user }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu left offset-y :loading="loading">
            <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                    <v-icon color="white">mdi-dots-vertical</v-icon>
                </v-btn>
            </template>
            <v-list class="pa-2">
                <v-list-item v-for="(item, i) in items" :key="i"
                    @click="handleClick(item.method)" color="primary">
                    <v-list-item-icon>
                        <v-icon>{{ item.icon }}</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            loading: false,
            items: [
                {
                    title: 'Sign Out',
                    icon: 'mdi-exit-to-app',
                    method: 'signOut'
                }
            ]
        }
    },
    computed: {
        ...mapGetters(['user'])
    },
    methods: {
        handleClick(method) {
            return this[method]()
        },
        async signOut() {
            this.loading = true

            const cognito = await this.$store.dispatch('signOut', {
                accessToken: localStorage.AccessToken
            })

            this.loading = false

            if (!cognito) return

            this.$router.push('/signin')
        }
    }
}
</script>