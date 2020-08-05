<template>
  <layout>
    <div slot="main" class="main">
      <div class="title">
        <span>标签</span>
      </div>
      <div class="tags">
        <div class="tag" v-for="(tag, index) in tagList" :key="index">
          <span @click="tagClick(tag)">{{tag}}</span>
        </div>
      </div>
    </div>
  </layout>
</template>

<script>
  import Layout from "components/content/Layout";

  import {request} from 'network/request'

  export default {
    name: "Tags",
    components: {
      Layout
    },
    data() {
      return {
        tagList: [],
      }
    },
    created() {
      request({
        method: 'get',
        url: '/api/tags/'
      }).then(response => {
        let res = response.data
        this.tagList = res.data
      })
    },
    methods: {
      tagClick(tag) {
        this.$router.replace({name: 'home', query: {tag: tag}})
      }
    }
  }
</script>

<style scoped>
  .main {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-content: center;
  }
  .title {
    text-align: center;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 10px 0;
    margin: 20px 0;
  }
  .tags {
    display: flex;
    justify-content: center;
    align-content: center;
    margin: 20px 0;
  }
  .tag{
    padding: 0 10px;

  }
  .tag span {
    border-bottom: 1px #999 solid;
    cursor: pointer;
  }
  .tag span:hover {
    color: #df5000;
    border-bottom: 1px #df5000 solid;
  }
</style>
