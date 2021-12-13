<template>
    <div class="index page">
        <div class="page-title fill-width mb-12">
            <div class="page-title-inner fill-width fill-height d-flex flex-column align-center">
                <h2 class="display-1 mb-3 text-center">Brains For Buildings - Satisfaction Predictor</h2>
                <p class="text-center">This application can be used to predict whether or not the occupants of a room would be comfortable in it's climate.</p>
            </div>
        </div>

        <v-row align="center" justify="center">
            <v-col cols="12" md="6">
                <v-stepper v-model.number="step">
                    <v-stepper-items>
                        <v-stepper-content :step="0">
                            <v-card>
                                <v-card-text>
                                    <ValidationObserver ref="validationObserver" v-slot="{ handleSubmit }" class="login-form-holder">
                                        <v-form @submit.prevent="handleSubmit(predict)">

                                            <ValidationProvider
                                                vid="number_of_occupants" name="number_of_occupants"
                                                rules="required|integer|min_value:1" v-slot="{ errors }"
                                            >
                                                <v-text-field name="number_of_occupants" label="Number of Occupants" type="number" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.number_of_occupants" :error-messages="errors"></v-text-field>
                                            </ValidationProvider>

                                            <ValidationProvider
                                                vid="activity_of_occupants" name="activity_of_occupants"
                                                rules="required|integer" v-slot="{ errors }"
                                            >
                                                <v-select name="activity_of_occupants" label="What will the occupants be doing?" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.activity_of_occupants" :items="activityOfOccupantsItems" :error-messages="errors"></v-select>
                                            </ValidationProvider>

                                            <div class="d-flex justify-end">
                                                <v-btn :disabled="shouldDisable" :loading="predicting" color="primary" type="submit">Predict</v-btn>
                                            </div>

                                        </v-form>
                                    </ValidationObserver>
                                </v-card-text>
                            </v-card>
                        </v-stepper-content>

                        <v-stepper-content :step="1">
                            <v-card>
                                <v-card-title class="justify-center align-center flex-column mb-7">
                                    <v-icon v-if="prediction >= satisfied" :size="70" class="mb-4" :class="predictionDisplayClass">mdi-emoticon-excited-outline</v-icon>
                                    <v-icon v-else :size="70" class="mb-4" :class="predictionDisplayClass">mdi-emoticon-sad-outline</v-icon>

                                    <span class="text-h4" v-if="predictionInput.activity_of_occupants != 0">
                                        The {{ predictionInput.number_of_occupants }} {{ activityOfOccupantsItems.find(ao => ao.value === predictionInput.activity_of_occupants).text.toLowerCase() }} <span :class="predictionDisplayClass">{{ prediction >= satisfied ? "comfortably" : "uncomfortably" }}</span>.
                                    </span>
                                    <span class="text-h4" v-else>
                                        The {{ predictionInput.number_of_occupants }} occupant(s) will be <span :class="predictionDisplayClass">{{ prediction >= satisfied ? "comfortable" : "uncomfortable" }}</span>.
                                    </span>
                                </v-card-title>
                                <v-card-text class="d-flex align-center justify-center">
                                    <v-btn :disabled="shouldDisable" color="primary" type="submit" @click="reset">Make another prediction</v-btn>
                                </v-card-text>
                            </v-card>
                        </v-stepper-content>
                    </v-stepper-items>
                </v-stepper>

                <v-expand-transition>
                    <div class="explain" v-if="prediction != null">
                        <v-divider class="my-7"></v-divider>

                        <div class="mb-5">
                            <h3 class="text-h6 mb-2">Why will they be {{ prediction >= satisfied ? "comfortable" : "uncomfortable" }}?</h3>
                            <div>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur assumenda ea eius in ipsum nulla recusandae! Cum fugiat id laudantium modi molestiae quae reiciendis totam veritatis. Beatae earum omnis possimus.</div>
                            <div>Accusantium quibusdam quidem quod repellat vel veniam vero voluptas. Aliquam debitis iure libero modi nostrum nulla praesentium repudiandae similique! A ab autem consequatur deleniti hic iure, laborum neque nostrum praesentium.</div>
                            <div>Amet assumenda atque autem, blanditiis eaque enim, expedita explicabo fuga itaque labore nemo numquam pariatur praesentium quas quasi, qui quis quos repellendus rerum ut? Expedita nemo possimus quibusdam quis vitae.</div>
                        </div>

