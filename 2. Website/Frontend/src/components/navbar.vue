<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
            <b-navbar-brand href="#">Watering System Console</b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-navbar-nav>
                        <b-nav-text class="mr-2" >Current Time:</b-nav-text>
                        <b-nav-text>&nbsp;{{curr_time}}</b-nav-text>
                    </b-navbar-nav>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    export default {
        name: "navbar",

        data:function () {
            return{
                curr_time: null,
            }
        },
        created() {
            setInterval(this.getNow, 1000);
        },
        methods: {
            getNow: function() {
                const today = new Date();
                const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
                const time = today.getHours() + ":" + (today.getMinutes()<10?'0':'') + today.getMinutes() + ":" + (today.getSeconds()<10?'0':'') + today.getSeconds();
                this.curr_time = date + ' ' + time;
            }
        }
    }
</script>

<style scoped>

</style>