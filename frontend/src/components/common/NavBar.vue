<template>
  <div style="background-color:#171c24;">
    <el-row>
      <el-col :xs="{span:24, offset:0}" :sm="{span:24, offset:0}" :md="{span:20, offset:2}" :lg="{span:16, offset:4}"
              :xl="{span:16, offset:4}">
        <div class="nav-bar">
          <div class="logo">
            <router-link to="/home">只想敲代码</router-link>
          </div>
          <el-menu class="el-menu"
                   mode="horizontal"
                   :default-active="this.$route.path"
                   router
                   active-text-color="#ff3d00">
            <el-menu-item index="/home">首页</el-menu-item>
            <el-menu-item index="/tags">标签</el-menu-item>
          </el-menu>
          <div class="nav-right" v-show="!$store.state.isLogin">
            <router-link to="/login">登录</router-link>
            <router-link to="/register">注册</router-link>
          </div>
          <div class="nav-right" v-show="$store.state.isLogin">
            <el-avatar size="medium" :src="avatarSrc"></el-avatar>
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                {{username}}
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="blogAdd" v-show="access">添加博客</el-dropdown-item>
                <el-dropdown-item command="logout">退出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    inject: ['reload'],
    name: "NavBar",
    data() {
      return {
        input: '',
        username: '',
        avatarSrc: '',
        access: false,
      }
    },
    created() {
      const user = this.$store.state.user
      if (this.$store.state.isLogin) {
        this.username = user.username
        this.avatarSrc = 'http://127.0.0.1:8000/media/' + user.avatar
        this.access = user.access===1
      }
    },
    methods: {
      handleCommand(command) {
        if (command === 'logout') {
          localStorage.removeItem('user')
          localStorage.removeItem('isLogin')
          this.$store.commit('changeLoginStatus')
          this.$router.push({name: 'home'})
        } else if (command === 'profile'){
          this.$router.push({
            name: 'profile',
            query: {user: this.$store.state.user.username}
          })
        } else if (command === 'blogAdd') {
          this.$router.push({
            name: 'blogAdd'
          })
        }
      },
    }
  }
</script>

<style scoped>
  .nav-bar {
    height: 70px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    padding: 0;
  }

  .nav-bar .logo {
    flex: 2;
  }

  .nav-bar .logo a {
    color: #eee;
    font-size: 30px;
    font-weight: 600;
    letter-spacing: 1px;
    text-decoration: none;
  }

  .nav-bar .el-menu {
    background-color: #171c24;
    border-bottom: none;
    margin-left: 50px;
  }

  .nav-bar .el-menu .el-menu-item{
    font-size: 16px;
    font-weight: 500;
    color: #eee;
    border-bottom: none;
  }

  .nav-bar .el-menu .el-menu-item:hover {
    background-color: #171c24;
    color: #df5000;
  }

  .nav-bar .el-menu.el-menu--horizontal {
    border-bottom: none;
  }

  .nav-bar .nav-right {
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 20px;
    line-height: 60px;
  }

  .nav-bar .nav-right a {
    margin-left: 20px;
    text-decoration: none;
    color: rgb(255, 61, 0);
    display: block;
  }

  .nav-bar .nav-right .el-avatar {
    display: block;
    margin-right: 10px;
  }

  .nav-bar .nav-right .el-dropdown {
    display: block;
  }

  .nav-bar .el-dropdown-link {
    cursor: pointer;
    color: #eee;
  }

  .nav-bar .el-icon-arrow-down {
    font-size: 12px;
  }
</style>
