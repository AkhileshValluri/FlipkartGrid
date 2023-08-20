<template>
  <MetaData/>
</template>

<script>
import MetaData from './components/MetaData.vue'
import axios from 'axios';
export default {
  name: 'App',
  components: {
    MetaData
  },
  mounted() {
    axios.get('http://localhost:5000/')
      .then(res => console.log(res))
      .catch(err => console.log(err))
  }
}
</script>

<style>
body{
  background-color: #047BD5;
}

#app {
  font-family:  'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: white;
}
</style>
