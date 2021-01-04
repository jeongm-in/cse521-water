<template>
    <b-container fluid="" >
        <H4 class="text-left">Watering Last 30 Days</H4>
        <b-row>
            <b-table head-variant="light" bordered hover :items="status"></b-table>
<!--            <b-button @click="onBtnClick()">refresh(test)</b-button>-->
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: "historytable",
        data: function () {
            return {
                fields: ['#', 'date_time', 'soil_humidity'],
                status: null,
                test:null,
            }
        },
        methods:{
            onBtnClick(){
                this.fetchData();

            },
            fetchData(){
                var aClickJSON = {"cmd": "getHistory","val":1};
                fetch('http://521.cpp.moe/console_post.php', {
                    method: 'post',
                    body: JSON.stringify(aClickJSON)
                }).then(response => response.json())
                    .then(data => {
                        //this.consoleOut(data);
                        this.genTable(data)
                    }).catch(error => console.error(error));
            },
            consoleOut(data){
                console.log(data);
            },
            genTable(data){
                let i;
                let res = [];
                for (i = 1; i <= data.length; i++) {
                    let elem = Object.values(data[i-1]);
                    res.push({ "#": i, date_time:  elem[1] , soil_humidity: + elem[0] });
                    //console.log(elem);
                }
                this.status = res;
                //console.log("table updated")

            }
        },
        mounted:function () {
            this.fetchData();
            window.setInterval(() => {
                this.fetchData()
            }, 2000)
            //console.log(123);
        },

    }
</script>

<style scoped>

</style>