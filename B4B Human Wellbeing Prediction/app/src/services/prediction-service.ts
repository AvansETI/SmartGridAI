import { ApolloClient } from "@apollo/client/core";

//Queries
//@ts-ignore: .gql file has no types...
import PredictQuery from "@/gql/queries/PredictQuery.gql";


export class PredictionService {

    private apolloClient: ApolloClient<any>;

    constructor(apolloClient: ApolloClient<any>) {

        this.apolloClient = apolloClient;
    }

    //@ts-ignore
    async predict({ input }): Promise<number> {

        return (

            await this.apolloClient.query({

                query: PredictQuery,
                variables: {

                    input
                }
            })
        )
        .data?.predict || 0
    }
}
