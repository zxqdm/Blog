<template>
  <div>
    <!--头部-->
    <nav-bar/>
    <!--内容-->
    <el-row>
      <el-col :xs="{span:24, offset:0}" :sm="{span:24, offset:0}" :md="{span:20, offset:2}" :lg="{span:16, offset:4}"
              :xl="{span:16, offset:4}">
        <el-container>
          <el-main>
            <div>
              <router-view :user="user"/>
            </div>
          </el-main>
        </el-container>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {request} from "network/request";
  import NavBar from "components/common/NavBar";
  export default {
    name: "Profile",
    components: {
      NavBar
    },
    data() {
      return {
        user: {}
      }
    },
    created() {
      let data = new URLSearchParams()
      data.append('username', this.$store.state.user.username)
      request({
        method: 'post',
        url: '/api/profile/',
        data: data
      }).then(res => {
        this.user = res.data.data
      })
    },
  }
</script>

<style scoped>

</style>
