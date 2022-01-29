import '@babel/polyfill';
import "vuetify/dist/vuetify.min.css";
import Vue from 'vue';
import Vuetify from 'vuetify';
import App from './App.vue';
import router from './router';
import VueResource from 'vue-resource';
import VueSession from 'vue-session';
import VueMoment from 'vue-moment';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.config.productionTip = false;

export const eventBus = new Vue();

Vue.use(VueResource);
Vue.use(VueSession);
Vue.use(VueMoment);
Vue.use(Vuetify);

 Vue.http.options.root = 'https://kyykka.com'
//Vue.http.options.root = 'http://localhost:8000'

Vue.mixin({
    methods: {
        getCookie: function (name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }
})

new Vue({
    vuetify: new Vuetify(),
    router,
    render: function (h) {
        return h(App);
    }
}).$mount('#app');
