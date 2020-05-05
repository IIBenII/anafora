import Vue from "vue";
import VueRouter from "vue-router";
import Datasets from "../views/Datasets.vue";
import Tables from "../views/Tables.vue";
import Search from "../views/Search.vue";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
    {
        path: "/datasets",
        name: "Datasets",
        component: Datasets
    },
    {
        path: "/tables",
        name: "Tables",
        component: Tables
    },
    {
        path: "/",
        name: "Home",
        component: Home
    },
    {
        path: "/search",
        name: "Search",
        component: Search
    },
    {
        path: "/about",
        name: "About",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ "../views/About.vue")
    }
    ,
    {
        path: "/build",
        name: "Build",
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import(/* webpackChunkName: "about" */ "../views/Build.vue")
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes
});

export default router;
