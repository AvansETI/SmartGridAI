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
                            <v-tabs v-model="tab" background-color="transparent" grow show-arrows>
                                <v-tab>Predict Now</v-tab>
                                <v-tab>Predict in the Future</v-tab>
                            </v-tabs>

                            <v-tabs-items v-model="tab">
                                <v-tab-item>
                                    <v-card flat>
                                        <v-card-text>
                                            <ValidationObserver ref="basicValidationObserver" v-slot="{ handleSubmit }" class="basic-form-holder">
                                                <v-form @submit.prevent="handleSubmit(() => predict(false))">

                                                    <v-row>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="number_of_occupants" name="number_of_occupants"
                                                                rules="required|integer|min_value:1|max_value:2147483647" v-slot="{ errors }"
                                                            >
                                                                <v-text-field name="number_of_occupants" min="1" max="2147483647" label="Number of Occupants" type="number" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.number_of_occupants" :error-messages="errors"></v-text-field>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="activity_of_occupants" name="activity_of_occupants"
                                                                rules="required|integer" v-slot="{ errors }"
                                                            >
                                                                <v-select name="activity_of_occupants" label="What will the occupants be doing?" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.activity_of_occupants" :items="activityOfOccupantsItems" :error-messages="errors"></v-select>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="window_state" name="window_state"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-checkbox name="window_state" label="Are there any open windows?" :disabled="shouldDisable" :prepend-icon="windowIcon" v-model="predictionInput.window_state" :error-messages="errors"></v-checkbox>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="state_of_door" name="state_of_door"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-checkbox name="state_of_door" label="Are there any open doors?" :disabled="shouldDisable" :prepend-icon="doorIcon" v-model="predictionInput.state_of_door" :error-messages="errors"></v-checkbox>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12">
                                                            <ValidationProvider
                                                                vid="room" name="room"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-select name="room" :items="roomItems" label="What room will the occupants be in?" :disabled="shouldDisable" prepend-icon="mdi-office-building-marker" v-model="predictionInput.room" :error-messages="errors"></v-select>
                                                            </ValidationProvider>
                                                        </v-col>
                                                    </v-row>

                                                    <div class="d-flex justify-end">
                                                        <v-btn :disabled="shouldDisable" :loading="predicting" color="primary" type="submit">Predict</v-btn>
                                                    </div>

                                                </v-form>
                                            </ValidationObserver>
                                        </v-card-text>
                                    </v-card>
                                </v-tab-item>

                                <v-tab-item>
                                    <v-card flat>
                                        <v-card-text>
                                            <ValidationObserver ref="extendedValidationObserver" v-slot="{ handleSubmit }" class="extended-form-holder">
                                                <v-form @submit.prevent="handleSubmit(() => predict(true))">

                                                    <v-row>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="number_of_occupants" name="number_of_occupants"
                                                                rules="required|integer|min_value:1|max_value:2147483647" v-slot="{ errors }"
                                                            >
                                                                <v-text-field name="number_of_occupants" min="1" max="2147483647" label="Number of Occupants" type="number" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.number_of_occupants" :error-messages="errors"></v-text-field>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="activity_of_occupants" name="activity_of_occupants"
                                                                rules="required|integer" v-slot="{ errors }"
                                                            >
                                                                <v-select name="activity_of_occupants" label="What will the occupants be doing?" :disabled="shouldDisable" prepend-icon="mdi-account-multiple" v-model.number="predictionInput.activity_of_occupants" :items="activityOfOccupantsItems" :error-messages="errors"></v-select>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="window_state" name="window_state"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-checkbox name="window_state" label="Are there any open windows?" :disabled="shouldDisable" :prepend-icon="windowIcon" v-model="predictionInput.window_state" :error-messages="errors"></v-checkbox>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="state_of_door" name="state_of_door"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-checkbox name="state_of_door" label="Are there any open doors?" :disabled="shouldDisable" :prepend-icon="doorIcon" v-model="predictionInput.state_of_door" :error-messages="errors"></v-checkbox>
                                                            </ValidationProvider>
                                                        </v-col>

                                                        <v-col cols="12">
                                                            <ValidationProvider
                                                                vid="room" name="room"
                                                                rules="required" v-slot="{ errors }"
                                                            >
                                                                <v-select name="room" :items="roomItems" label="What room will the occupants be in?" :disabled="shouldDisable" prepend-icon="mdi-office-building-marker" v-model="predictionInput.room" :error-messages="errors"></v-select>
                                                            </ValidationProvider>
                                                        </v-col>
                                                    </v-row>

                                                    <v-divider class="my-7"></v-divider>

                                                    <v-row>
                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="time" name="time"
                                                                rules="" v-slot="{ errors }"
                                                            >
                                                                <v-time-picker
                                                                    format="24hr" name="time" label="Time" use-seconds
                                                                    :disabled="shouldDisable" prepend-icon="mdi-clock-outline"
                                                                    v-model="predictionInput.time" :error-messages="errors"
                                                                ></v-time-picker>
                                                            </ValidationProvider>
                                                        </v-col>
                                                        <v-col cols="12" md="6">
                                                            <ValidationProvider
                                                                vid="temperature" name="temperature"
                                                                rules="min_value:-10|max_value:100" v-slot="{ errors }"
                                                            >
                                                                <v-slider name="temperature" :color="temperatureColor" min="-10" max="50" step="0.5" label="Temperature" :disabled="shouldDisable" prepend-icon="mdi-thermometer-lines" v-model.number="predictionInput.temperature" :error-messages="errors">
                                                                    <template v-slot:append>
                                                                        <h3 :style="`color: ${ temperatureColor };`">{{ predictionInput.temperature.toFixed(1) }}&deg;</h3>
                                                                    </template>
                                                                </v-slider>
                                                            </ValidationProvider>

                                                            <ValidationProvider
                                                                vid="mean_temp_day" name="mean_temp_day"
                                                                rules="min_value:-10|max_value:100" v-slot="{ errors }"
                                                            >
                                                                <v-slider name="mean_temp_day" :color="temperatureColor" min="-10" max="50" step="0.5" label="Mean Outside Temperature" :disabled="shouldDisable" prepend-icon="mdi-thermometer-lines" v-model.number="predictionInput.mean_temp_day" :error-messages="errors">
                                                                    <template v-slot:append>
                                                                        <h3 :style="`color: ${ meanTempDayColor };`">{{ predictionInput.mean_temp_day.toFixed(1) }}&deg;</h3>
                                                                    </template>
                                                                </v-slider>
                                                            </ValidationProvider>
                                                        </v-col>
                                                    </v-row>

                                                    <div class="d-flex justify-end">
                                                        <v-btn :disabled="shouldDisable" :loading="predicting" color="primary" type="submit">Predict</v-btn>
                                                    </div>

                                                </v-form>
                                            </ValidationObserver>
                                        </v-card-text>
                                    </v-card>
                                </v-tab-item>
                            </v-tabs-items>
                        </v-stepper-content>

                        <v-stepper-content :step="1">
                            <v-card v-if="prediction != null">
                                <v-card-title class="justify-center align-center flex-column mb-7">
                                    <v-icon v-if="prediction.satisfaction >= satisfied" :size="70" class="mb-4" :class="predictionDisplayClass">mdi-emoticon-excited-outline</v-icon>
                                    <v-icon v-else :size="70" class="mb-4" :class="predictionDisplayClass">mdi-emoticon-sad-outline</v-icon>

                                    <span class="text-h4" v-if="predictionInput.activity_of_occupants != 0">
                                        The {{ predictionInput.number_of_occupants }} {{ activityOfOccupantsItems.find(ao => ao.value === predictionInput.activity_of_occupants).text.toLowerCase() }} <span :class="predictionDisplayClass">{{ prediction.satisfaction >= satisfied ? "comfortably" : "uncomfortably" }}</span>.
                                    </span>
                                    <span class="text-h4" v-else>
                                        The {{ predictionInput.number_of_occupants }} occupant(s) will be <span :class="predictionDisplayClass">{{ prediction.satisfaction >= satisfied ? "comfortable" : "uncomfortable" }}</span>.
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
                            <h3 class="text-h6 mb-2">Why will they be {{ prediction.satisfaction >= satisfied ? "comfortable" : "uncomfortable" }}?</h3>
                            <div>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aspernatur assumenda ea eius in ipsum nulla recusandae! Cum fugiat id laudantium modi molestiae quae reiciendis totam veritatis. Beatae earum omnis possimus.</div>
                            <div>Accusantium quibusdam quidem quod repellat vel veniam vero voluptas. Aliquam debitis iure libero modi nostrum nulla praesentium repudiandae similique! A ab autem consequatur deleniti hic iure, laborum neque nostrum praesentium.</div>
                            <div>Amet assumenda atque autem, blanditiis eaque enim, expedita explicabo fuga itaque labore nemo numquam pariatur praesentium quas quasi, qui quis quos repellendus rerum ut? Expedita nemo possimus quibusdam quis vitae.</div>
                        </div>

                        <AdditiveForceVisualizer v-bind="shapJSON"></AdditiveForceVisualizer>

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
import colors from "vuetify/lib/util/colors";

