import Vue from "vue";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";

import * as rules from "vee-validate/dist/rules";
import { messages } from "vee-validate/dist/locale/en.json";


Vue.component("ValidationObserver", ValidationObserver);
Vue.component("ValidationProvider", ValidationProvider);

for (let [ rule, validation ] of Object.entries(rules)) {

    extend(rule, {

        ...validation,
        //@ts-ignore
        message: messages[rule]
    });
}