<!--                        <AdditiveForceVisualizer></AdditiveForceVisualizer>-->
                        <v-skeleton-loader class="my-5" type="image"></v-skeleton-loader>

                        <div class="mb-5">
                            <div>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut dolor earum est odit porro quae, qui quis ullam! Ab atque, et iure iusto nulla obcaecati porro quia quod ratione recusandae.</div>
                            <div>Accusamus accusantium architecto asperiores blanditiis cupiditate delectus deleniti eaque fugiat in laboriosam maiores nesciunt, numquam officia possimus quibusdam quidem quis quisquam reprehenderit sapiente, soluta suscipit tempore temporibus vel veniam veritatis.</div>
                            <div>Ab dolores excepturi fuga nostrum ut. Alias consectetur cumque deleniti dolorem et ex, facere harum id labore maiores molestiae molestias necessitatibus nesciunt nisi, odit porro quos recusandae reprehenderit similique vel?</div>
                        </div>

                        <div class="mb-5">
                            <h3 class="text-h6 mb-2">Disclaimer</h3>
                            <div>Lorem ipsum dolor sit amet, consectetur adipisicing elit. A alias animi assumenda aut blanditiis cupiditate eaque est, expedita impedit laboriosam laudantium molestias neque non nulla placeat praesentium quia quisquam voluptas.</div>
                            <div>Aliquid animi commodi, debitis deleniti deserunt dignissimos dolorem incidunt ipsam minima mollitia nulla obcaecati, quibusdam quod repudiandae, rerum sed sequi ut. Dolorem dolores ducimus magni nisi odit quam rerum suscipit!</div>
                            <div>Aperiam aut consectetur debitis delectus deleniti dignissimos, dolores doloribus, ea, eos est eum harum hic in inventore ipsam maiores nam nihil non numquam pariatur perferendis quasi quisquam repellendus saepe vel?</div>
                        </div>
                    </div>
                </v-expand-transition>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";

// Services
import { PredictionService } from "@/services/prediction-service";

// Enums
import { OccupantsActivity } from "@/enums/occupants-activity";

// Filters
import { occupantsActivityFilter } from "@/filters/occupants-activity-filter";

// SHAP
import { AdditiveForceVisualizer } from "shapjs";


@Component({

    name: "IndexPage",
    components: { AdditiveForceVisualizer }
})
export default class IndexPage extends Vue {

    data() {

        return {

            step: 0,

            satisfied: 1,

            predicting: false,
            prediction: null,

            predictionInput: {

                number_of_occupants: 1,
                activity_of_occupants: 0,
            }
        };
    }

    created() {

        this.predictionService = new PredictionService(this.$apollo.getClient());
    }

    get shouldDisable() {

        return this.predicting;
    }

    get activityOfOccupantsItems() {

        return Object.values(OccupantsActivity)
            .filter(oa => typeof oa === "number")
            .map
            (
                oa => (

                    {
                        text: occupantsActivityFilter(oa),
                        value: oa
                    }
                )
            )
        ;
    }

    get predictionDisplayClass() {

        return {
            "error--text": (this.prediction < this.satisfied),
            "success--text": (this.prediction >= this.satisfied)
        };
    }

    async predict() {

        this.predicting = true;
        this.prediction = await this.predictionService.predict({

            input: this.predictionInput
        });
        this.predicting = false;

        this.$nextTick(() => {

            this.step = 1;
        });
    }

    reset() {

        this.step = 0;

        this.predictionInput = {

            number_of_occupants: 1,
            activity_of_occupants: 0
        }

        this.prediction = null;
    }
}
</script>

<style lang="less" scoped>

</style>
