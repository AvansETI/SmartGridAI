import Vue from "vue";
import VueApollo from "vue-apollo";

import config from "@/config";

import { ApolloClient, InMemoryCache, ApolloLink, createHttpLink } from "@apollo/client/core";


Vue.use(VueApollo);

const links: ApolloLink[] = [];

const httpOptions = {

    uri: `${ config.api.url }${ config.api.gqlEndpoint }`
};

function linkReducer(acc: any, link: ApolloLink) {

    if (acc == null) {

        return link;
    }

    return acc.concat(link);
}

export const apolloClient = new ApolloClient({

    link: (

        [
            ...links,
            createHttpLink(httpOptions)
        ]
        .reduce(linkReducer, null)
    ),

    cache: new InMemoryCache()
});

export const apolloProvider = new VueApollo({

    defaultClient: apolloClient
});
