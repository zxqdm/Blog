<template>
  <div class="comment-box">
    <div class="myComment" >
      <div v-if="$store.state.isLogin">
        <div class="avatar">
          <el-avatar :size="40" :src="avatarUrl"></el-avatar>
        </div>
        <div class="myCommentInput">
          <el-input v-model="commentInput"
                    type="textarea"
                    placeholder="请输入评论..."
                    maxlength="1000"
                    show-word-limit
                    @focus="inputFocus"
                    resize="none"
                    :autosize="{minRows:4, maxRows:4}">

          </el-input>
          <div class="btn" v-show="btnShow">
            <el-button type="primary"
                       round
                       size="small"
                       :disabled="btnAble"
                       @click="sendComment">发布
            </el-button>
            <el-button round size="small" @click="cancel">取消</el-button>
          </div>
        </div>
      </div>
      <div v-if="!$store.state.isLogin">
        <el-button type="primary" round @click="logClick">登录</el-button>
        or
        <el-button type="danger" round @click="regClick">注册</el-button>
      </div>
    </div>
    <div class="comments">
      <div class="title">
        <span>全部评论</span>
      </div>
      <div class="comments-item"
           v-for="(comment, index) in this.commentList"
           :key="index">
        <div class="avatar">
          <el-avatar :size="40" :src="'http://127.0.0.1:8000/media/' + comment.avatar"></el-avatar>
        </div>
        <div class="comments-item-right">
          <div class="username">
            <span>{{comment.fromUser}}</span>
          </div>
          <div class="time">
            <span>{{comment.created}}</span>
          </div>
          <div class="content">
            <span>{{comment.content}}</span>
          </div>
          <div class="replyBtn">
            <span @click="showReplyInput(comment)">
              <i class="iconfont iconcomments">回复</i>
            </span>
          </div>
          <div class="reply-box"
               v-for="(reply, index) in comment.replies">
            <div class="avatar">
              <el-avatar :size="40" :src="'http://127.0.0.1:8000/media/' + reply.avatar"></el-avatar>
            </div>
            <div class="comments-item-right">
              <div class="username">
                <span>{{reply.fromUser}}</span>
              </div>
              <div class="time">
                <span>{{reply.created}}</span>
              </div>
              <div class="content">
                <span>{{reply.content}}</span>
              </div>
              <div class="replyBtn">
                <span @click="showReplyInput(comment, reply)">
                  <i class="iconfont iconcomments">回复</i>
                </span>
              </div>
            </div>
          </div>
          <div class="myComment" v-if="comment.id === showInputId">
            <div class="avatar">
              <el-avatar :size="40" :src="avatarUrl"></el-avatar>
            </div>
            <div class="myCommentInput">
              <el-input v-model="replyInput"
                        type="textarea"
                        maxlength="1000"
                        show-word-limit
                        @focus="inputFocus"
                        resize="none"
                        :autosize="{minRows:4, maxRows:4}">

              </el-input>
              <div class="btn">
                <el-button type="primary"
                           round
                           size="small" @click="sendReply()">发布
                </el-button>
                <el-button round size="small" @click="cancelReply">取消</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p v-show="this.commentList.length === 0">暂无评论</p>
    </div>
  </div>
</template>

<script>
  import {request} from "network/request";

  export default {
    inject: ['reload'],
    name: 'Comment',
    props: {
      commentList: {
        type: Array,
        default() {
          return []
        }
      }
    },
    data() {
      return {
        avatarUrl: 'http://39.98.207.147/media/' + this.$store.state.user.avatar,
        commentInput: '',
        replyInput: '',
        btnShow: false,
        btnAble: true,
        showInputId: '',
        reply: {
          toUser: '',
          type: '',
          cid: '',
          rid: '',
        },
      }
    },
    methods: {
      logClick() {
        this.$router.replace({name: 'login'})
      },
      regClick() {
        this.$router.replace({name: 'register'})
      },
      inputFocus() {
        this.btnShow = true
      },
      cancel() {
        this.btnShow = false
      },
      cancelReply() {
        this.showInputId = ''
      },
      showReplyInput(comment, reply) {
        if (reply) {
          this.replyInput = "@" + reply.fromUser + " "
          this.reply.toUser = reply.fromUser
          this.reply.type = 'reply'
          this.reply.cid = comment.id
          this.reply.rid = reply.id
        } else {
          this.replyInput = "@" + comment.fromUser + " "
          this.reply.toUser = comment.fromUser
          this.reply.type = 'comment'
          this.reply.cid = comment.id
        }
        this.showInputId = comment.id
      },
      sendComment(){
        let bid = this.$route.query.bid
        let user = this.$store.state.user.username
        let data = new URLSearchParams()
        data.append('bid', bid)
        data.append('fromUser', user)
        data.append('content', this.commentInput)
        request({
          method: 'post',
          url: '/api/commentAdd/',
          data: data
        }).then(response => {
          let res = response.data
          if (res.status === 1) {
            this.$alert(res.message, {
              confirmButtonText: '确定',
              callback: () => {
                this.reload()
              }
            })
          }
        })
      },
      sendReply() {
        console.log(this.reply);
        let data = new URLSearchParams()
        data.append('fromUser', this.$store.state.user.username)
        data.append('toUser', this.reply.toUser)
        data.append('type', this.reply.type)
        data.append('cid', this.reply.cid)
        data.append('rid', this.reply.rid)
        data.append('content', this.replyInput)
        request({
          method: 'post',
          url: '/api/replyAdd/',
          data: data
        }).then(response => {
          let res = response.data
          if (res.status === 1) {
            this.$alert(res.message, {
              confirmButtonText: '确定',
              callback: () => {
                this.reload()
              }
            })
          }
        })
      }
    },
    watch: {
      commentInput: function () {
        this.btnAble = this.commentInput === '';
      }
    }
  }
</script>

<style scoped>
  .el-button {
    margin: 0 10px;
  }
  .comment-box {
    padding: 10px;
  }

  .comment-box .myComment {
    display: flex;
    flex-wrap: nowrap;
    padding: 20px 0;
  }

  .avatar {
    margin: 5px;
  }

  .comment-box .myComment .myCommentInput {
    flex: 2;
    margin: 5px;
    display: flex;
    flex-direction: column;
  }

  .comment-box .myComment .myCommentInput .btn {
    margin: 5px;
    display: flex;
    justify-content: flex-end;
  }

  .comment-box .comments {
    padding-top: 20px;
  }

  .comment-box .comments .title span {
    font-size: 20px;
    font-weight: 500;
  }

  .comment-box .comments .comments-item {
    display: flex;
    margin: 20px 0;
    border-bottom: 1px #eee solid;
  }

  .comment-box .comments .comments-item .comments-item-right {
    padding: 5px;
    flex-grow: 2;
  }

  .comment-box .comments .comments-item .comments-item-right .username {
    font-size: 14px;
  }

  .comment-box .comments .comments-item .comments-item-right .time {
    font-size: 12px;
    color: #999999;
    margin-bottom: 20px;
  }

  .comment-box .comments .comments-item .comments-item-right .replyBtn {
    font-size: 14px;
    color: #b0b0b0;
    margin: 20px 0;
  }

  .replyBtn span {
    cursor: pointer;
  }

  .reply-box {
    padding-top: 20px;
    width: 100%;
    border-top: 1px #eee solid;
    display: flex;
    flex-basis: auto;
  }
  p {
    color: #999;
    font-size: 14px;

  }
</style>
