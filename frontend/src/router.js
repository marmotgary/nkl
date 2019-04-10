import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/info',
            name: 'info',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function() {
                return import(/* webpackChunkName: "info" */ './views/Info.vue');
            }
        },
        {
            path: '/ottelut',
            name: 'ottelut',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function() {
                return import(/* webpackChunkName: "ottelut" */ './views/OttelutView.vue');
            }
        },
        {
            path: '/ottelu/(.*)',
            name: 'ottelu',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function() {
                return import(/* webpackChunkName: "ottelut" */ './views/SingleOtteluView.vue');
            }
        },
        {
            path: '/joukkueet',
            name: 'joukkueet',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function() {
                return import(/* webpackChunkName: "joukkueet" */ './views/Joukkueet.vue');
            }
        },
        {
            path: '/pelaajat',
            name: 'pelaajat',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: function() {
                return import(/* webpackChunkName: "pelaajat" */ './views/PelaajatView.vue');
            }
        }
    ]
});
