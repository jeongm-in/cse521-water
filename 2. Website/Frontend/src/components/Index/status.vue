<template>
    <b-container fluid="" >
      <H4 class="text-left">Status</H4>
        <b-row>
        <b-col>
            <b-table head-variant="light" bordered hover :items="status1"></b-table>
        </b-col>
        <b-col>
            <b-table head-variant="light" bordered hover :items="status2"></b-table>

        </b-col>
        </b-row>
<!--        <b-button @click="onBtnClick()">refresh(test)</b-button>-->
    </b-container>


</template>

<script>
    export default {
        name: "status",

        data: function () {
            return {
                status1: [
                    { Name: 'System',  Info: "Normal" },
                    { Name: 'Water',  Info: 'Normal' },
                    { Name: 'Pump',  Info: 'Normal' },
                    { Name: 'Motor',  Info: 'Normal' }
                ],
                status2: [
                    { Name: 'Watering Mode',  Info: 'Loading...' },
                    { Name: 'Last Reporting',  Info: 'Loading...' },
                    { Name: 'Soil Humidity',  Info: 'Loading...' },
                    { Name: 'Sunlight',  Info: 'Loading...' }
                ]
            }
        },
        methods:{
            onBtnClick(){
                this.fetchData();
            },
            fetchData(){
                var aClickJSON = {"cmd": "getRealTime","val":1};
                fetch('http://521.cpp.moe/console_post.php', {
                    method: 'post',
                    body: JSON.stringify(aClickJSON)
                }).then(response => response.json())
                    .then(data => {
                        this.genTable(data);
                        //this.consoleOut(data);

                    });
            },
            consoleOut(data){
                console.log(data);
            },
            genTable(data){
                let res = [];
                let mode = null;
                //console.log(data);
                let record = Object.values(data[0]);
                if(record[2] === "0"){mode = "Automatic"}else {mode = "Manual"}
                res.push({ Name: 'Watering Mode',  Info: mode });
                res.push({ Name: 'Last Reporting',  Info: record[1] });
                res.push({ Name: 'Soil Humidity',  Info: record[0] });
                res.push({ Name: 'Sunlight',  Info: record[3] });
                this.status2 = res;
                //console.log(record)

            }
        },
        mounted:function () {
            this.fetchData();
            window.setInterval(() => {
                this.fetchData()
            }, 2000);
            console.log(123);
        },

    }
</script>

<style scoped>

</style>