// Services
import { PredictionService } from "@/services/prediction-service";

// Enums
import { OccupantsActivity } from "@/enums/occupants-activity";

// Filters
import { occupantsActivityFilter } from "@/filters/occupants-activity-filter";

// SHAP
import { AdditiveForceVisualizer, AdditiveForceArrayVisualizer, SimpleListVisualizer } from "shapjs";


@Component({

    name: "IndexPage",
    components: { AdditiveForceVisualizer, AdditiveForceArrayVisualizer, SimpleListVisualizer }
})
export default class IndexPage extends Vue {

    data() {

        return {

            step: 0,
            tab: 0,

            satisfied: 1,

            predicting: false,
            prediction: null,

            basicFields: [
                "number_of_occupants",
                "activity_of_occupants",
                "window_state", "state_of_door",
                "room"
            ],
            emptyPredictionInput: {

                number_of_occupants: 1,
                activity_of_occupants: 0,

                window_state: false,
                state_of_door: false,

                room: null,

                temperature: 21.5,
                mean_temp_day: 9.5,

                time: null,
                head_index: null,
            },

            predictionInput: {}
        };
    }

    created() {

        this.predictionService = new PredictionService(this.$apollo.getClient());
        this.predictionInput = { ...this.emptyPredictionInput };
    }

