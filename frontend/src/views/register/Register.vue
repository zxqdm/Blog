<template>
  <div class="register">
    <div class="reg-form">
      <h2 class="reg-title">注册</h2>
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
        <el-form-item label="确认密码"
                      prop="checkpass">
          <el-input type="password"
                    v-model="ruleForm.checkpass"
                    placeholder="请再次输入密码"
                    maxlength="16"></el-input>
        </el-form-item>
        <el-form-item label="邮箱"
                      prop="email">
          <el-input type="email"
                    placeholder="请输入邮箱"
                    v-model="ruleForm.email"></el-input>
        </el-form-item>
        <el-form-item>
          <div class="btn">
            <el-button type="primary" @click="submitForm">注册</el-button>
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
    name: "Register",
    data() {
      const validateCheckPass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback()
        }
      }
      return {
        checked: false,
        ruleForm: {
          username: '',
          password: '',
          checkpass: '',
          email: '',
        },
        rules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
            {min: 6, message: '用户名最少6位', trigger: 'blur'},
          ],
          password: [
            {required: true, message: '请输入密码', trigger: 'blur'},
            {min: 6, max: 16, message: '密码最少6位', trigger: 'blur'},
          ],
          checkpass: [
            {
              validator: validateCheckPass, trigger: 'blur', required: true
            }
          ],
          email: [
            {required: true, message: '请输入邮箱', trigger: 'blur'},
            {
              pattern: /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
              message: '邮箱格式不正确', trigger: 'blur'
            },
          ]
        }
      }
    },
    methods: {
      submitForm() {
        if (this.ruleForm.username === '' || this.ruleForm.password === '' || this.ruleForm.password === '' || this.ruleForm.email === '') {
          this.$alert('内容不能为空', {
            confirmButtonText: '确定',
          })
        } else {
          let data = new URLSearchParams()
          data.append('username', this.ruleForm.username)
          data.append('password', this.ruleForm.password)
          data.append('email', this.ruleForm.email)
          request({
            method: 'post',
            url: '/api/register/',
            data: data,
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
                  this.$router.replace({name: 'login'})
                }
              })
            }
          })
        }
      },
      cancel() {
        this.$router.go(-1)
      },
    }
  }
</script>

<style scoped>
  .register {
    position: absolute;
    height: 100%;
    width: 100%;
    background: url("../../assets/img/login1.jpg") no-repeat;
    background-size: cover;
  }

  .reg-form {
    width: 600px;
    margin: 160px auto;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 30px;
    display: flex;
    align-items: center;
  }

  .reg-title {
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

  .el-button {
    width: 100%;
  }

  .el-form-item >>> .el-form-item__label {
    color: #e9e9e9;
  }
</style>
