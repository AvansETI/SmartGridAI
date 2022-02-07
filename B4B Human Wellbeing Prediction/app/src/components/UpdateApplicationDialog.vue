<template>
    <v-dialog v-model="showDialog" persistent max-width="400px">
        <v-card>
            <v-card-title class="text-h5">Update Available</v-card-title>
            <v-card-text>The <span class="primary--text">Brains for Buildings Satisfaction Predictor</span> has an update available, please press the "Update now" button below.</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    @click="refresh"
                    :disabled="refreshing"
                    :loading="refreshing"
                >
                    Update Now
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";


@Component({

    name: "UpdateApplicationDialog"
})
export default class UpdateApplicationDialog extends Vue {

    data() {

        return {

            showDialog: false,

            registration: null,
            refreshing: false,
        };
    }

    created() {

        this.$eventBus.$on("pwa-update-required", (registration) => {

            this.showDialog = true;
            this.registration = registration;
        });
    }

    refresh() {

        if (!this.registration || !this.registration.waiting) {

            return;
        }

        this.registration.waiting.postMessage({ type: 'SKIP_WAITING' });
        this.refreshing = true;

        window.location.reload();
    }
}
</script>

<style lang="less" scoped>

</style>
