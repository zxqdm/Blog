<template>
  <layout>
    <div slot="main" class="main">
      <div class="header">
        <span class="title">{{this.article.title}}</span>
        <div>
          <span class="iconfont iconrili">发布时间: {{this.article.updated}}</span>
          <span class="iconfont iconbrowse">{{this.article.visit_num}}</span>
          <span class="iconfont icondiscount"><a v-for="tag in this.article.tags" :href="getTag(tag)">{{tag}}</a></span>
        </div>
      </div>
      <div class="article">
        <mavon-editor class="md"
                      v-model="article.content"
                      defaultOpen="preview"
                      :boxShadow="false"
                      :subfield="false"
                      :toolbarsFlag="false"
                      :editable="false"
                      :scrollStyle="false"
                      previewBackground="#fff"/>
      </div>
      <comment :commentList="commentList"/>
    </div>
  </layout>
</template>

<script>
  import Layout from "components/content/Layout";
  import Comment from "components/common/Comment";

  import {request} from 'network/request'

  export default {
    inject: ['reload'],
    name: "Blog",
    components: {
      Layout,
      Comment,
    },
    data() {
      return {
        article: {
          type: Object,
          default() {
            return {}
          }
        },
        commentList: [],
        reviewShow:false,
        placeholder: '',
        comUser: '',
      }
    },
    created() {
      let data = new URLSearchParams()
      data.append('bid', this.$route.query.bid)
      request({
        method: 'post',
        url: '/api/article/',
        data: data
      }).then(response => {
        this.article = response.data.data
      })
      request({
        method: 'post',
        url: '/api/comment/',
        data: data
      }).then(response => {
        this.commentList = response.data.data;
      })
    },
    methods: {
      getTag(tag) {
        return '/home?tag=' + tag
      },
    }
  }
</script>

<style scoped>
  a {
    text-decoration: none;
    color: #0c73c2;
  }
  .main {
    margin-top: 50px;
    display: flex;
    flex-direction: column;
  }
  .main .header {
    text-align: center;
    margin-bottom: 10px;
  }
  .main .header span {
    font-size: 15px;
    color: #999;
    display: block;
    padding-right: 20px;
  }
  .main .header span a {
    display: inline-block;
    padding: 0 5px;
  }
  .main .header .title {
    font-size: 28px;
    font-weight: 600;
    color: #222226;
    word-break: break-all;
    margin: 0;
    padding-bottom: 10px;
  }
  .main .header div {
    padding: 10px 0;
    display: flex;
    justify-content: center;
    align-content: center;
  }
  .main .article {
    margin: 50px 0;
    z-index: 0;
  }
  .main .article .md {
    border: none;
  }
</style>
