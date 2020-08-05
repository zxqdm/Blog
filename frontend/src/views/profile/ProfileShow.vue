<template>
  <div>
    <p>用户名：{{user.username}}</p>
    <p>邮箱：{{user.email}}</p>
    <p>创建时间：{{user.created}}</p>
    <el-button type="primary" @click="changeProfile">修改信息</el-button>
  </div>
</template>

<script>
  export default {
    name: "ProfileShow",
    props: {
      user: {
        type: Object,
        default() {
          return {}
        }
      }
    },
    methods: {
      changeProfile() {
        this.$router.push('/profile/change')
      }
    }
  }
</script>

<style scoped>

</style>
