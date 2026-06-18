<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <el-icon :size="28" color="#409EFF"><ScaleToOriginal /></el-icon>
        <span class="logo-text">法律咨询平台</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        class="sidebar-menu"
      >
        <template v-if="isClient">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/lawyers">
            <el-icon><User /></el-icon>
            <span>找律师</span>
          </el-menu-item>
          <el-menu-item index="/consultation">
            <el-icon><ChatDotRound /></el-icon>
            <span>在线咨询</span>
          </el-menu-item>
          <el-menu-item index="/appointments">
            <el-icon><Calendar /></el-icon>
            <span>我的预约</span>
          </el-menu-item>
        </template>
        <template v-if="isLawyer">
          <el-menu-item index="/lawyer/cases">
            <el-icon><Document /></el-icon>
            <span>案件管理</span>
          </el-menu-item>
          <el-menu-item index="/lawyer/documents">
            <el-icon><Files /></el-icon>
            <span>文书生成</span>
          </el-menu-item>
          <el-menu-item index="/lawyer/knowledge">
            <el-icon><Reading /></el-icon>
            <span>知识库</span>
          </el-menu-item>
        </template>
        <template v-if="isAdmin">
          <el-menu-item index="/admin/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/admin/verifications">
            <el-icon><CircleCheck /></el-icon>
            <span>资质审核</span>
          </el-menu-item>
          <el-menu-item index="/admin/complaints">
            <el-icon><Warning /></el-icon>
            <span>投诉处理</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <span class="page-title">{{ pageTitle }}</span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" :src="userInfo?.avatar">
                {{ userInfo?.full_name?.charAt(0) }}
              </el-avatar>
              <span class="username">{{ userInfo?.full_name }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const userInfo = computed(() => userStore.userInfo)
const isClient = computed(() => userStore.isClient)
const isLawyer = computed(() => userStore.isLawyer)
const isAdmin = computed(() => userStore.isAdmin)

const activeMenu = computed(() => {
  const path = route.path
  if (path.startsWith('/lawyer')) {
    return '/lawyer/cases'
  }
  if (path.startsWith('/admin')) {
    return '/admin/dashboard'
  }
  return path
})

const pageTitle = computed(() => {
  const path = route.path
  const titles = {
    '/': '首页',
    '/lawyers': '找律师',
    '/consultation': '在线咨询',
    '/appointments': '我的预约',
    '/lawyer/cases': '案件管理中心',
    '/lawyer/documents': '文书生成器',
    '/lawyer/knowledge': '知识库',
    '/admin/dashboard': '数据统计',
    '/admin/verifications': '律师资质审核',
    '/admin/complaints': '投诉处理',
  }
  return titles[path] || '法律咨询平台'
})

function handleCommand(command) {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }).then(() => {
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/login')
    }).catch(() => {})
  } else if (command === 'profile') {
    ElMessage.info('个人中心功能开发中')
  }
}

onMounted(() => {
  if (userStore.token && !userStore.userInfo) {
    userStore.fetchUserInfo()
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid #1f2d3d;
}

.logo-text {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #606266;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
