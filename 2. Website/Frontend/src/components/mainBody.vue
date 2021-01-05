<template>
        <b-container fluid="" >
            <b-row class="pt-1">
                <b-col style="padding-right:2rem; border-right: 0.1rem solid #ccc;" >
                    <indexStatus style="padding-bottom:1rem; border-bottom: 0.1rem solid #ccc;"></indexStatus>
                    <b-row style="padding-top:1rem; border-bottom: 0.1rem solid #ccc;" ><humidity-chart></humidity-chart></b-row>

                </b-col>


                <b-col style="padding-left:2rem; border-left: 0.1rem solid #ccc;">
                    <indexControl style="padding-bottom:1rem; border-bottom: 0.1rem solid #ccc;"></indexControl>
                    <b-row style="padding-top:1rem; border-bottom: 0.1rem solid #ccc;" ><historytable></historytable></b-row>

                </b-col>
            </b-row>
        </b-container>

</template>

<script>
    import indexStatus from "@/components/Index/status";
    import indexControl from "@/components/Index/control";
    import humidityChart from "@/components/Index/humiditychart";
    import Historytable from "@/components/Index/historytable";
    export default {
        name: "mainBody",
        components:{
            Historytable,
            indexStatus,
            indexControl,
            humidityChart,
        },

        data: function () {
            return {
                items: [
                    { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
                    { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
                    { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' },
                    { age: 38, first_name: 'Jami', last_name: 'Carney' }
                ]
            }
        },
    }
</script>

<style scoped>

</style>