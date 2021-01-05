<template>
    <b-container fluid="" >
        <H4 class="text-left">Control</H4>

        <b-row>
            <b-card-group deck>

                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Mode Switch</h5>
                        <p class="card-text">Switch between automatic and manual control mode</p>
                        <div>
                            <b-button-group>
                                <b-button @click="onBtnClick('mode_switch','auto')">Automatic</b-button>
                                <b-button @click="onBtnClick('mode_switch','manual')">Manual</b-button>
                            </b-button-group>
                        </div>
                    </div>
                </div>

                <div class="card" >
                    <div class="card-body">
                        <h5 class="card-title">Real-Time Control</h5>
                        <p class="card-text">Manually operate the water pump and motor.</p>
                        <b-button-group>
                            <b-button @click="onBtnClick('control','water_start')">Watering</b-button>
                            <b-button @click="onBtnClick('control','rotate_start')">Rotating</b-button>
                        </b-button-group>
                    </div>
                </div>

                <div class="card" >
                    <div class="card-body">
                        <h5 class="card-title">Target Humidity: {{humInp}}</h5>
                        <b-col class="card-text mb-4">

                            <b-input-group prepend="10" append="100" class="mt-3">
                                <b-form-input v-model="humInp" type="range" min="10" max="100"></b-form-input>
                            </b-input-group>

                        </b-col>

                        <b-button class="btn-secondary" @click="onBtnClick('humidity_control',humInp)">Apply Humidity</b-button>
                    </div>
                </div>
            </b-card-group>
        </b-row>
    </b-container>
</template>

<script>


    export default {
        name: "control",
        data() {
            return {
                humInp:50,

            }
        },
        methods: {
            onBtnClick(mode,val) {
                var aClickJSON = {"cmd": mode,"val":val};
                console.log(aClickJSON);
                fetch('http://521.cpp.moe/console_post.php', {
                    method: 'post',
                    body: JSON.stringify(aClickJSON)
                });



            }
        }
    }
</script>

<style scoped>

</style>