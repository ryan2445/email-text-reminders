<template>
    <v-app id="app">
        <app-bar v-if="user" />
        <nav-drawer v-if="user" />
        <template v-for="(dialog, i) in dialogs">
            <component-dialog :key="`dialog${i}`" :params="dialog" />
        </template>
        <v-main style="background-color:lightgrey;">
            <div class="ma-8">
                <router-view />
            </div>
        </v-main>
    </v-app>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
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
