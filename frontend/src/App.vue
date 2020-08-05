<template>
  <div id="app">
    <router-view v-if="isRouterAlive"/>
  </div>
</template>

<script>

  export default {
    name: "App",
    components: {},
    data() {
      return {
        isRouterAlive: true
      }
    },
    provide() {
      return {
        reload: this.reload
      }
    },
    methods: {
      reload() {
        this.isRouterAlive = false
        this.$nextTick(() => {
          this.isRouterAlive = true
        })
      }
    }
  }
</script>

<style>
  @import 'assets/css/base.css';
</style>
