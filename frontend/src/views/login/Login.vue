<template>
  <div class="login">
    <div class="login-form">
      <h1 class="login-title">登录</h1>
      <el-form :model="ruleForm"
               label-width="100px"
               :rules="rules"
               ref="ruleForm"
               status-icon>
        <el-form-item label="用户名"
                      prop="username">
          <el-input type="username"
                    v-model="ruleForm.username"
                    placeholder="请输入用户名"
                    maxlength="16"></el-input>
        </el-form-item>
        <el-form-item label="密码"
                      prop="password">
          <el-input type="password"
                    v-model="ruleForm.password"
                    placeholder="请输入密码"
                    maxlength="16"></el-input>
        </el-form-item>
        <el-form-item>
          <a href="#" style="text-decoration: none; color: #ff0000">忘记密码？</a>
        </el-form-item>
        <el-form-item>
          <div class="btn">
            <el-button type="primary" @click="submitForm">登录</el-button>
            <el-button type="danger" @click="regClick">注册</el-button>
            <el-button @click="cancel">取消</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
  import {request} from "network/request";

  export default {
    name: "Login",
    data() {
      return {
        ruleForm: {
          username: '',
          password: '',
        },
        rules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {min: 6, message: '用户名最少6位', trigger: 'blur'},
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {min: 6, message: '密码最少6位', trigger: 'blur'},
          ],
        }
      }
    },
    methods: {
      submitForm() {
        if (this.ruleForm.username === '' || this.ruleForm.password === '') {
          this.$alert('内容不能为空', {
            confirmButtonText: '确定',
          })
        } else {
          let data = new URLSearchParams()
          data.append('username', this.ruleForm.username)
          data.append('password', this.ruleForm.password)
          request({
            method: 'post',
            url: '/api/login/',
            data: data
          }).then(response => {
            let res = response.data
            if (res.status === 0) {
              this.$message({
                type: 'error',
                message: res.message
              })
            } else if (res.status === 1) {
              this.$alert(res.message, {
                confirmButtonText: '确定',
                callback: () => {
                  localStorage.setItem('user', JSON.stringify(res.data))
                  localStorage.setItem('isLogin', '1')
                  this.$store.commit('changeLoginStatus')
                  this.$router.replace('/')
                }
              })
            }
          })
        }
      },
      regClick() {
        this.$router.replace({name: 'register'})
      },
      cancel() {
        this.$router.go(-1)
      },
    }
  }
</script>

<style scoped>
  .login {
    position: absolute;
    height: 100%;
    width: 100%;
    background: url("../../assets/img/login1.jpg") no-repeat;
    background-size: cover;
  }

  .login-form {
    width: 600px;
    margin: 160px auto;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 30px;
    display: flex;
    align-items: center;
  }

  .login-title {
    text-align: center;
    color: #e9e9e9;
    letter-spacing: 50px;
    margin-left: 25px;
    flex-grow: 2;
  }

  .btn {
    display: flex;
    flex-direction: row
  }

  .el-form {
    flex-grow: 8;
    padding: 30px 0 20px 0;
  }

  .el-checkbox {
    color: #e9e9e9;
  }

  .el-button {
    width: 100%;
  }

  .el-form-item >>> .el-form-item__label {
    color: #e9e9e9;
  }
</style>
