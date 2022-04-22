<template>
    <v-app id="app">
        <app-bar v-if="user" @min="navDrawerIsMin = $event" />
        <nav-drawer v-if="user" :isMin="navDrawerIsMin" />
        <template v-for="(dialog, i) in dialogs">
            <component-dialog :key="`dialog${i}`" :params="dialog" />
        </template>
        <v-main style="background-color: lightgrey">
            <div :style="user && 'max-width:1440px; margin:auto;'">
                <router-view />
            </div>
        </v-main>
    </v-app>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            navDrawerIsMin: false
        }
    },
    computed: {
        ...mapGetters(['dialogs', 'user'])
    }
}
</script>
<style>
* {
    text-transform: none;
}
::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}
::-webkit-scrollbar-thumb {
    background: gray;
}
::-webkit-scrollbar-track {
    background: lightgray;
}
</style>
