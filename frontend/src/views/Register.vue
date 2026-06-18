<template>
  <div class="register-page">
    <div class="register-box">
      <h2 class="title">账号注册</h2>
      <el-tabs v-model="activeTab" class="register-tabs">
        <el-tab-pane label="用户注册" name="user">
          <el-form :model="userForm" :rules="userRules" ref="userFormRef">
            <el-form-item prop="username">
              <el-input v-model="userForm.username" placeholder="用户名" size="large" />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="userForm.email" placeholder="邮箱" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="userForm.password" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input v-model="userForm.confirmPassword" type="password" placeholder="确认密码" size="large" show-password />
            </el-form-item>
            <el-form-item prop="phone">
              <el-input v-model="userForm.phone" placeholder="手机号" size="large" />
            </el-form-item>
            <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="handleUserRegister">
              注册
            </el-button>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="律师入驻" name="lawyer">
          <el-form :model="lawyerForm" :rules="lawyerRules" ref="lawyerFormRef">
            <el-form-item prop="username">
              <el-input v-model="lawyerForm.username" placeholder="用户名" size="large" />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="lawyerForm.email" placeholder="邮箱" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="lawyerForm.password" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>
            <el-form-item prop="name">
              <el-input v-model="lawyerForm.name" placeholder="真实姓名" size="large" />
            </el-form-item>
            <el-form-item prop="phone">
              <el-input v-model="lawyerForm.phone" placeholder="手机号" size="large" />
            </el-form-item>
            <el-form-item prop="firm">
              <el-input v-model="lawyerForm.firm" placeholder="律所名称" size="large" />
            </el-form-item>
            <el-form-item prop="licenseNumber">
              <el-input v-model="lawyerForm.licenseNumber" placeholder="执业证号" size="large" />
            </el-form-item>
            <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="handleLawyerRegister">
              提交入驻申请
            </el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div class="footer">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import request from "../utils/request"

const router = useRouter()
const activeTab = ref("user")
const loading = ref(false)
const userFormRef = ref(null)
const lawyerFormRef = ref(null)

const userForm = reactive({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
  phone: ""
})

const lawyerForm = reactive({
  username: "",
  email: "",
  password: "",
  name: "",
  phone: "",
  firm: "",
  licenseNumber: ""
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== userForm.password) {
    callback(new Error("两次输入的密码不一致"))
  } else {
    callback()
  }
}

const userRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  confirmPassword: [{ required: true, validator: validateConfirmPassword, trigger: "blur" }],
  phone: [{ required: true, message: "请输入手机号", trigger: "blur" }]
}

const lawyerRules = {
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  email: [{ required: true, message: "请输入邮箱", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  name: [{ required: true, message: "请输入真实姓名", trigger: "blur" }],
  phone: [{ required: true, message: "请输入手机号", trigger: "blur" }],
  firm: [{ required: true, message: "请输入律所名称", trigger: "blur" }],
  licenseNumber: [{ required: true, message: "请输入执业证号", trigger: "blur" }]
}

async function handleUserRegister() {
  await userFormRef.value?.validate()
  loading.value = true
  try {
    await request.post("/auth/register", userForm)
    ElMessage.success("注册成功，请登录")
    router.push("/login")
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleLawyerRegister() {
  await lawyerFormRef.value?.validate()
  loading.value = true
  try {
    await request.post("/auth/register/lawyer", lawyerForm)
    ElMessage.success("入驻申请已提交，请等待审核")
    router.push("/login")
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.register-box {
  width: 480px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}
.title {
  text-align: center;
  margin: 0 0 30px;
  color: #333;
}
.footer {
  text-align: center;
  margin-top: 20px;
  color: #999;
  font-size: 14px;
}
.footer a {
  color: #409eff;
  text-decoration: none;
}
</style>
