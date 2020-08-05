<template>
  <layout>
    <div slot="main">
        <div class="main">
          <blog-box :blogs="blogList"></blog-box>
          <infinite-loading spinner="spiral" @infinite="load">
            <p slot="no-more" style="color: #999999; font-size: 14px">没有更多了</p>
          </infinite-loading>
        </div>
    </div>
  </layout>
</template>

<script>
  import Layout from "components/content/Layout";
  import BlogBox from "components/content/BlogBox";
  import InfiniteLoading from 'vue-infinite-loading';

  import {request} from "network/request"

  export default {
    name: "Home",
    components: {
      Layout,
      BlogBox,
      InfiniteLoading,
    },
    data() {
      return {
        blogList: [],
        currentPages: 1,
        totalPages: 1,
      }
    },
    created() {
      // 获取用户登录状态
      if(this.$store.state.isLogin) {
        let now = parseInt(new Date() / 1000)
        if (now > this.$store.state.user.endtime) {
          localStorage.removeItem('user')
          localStorage.removeItem('isLogin')
          this.$store.commit('changeLoginStatus')
        }
      }

      // 获取博客列表
      let data = new URLSearchParams()
      data.append('currentPages', this.currentPages)
      if (this.$route.query) {
        data.append('tag', this.$route.query.tag)
      }
      this.getBlogs(data).then(response => {
        let res = response.data
        if (res.status === 1) {
          this.blogList = res.data;
          this.totalPages = res.numPages;
        }
      })
    },
    methods: {
      getBlogs(data) {
        return request ({
          url: '/api/blog/',
          method: 'post',
          data: data
        })
      },
      load($state) {
        setTimeout(() => {
          this.currentPages += 1;
          let data = new URLSearchParams()
          data.append('currentPages', this.currentPages)
          if (this.$route.query) {
            data.append('tag', this.$route.query.tag)
          }
          this.getBlogs(data).then(response => {
            let res = response.data
            if (res.status === 1) {
              this.blogList = this.blogList.concat(res.data)
              if (this.currentPages < this.totalPages){
                $state.loaded();
              } else {
                $state.complete();
              }
            }
          })
        }, 2000);
      },
    }
  }
</script>

<style scoped>

</style>
