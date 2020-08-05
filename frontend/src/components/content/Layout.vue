<template>
  <div>
    <!-- 侧边栏 -->
    <author/>

    <!--头部-->
    <nav-bar/>
    <!--内容-->
    <el-row>
      <el-col :xs="{span:24, offset:0}" :sm="{span:24, offset:0}" :md="{span:20, offset:2}" :lg="{span:16, offset:4}"
              :xl="{span:16, offset:4}">
        <el-container>
          <el-main>
            <slot name="main"></slot>
          </el-main>
          <el-backtop style="background-color: #171c24; color: #fff"/>
        </el-container>
      </el-col>
    </el-row>

    <!--底部-->
    <Footer/>
  </div>
</template>

<script>
  import NavBar from "components/common/NavBar";
  import Footer from "components/common/Footer";
  import Author from "components/content/Author";

  export default {
    name: "Layout",
    components: {
      NavBar,
      Author,
      Footer,
    }
  }
</script>

<style scoped>
  .el-main {
    overflow: visible!important;
  }
  .el-backtop {
    right: 100px!important;
  }
</style>
