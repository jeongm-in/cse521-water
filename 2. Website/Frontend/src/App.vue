<template>
  <div id="app">
    <navbar></navbar>
    <mainBody></mainBody>
  </div>
</template>

<script>

import navbar from "@/components/navbar";
import mainBody from "@/components/mainBody";


export default {
  name: 'App',
  components: {
    navbar,
    mainBody,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
