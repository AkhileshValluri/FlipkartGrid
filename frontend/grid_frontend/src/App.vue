<template>
  <MetaData/>
</template>

<script>
import MetaData from './components/MetaData.vue'

export default {
  name: 'App',
  components: {
    MetaData
  }
}
</script>

<style>
body{
  background-color: #2b2a2b;
}

#app {
  font-family:  'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: white;
}
</style>
