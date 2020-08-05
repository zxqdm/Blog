<template>
  <div>
    <div class="btn" @click="showClick">
      <span class="iconfont iconcaidan" v-if="btnShow"></span>
      <span class="iconfont iconguanbi" v-if="!btnShow"></span>
    </div>
    <div class="author" v-show="isShow">
      <div class="avatar">
        <el-avatar :size="150"
                   :src="avatarSrc"
                   shape="square">

        </el-avatar>
      </div>
      <div class="profile">
        <span class="name">只想敲代码</span>
        <span class="info">不断脱发，不断变强</span>
        <span class="info">邮箱：997635832@qq.com</span>
      </div>
    </div>
  </div>
</template>

<script>

  export default {
    name: "Author",
    data() {
      return {
        username: '',
        isShow: false,
        btnShow: true,
        avatarSrc: 'http://127.0.0.1:8000/media/authorAvatar.jpg'
      }
    },
    methods: {
      showClick() {
        this.isShow = !this.isShow
        this.btnShow = !this.btnShow
      }
    }
  }
</script>

<style scoped>
  .btn {
    width: 40px;
    height: 40px;
    background-color: #171c24;
    border-radius: 50%;
    color: #eee;
    cursor: pointer;
    position: fixed;
    bottom: 40px;
    right: 40px;
    z-index: 5;
    text-align: center;
    line-height: 40px;
  }

  .btn span {
    font-size: 20px;
  }

  .author {
    width: 300px;
    height: 100vh;
    position: fixed;
    right: 0;
    background-color: #171c24;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 120px;
  }

  .author .profile span {
    display: block;
    text-align: center;
    padding-top: 20px;
  }

  .author .profile .name {
    color: #eee;
    font-size: 18px;
  }

  .author .profile .info {
    color: #999999;
    font-size: 14px;
  }

  @media (max-width: 1680px) {
    div {
      display: none;
    }
  }
</style>
