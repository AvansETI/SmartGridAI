import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

//Page
import IndexPage from "../pages/IndexPage.vue";


Vue.use(VueRouter);

const routes: Array<RouteConfig> = [

    {
        path: "/",
        name: "index",
        component: IndexPage
    },

    {
        path: "/about",
        name: "About",
        component: () => import(/* webpackChunkName: "about" */ "../pages/AboutPage.vue")
    }
];

const router = new VueRouter({

    mode: "history",
    base: process.env.BASE_URL,
    routes
});

export default router;
