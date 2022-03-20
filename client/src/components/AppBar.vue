<template>
    <v-app-bar color="primary" class="white--text" app clipped-left flat>
        <v-app-bar-nav-icon>
            <v-icon color="white">mdi-menu</v-icon>
        </v-app-bar-nav-icon>
        <v-toolbar-title>Toolbar Title</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu left offset-y>
            <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on">
                    <v-icon color="white">mdi-dots-vertical</v-icon>
                </v-btn>
            </template>
            <v-list class="pa-4">
                <v-list-item v-for="(item, i) in items" :key="i"
                    @click="handleClick(item.method)">
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
export default {
    data() {
        return {
            items: [
                {
                    title: 'Sign Out',
                    icon: 'mdi-exit-to-app',
                    method: 'signOut'
                }
            ]
        }
    },
    methods: {
        handleClick(method) {
            return this[method]()
        },
        signOut() {
            console.log('signOut')
        }
    }
}
</script>