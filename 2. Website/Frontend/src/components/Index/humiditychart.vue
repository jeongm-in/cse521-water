<template>
    <b-container fluid="" >
        <H4 class="text-left">Humidity Last 12 Hours</H4>
        <div v-if="alertFlag" class="alert alert-danger" role="alert">
            Warning: In last 12 hours, humidity level is less than 30, check the system status.
        </div>
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

        data: function () {
            return {
                status1: [
                    { Time: 'Loading',  Humidity: "Loading" },
                    { Time: 'Loading',  Humidity: 'Loading' },
                    { Time: 'Loading',  Humidity: 'Loading' },
                    { Time: 'Loading',  Humidity: 'Loading' }
                ],
                status2: [
                    { Time: 'Loading',  Humidity: 'Loading' },
                    { Time: 'Loading',  Humidity: 'Loading' },
                    { Time: 'Loading',  Humidity: 'Loading' },
                    { Time: 'Loading',  Humidity: 'Loading' }
                ],
                alertFlag : 0
            }
        },
        methods:{
            onBtnClick(){
                this.fetchData();
            },
            fetchData(){
                var aClickJSON = {"cmd": "getHum12Hr","val":1};
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
                let res1 = [];
                let res2 = [];

                var flag = 0;
                for (let elem of data) {
                    if(elem < 30){
                        flag = 1;
                    }
                }
                if(flag === 1){
                    this.alertFlag = 1
                }else{
                    this.alertFlag = 0
                }

                const date = new Date();

                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[0] });
                date.setHours(date.getHours() -1);
                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[1] });
                date.setHours(date.getHours() -1);
                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[2] });
                date.setHours(date.getHours() -1);
                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[3] });
                date.setHours(date.getHours() -1);
                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[4] });
                date.setHours(date.getHours() -1);
                res1.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[5] });
                this.status1 = res1;

                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[6] });
                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[7] });
                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[8] });
                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[9] });
                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[10] });
                date.setHours(date.getHours() -1);
                res2.push({ Time: date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate()+ " " +date.getHours() + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes(),  Humidity: data[11] });
                this.status2 = res2;
                //console.log(record)

            }
        },
        mounted:function () {
            this.fetchData();
            window.setInterval(() => {
                this.fetchData()
            }, 60000)
            console.log(123);
        },

    }
</script>

<style scoped>

</style>