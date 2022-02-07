//@ts-ignore
import merge from "lodash.merge";

import shared from "@/config/shared";
import development from "@/config/env/development";
import production from "@/config/env/production";


const config = merge(

    {
        ...shared
    },

    (
        () => {

            switch (process.env.NODE_ENV) {

                case "development":
                    return development;

                default:
                case "production":
                    return production;
            }
        }
    )
    ()
);

export default config;
