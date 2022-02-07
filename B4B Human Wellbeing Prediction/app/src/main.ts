import Vue from "vue";
import AppLayout from "@/layouts/AppLayout.vue";

// PWA
import "@/registerServiceWorker";

// Plugins
import "@/plugins/vuera";
import "@/plugins/vee-validate";
import vuetify from "@/plugins/vuetify";
import { apolloProvider } from "@/plugins/apollo";
import router from "@/router";

// Globals
import { EventBus } from "@/event-bus";
Vue.prototype.$eventBus = EventBus;


new Vue({

    router,
    vuetify,

    apolloProvider,

    render: h => h(AppLayout)
})
.$mount("#app");
