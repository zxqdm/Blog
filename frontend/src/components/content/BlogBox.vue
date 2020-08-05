<template>
  <div>
    <div class="blog-box" v-for="(blog, index) in this.blogs" :key="index">
      <div class="title">
        <span><a :href="getArticle(blog.id)">{{blog.title}}</a></span>
      </div>
      <div class="infor">
        <span class="iconfont iconrili">发布时间: {{blog.updated}}</span>
        <span class="iconfont iconbrowse">{{blog.visitNum}}</span>
        <span class="iconfont iconcomments">{{blog.commentNum}}</span>
        <span class="iconfont icondiscount"><a v-for="tag in blog.tags" :href="getTag(tag)">{{tag}}</a></span>
      </div>
      <div class="blog">
        <span>{{blog.content}}</span>
      </div>
      <div class="more">
        <span @click="moreClick(blog.id)">阅读全文</span>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    name: "BlogBox",
    props: {
      blogs: {
        type: Array,
        default() {
          return []
        }
      }
    },
    methods: {
      getArticle(bid) {
        return '/blog?bid=' + bid
      },
      getTag(tag) {
        return '/home?tag=' + tag
      },
      moreClick(bid) {
        this.$router.push('/blog?bid=' + bid)
      },
    }
  }
</script>

<style scoped>
  a {
    text-decoration: none;
    color: black;
  }

  .blog-box {
    margin: 50px 0;
    display: flex;
    flex-direction: column;
    flex-basis: auto;
  }

  .blog-box .title {
    font-size: 26px;
    font-weight: 500;
    letter-spacing: 2px;
    padding: 10px 0 10px;
  }

  .blog-box .infor {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 0 10px;
  }

  .blog-box .infor span {
    font-size: 15px;
    color: #999;
    display: block;
    padding-right: 20px;
  }

  .blog-box .infor span a {
    color: #999;
    padding: 5px;
  }

  .blog-box .infor span a:hover {
    color: #df5000;
  }

  .blog-box .infor .icondiscount {
    flex: 2;
  }

  .blog-box .blog {
    padding: 10px 0 10px;
    flex: 1;
  }
  .blog-box .more {
    padding: 10px 0 10px;
  }

  .blog-box .more span {
    cursor: pointer;
    font-size: 14px;
    border-bottom: 2px #999999 solid;
  }

  .blog-box .more span:hover {
    color: #df5000;
    border-bottom: 2px #df5000 solid;
  }
</style>
