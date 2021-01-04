<template>
    <div class="indexBody">
        {{ info }}
    <p>{{test123}}</p>
        <span v-bind:title="msg1">
    鼠标悬停几秒钟查看此处动态绑定的提示信息！
  </span>
        <p v-if="seen">现在你看到我了</p>
        <button v-on:click="reverseMessage">反转消息</button>
    </div>

</template>

<script>
    import axios from 'axios';
    export default {
        name: "main",
        props: {
            msg: String
        },
        data: function () {
            return {
                msg1: 0,
                seen:true,
                test123:"test123",
                info:null
            }
        },
        methods: {
            reverseMessage: function () {
                this.test123 = this.test123.split('').reverse().join('')
            }
        },
        mounted(){
            axios
                .get('https://api.coindesk.com/v1/bpi/currentprice.json')
                .then(response => (this.info = response))
        }


    }


</script>

<style scoped>

</style>