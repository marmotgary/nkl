import '@babel/polyfill';
import Vue from 'vue';
import './plugins/vuetify';
import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;

export const eventBus = new Vue();

import VueResource from 'vue-resource';
import VueSession from 'vue-session';
import VueMoment from 'vue-moment';

Vue.use(VueResource);
Vue.use(VueSession);
Vue.use(VueMoment);

// Vue.http.options.root = 'https://kyykka.com'
Vue.http.options.root = 'http://localhost:8000'

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
    router,
    render: function (h) {
        return h(App);
    }
}).$mount('#app');
