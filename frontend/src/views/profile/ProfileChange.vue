<template>
  <div>
    <el-form :model="form"
             ref="form"
             label-width="100px">
      <el-form-item
        :prop="form.email"
        label="邮箱"
        :rules="[
            {
              type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change']
            }
          ]"
      >
        <el-input v-model="form.email"></el-input>
      </el-form-item>
      <el-form-item label="修改头像">
        <el-upload
          class="avatar-uploader"
          action="#"
          :http-request="httpRequest"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload">
          <img v-if="form.imageUrl" :src="form.imageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即修改</el-button>
        <el-button @click="goBack">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import {request} from "network/request";

  export default {
    inject: ['reload'],
    name: "ProfileChange",
    data() {
      return {
        form: {
          email: '',
          imageUrl: ''
        }
      }
    },
    methods: {
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      httpRequest(data) {
        let _this = this
        let rd = new FileReader()
        let file = data.file
        rd.readAsDataURL(file)
        rd.onloadend = function (e) {
          _this.form.imageUrl = this.result
        }
      },
      onSubmit() {
        if (this.form.imageUrl === '' && this.form.email === '') {
          this.$alert('请填写修改内容', {
            confirmButtonText: '确定'
          })
        } else {
          let data = new URLSearchParams()
          data.append('username', this.$store.state.user.username)
          data.append('email', this.form.email)
          data.append('img', this.form.imageUrl)
          request({
            method: 'post',
            url: '/api/profile/change/',
            data: data
          }).then(res => {
            this.$store.state.user.avatar = res.data.data.avatar
            localStorage.setItem('user', JSON.stringify(this.$store.state.user))
            this.$router.replace({name: 'profile'})
            this.reload()
          })
        }
      },
      goBack() {
        this.$router.go(-1)
      }
    }
  }
</script>

<style scoped>
  .el-form {
    width: 500px;
    height: auto;
  }

  .avatar-uploader >>> .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader >>> .el-upload:hover {
    border-color: #409EFF;
  }

  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }

  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
