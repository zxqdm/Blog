import Vue from "vue";
import VueRouter from 'vue-router';

const Comment = () => import('components/common/Comment')

const Home = () => import('views/home/Home')
const Tags = () => import('views/tags/Tags')
const Login = () => import('views/login/Login')
const Register = () => import('views/register/Register')

const BlogAdd = () => import('views/blog/BlogAdd')
const Blog = () => import('views/blog/Blog')

const Profile = () => import('views/profile/Profile')
const ProfileChange = () => import('views/profile/ProfileChange')
const ProfileShow = () => import('views/profile/ProfileShow')

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path: '',
    redirect: '/home'
  },
  {
    path: '/home',
    component: Home,
    name: 'home',
  },
  {
    path: '/blog',
    component: Blog,
    name: 'blog',
  },
  {
    path: '/tags',
    component: Tags,
    name: 'tag',
  },
  {
    path: '/login',
    component: Login,
    name: 'login'
  },
  {
    path: '/register',
    component: Register,
    name: 'register'
  },
  {
    path: '/profile',
    component: Profile,
    children: [
      {
        path: '',
        component: ProfileShow,
        name: 'profile',
      },
      {
        path: 'change',
        component: ProfileChange,
        name: 'profileChange'
      }
    ]
  },
  {
    path: '/blogAdd',
    component: BlogAdd,
    name: 'blogAdd',
  },
  {
    path: '/comment',
    component: Comment,
    name: 'comment',
  },
]

const router = new VueRouter({
  routes,
  mode: 'history'
})

export default router
