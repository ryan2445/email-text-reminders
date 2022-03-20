<template>
    <div>
        <v-dialog v-model="dialog" width="600" persistent>
            <v-card>
                <div class="pa-4 d-flex flex-column">
                    <div class="text-right">
                        <v-btn icon large @click="close">
                            <v-icon large>
                                mdi-close
                            </v-icon>
                        </v-btn>
                    </div>
                    <div>
                        <component :is="params.component" v-bind="params.props" />
                    </div>
                </div>
            </v-card>
        </v-dialog>
    </div>
</template>
<script>
export default {
    props: {
        params: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            dialog: true
        }
    },
    methods: {
        close() {
            this.$store.dispatch('dialogClose')
        },
        submit(data) {
            if (this.params.callback) this.params.callback(data)

            if (this.params.closeOnSubmit) this.close()
        }
    }
}
</script>