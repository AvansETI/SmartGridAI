<template>
    <v-app>
        <v-app-bar app color="primary" dark>
            <v-app-bar-title>
                <router-link :to="{ name: 'index' }" class="white--text text-decoration-none">B4BUX</router-link>
            </v-app-bar-title>
        </v-app-bar>

        <v-main>
            <v-fade-transition mode="out-in">
                <router-view :key="`app-layout-${ $route.path }`"></router-view>
            </v-fade-transition>
        </v-main>

        <UpdateApplicationDialog></UpdateApplicationDialog>
    </v-app>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";
import UpdateApplicationDialog from "@/components/UpdateApplicationDialog.vue";


@Component({

    name: "AppLayout",
    components: { UpdateApplicationDialog }
})
export default class AppLayout extends Vue {

    data() {

        return {};
    }
}
</script>

<style lang="less">

* {

    user-select: none;
}

html, html body, html body #app {

    //Nasty importants are needed to overwrite vuetify...

    margin: 0!important;
    padding: 0!important;

    width: 100vw!important;
    min-width: 100vw!important;
    max-width: 100vw!important;

    height: 100vh!important;
    min-height: 100vh!important;
    max-height: 100vh!important;

    overflow-x: hidden!important;
    overflow-y: auto!important;
}

.fill-width {

    width: 100%;
}

.page {

    padding: 2.5%;

    width: 100%;
    min-width: 100%;
    max-width: 100%;

    height: 100%;
    min-height: 100%;

    overflow-x: hidden;
    overflow-y: auto;
}

</style>