    get shapJSON() {

        return JSON.parse(this.prediction.shapOptions);
    }

    get meanTempDayColor() {

        if (this.predictionInput?.mean_temp_day <= 5) {

            return colors.blue.darken1;
        }
        else if (this.predictionInput?.mean_temp_day <= 15) {

            return colors.blue.base;
        }
        else if (this.predictionInput?.mean_temp_day <= 30) {

            return this.$vuetify?.theme?.themes?.light?.primary || null;
        }
        else if (this.predictionInput?.mean_temp_day <= 40) {

            return colors.deepOrange.base;
        }
        else if (this.predictionInput?.mean_temp_day <= 50) {

            return colors.red.base;
        }
    }

    get temperatureColor() {

        if (this.predictionInput?.temperature <= 5) {

            return colors.blue.darken1;
        }
        else if (this.predictionInput?.temperature <= 15) {

            return colors.blue.base;
        }
        else if (this.predictionInput?.temperature <= 30) {

            return this.$vuetify?.theme?.themes?.light?.primary || null;
        }
        else if (this.predictionInput?.temperature <= 40) {

            return colors.deepOrange.base;
        }
        else if (this.predictionInput?.temperature <= 50) {

            return colors.red.base;
        }
    }

    get windowIcon() {

        return this.predictionInput.window_state ? "mdi-window-open-variant" : "mdi-window-closed-variant";
    }

    get doorIcon() {

        return this.predictionInput.state_of_door ? "mdi-door-sliding-open" : "mdi-door-sliding";
    }

    get roomItems() {

        //@TODO: Retrieve from API endpoint
        return [

            {
                text: "Room A",
                value: 0
            },

            {
                text: "Room B",
                value: 1
            },

            {
                text: "Room C",
                value: 2
            }
        ];
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
            "error--text": (this.prediction.satisfaction < this.satisfied),
            "success--text": (this.prediction.satisfaction >= this.satisfied)
        };
    }

    async predict(extended = false) {

        this.predicting = true;

        if (extended && this.predictionInput.time != null) {

            //Prep Time
            const timeMap = this.predictionInput.time.split(":");

            this.predictionInput.hour = parseInt(timeMap[0]);
            this.predictionInput.minute = parseInt(timeMap[1]);
            this.predictionInput.second = parseInt(timeMap[2]);
        }

        if (this.predictionInput.temperature != null) {

            this.predictionInput.heat_index = 0; //@TODO: CALCULATE
        }

        delete this.predictionInput.time;

        this.prediction = await this.predictionService.predict({

            input: extended ? this.predictionInput : {

                ...(

                    this.basicFields.reduce(

                        (acc, key) => ({ ...acc, [key]: this.predictionInput[key] }),
                        {}
                    )
                )
            }
        });
        this.predicting = false;

        this.$nextTick(() => {

            this.step = 1;
        });
    }

    reset() {

        this.step = 0;
        this.predictionInput = { ...this.emptyPredictionInput };
        this.prediction = null;
    }
}
</script>

<style lang="less" scoped>

</style>
