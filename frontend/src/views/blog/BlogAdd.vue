<template>
  <layout>
    <div slot="container" class="container">
      <h2>添加博客</h2>
      <div style="margin-top: 20px">
        <el-input v-model="title"
                  id="title"
                  placeholder="请输入标题"
                  style="width: 500px">
        </el-input>
      </div>
      <div style="margin-top: 20px">
        <el-tag
          :key="tag"
          v-for="tag in tags"
          closable
          :disable-transitions="false"
          @close="handleClose(tag)">
          {{tag}}
        </el-tag>
        <el-input
          class="input-new-tag"
          v-if="inputVisible"
          v-model="tagAdd"
          ref="saveTagInput"
          size="small"
          @keyup.enter.native="handleInputConfirm"
          @blur="handleInputConfirm"
        >
        </el-input>
        <el-button
          v-else
          class="button-new-tag"
          size="small"
          @click="showInput">
          添加新标签
        </el-button>
      </div>
      <div style="margin-top: 20px">
        <mavon-editor v-model="content"
                      ref="md"
                      @imgAdd="$imgAdd"
                      @imgDel="$imgDel"/>
      </div>
      <div class="btn">
        <el-button type="primary" round @click="saveBtn">发布博客</el-button>
        <el-button round @click="goBack">取消</el-button>
      </div>
    </div>
  </layout>
</template>

<script>
  import Layout from "components/content/Layout";

  import {request} from "network/request"

  export default {
    name: "BlogAdd",
    components: {
      Layout,
    },
    data() {
      return {
        title: '',
        content: '',
        tags: [],
        inputVisible: false,
        tagAdd: '',
        img_file: {},
      }
    },
    created() {
      request({
        method: 'get',
        url: '/api/tags/',
      }).then(response => {
        let res = response.data
        this.tags = res.data.tags
      })
    },
    methods: {
      // 绑定@imgAdd event
      $imgAdd(pos, $file) {
        // 缓存图片信息
        this.img_file[pos] = $file;
      },
      $imgDel(pos) {
        //删除缓存的指定的图片
        delete this.img_file[pos];
      },
      async uploadImg($e) {
        return new Promise((resolve, reject) => {
          let data = new FormData()
          for (let _img in this.img_file) {
            data.append('imgList[]', this.img_file[_img])
          }
          request({
            method: 'post',
            url: '/api/saveImg/',
            data: data,
            headers: {'Content-Type': 'multipart/form-data'},
          }).then(response => {
            let res = response.data
            if (res.status === 1) {
              for (var i in res.data) {
                this.$refs.md.$img2Url(res.data[i][0], 'http://127.0.0.1:8000/media/' + res.data[i][1]);
              }
              resolve()
            }
          })
        })
      },
      uploadBlog() {
        let data = new URLSearchParams()
        data.append('title', this.title)
        data.append('content', this.content)
        data.append('user', this.$store.state.user.username)
        data.append('tags', this.tags)
        request({
          method: 'post',
          url: '/api/articleAdd/',
          data: data,
        }).then(response => {
          let res = response.data
          if (res.status === 1) {
            this.$alert(res.message, {
              confirmButtonText: '确定',
              callback: () => {
                this.$router.replace({name: 'home'})
              }
            })
          }
        })
      },
      async saveBtn() {
        await this.uploadImg()

        this.uploadBlog()

      },
      goBack() {
        this.$router.go(-1)
      },

      // 关闭标签后从tags中删除该标签
      handleClose(tag) {
        this.tags.splice(this.tags.indexOf(tag), 1);
      },

      // 显示添加标签的input
      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },

      // 将新标签添加到tags中，并将input框重新隐藏
      handleInputConfirm() {
        let tagAdd = this.tagAdd;
        if (tagAdd) {
          this.tags.push(tagAdd);
        }
        this.inputVisible = false;
        this.tagAdd = '';
      }
    }
  }
</script>

<style scoped>
  .btn {
    margin-top: 20px;
  }

  .el-tag {
    margin-right: 10px;
  }

  .button-new-tag {
    margin-right: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }

  .input-new-tag {
    width: 90px;
    margin-right: 10px;
    vertical-align: bottom;
  }
</style>
