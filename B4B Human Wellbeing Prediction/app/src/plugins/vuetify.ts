import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import colors from "vuetify/lib/util/colors";


Vue.use(Vuetify);

export default new Vuetify({

    theme: {

        themes: {

            light: {

                primary: "#36805C",
                secondary: "#70C1B3",
                accent: "#70C1B3"
            },

            dark: {

                primary: "#36805C",
                secondary: "#70C1B3",
                accent: "#70C1B3"
            }
        }
    }
});
