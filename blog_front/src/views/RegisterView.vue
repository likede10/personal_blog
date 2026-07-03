<template>
  <div class="register-page">
    <div class="register-container">
      <section class="register-hero">
        <div class="hero-content">
          <p class="hero-kicker">PERSONAL BLOG</p>
          <h1>创建你的博客账号</h1>
          <p class="hero-desc">
            使用邮箱验证码完成注册，进入后台后可以管理文章、分类、标签和个人资料。
          </p>

          <div class="hero-list">
            <div class="hero-item">
              <el-icon><EditPen /></el-icon>
              <span>发布和管理博客文章</span>
            </div>
            <div class="hero-item">
              <el-icon><Lock /></el-icon>
              <span>邮箱验证码保护账号安全</span>
            </div>
            <div class="hero-item">
              <el-icon><User /></el-icon>
              <span>支持个人资料和头像设置</span>
            </div>
          </div>
        </div>
      </section>

      <section class="register-card">
        <div class="register-title">
          <h2>注册账号</h2>
          <p>请输入信息完成注册</p>
        </div>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          label-position="top"
          size="large"
          @submit.prevent
        >
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model.trim="registerForm.username"
              placeholder="请输入用户名"
              clearable
            />
          </el-form-item>

          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model.trim="registerForm.email"
              placeholder="请输入邮箱"
              clearable
            />
          </el-form-item>

          <el-form-item label="邮箱验证码" prop="emailCode">
            <div class="code-row">
              <el-input
                v-model.trim="registerForm.emailCode"
                placeholder="请输入 6 位验证码"
                maxlength="6"
                clearable
              />
              <el-button
                class="code-button"
                :disabled="sendCodeDisabled"
                :loading="sendingCode"
                @click="handleSendCode"
              >
                {{ codeButtonText }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item label="昵称" prop="nickname">
            <el-input
              v-model.trim="registerForm.nickname"
              placeholder="请输入昵称，可选"
              clearable
            />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              clearable
            />
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              show-password
              clearable
            />
          </el-form-item>

          <el-button
            class="register-button"
            type="primary"
            :loading="submitting"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form>

        <div class="register-footer">
          已有账号？
          <router-link to="/login">去登录</router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { EditPen, Lock, User } from '@element-plus/icons-vue'

const router = useRouter()

const registerFormRef = ref(null)
const submitting = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)
let countdownTimer = null

const registerForm = reactive({
  username: '',
  email: '',
  emailCode: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入密码'))
    return
  }

  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
    return
  }

  callback()
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应为 3 到 50 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] }
  ],
  emailCode: [
    { required: true, message: '请输入邮箱验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '验证码应为 6 位数字', trigger: 'blur' }
  ],
  nickname: [
    { max: 80, message: '昵称不能超过 80 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, max: 128, message: '密码长度应为 8 到 128 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const sendCodeDisabled = computed(() => {
  return sendingCode.value || countdown.value > 0 || !emailPattern.test(registerForm.email)
})

const codeButtonText = computed(() => {
  if (countdown.value > 0) {
    return `${countdown.value}s 后重发`
  }

  return '发送验证码'
})

const startCountdown = () => {
  countdown.value = 60

  countdownTimer = window.setInterval(() => {
    countdown.value -= 1

    if (countdown.value <= 0) {
      window.clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

const handleSendCode = async () => {
  if (!registerForm.email) {
    ElMessage.warning('请先输入邮箱')
    return
  }

  if (!emailPattern.test(registerForm.email)) {
    ElMessage.warning('邮箱格式不正确')
    return
  }

  sendingCode.value = true

  try {
    const response = await fetch('/api/auth/email-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: registerForm.email,
        scene: 'register'
      })
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.detail || data.message || '验证码发送失败')
    }

    ElMessage.success('验证码已发送，请查看邮箱')
    startCountdown()
  } catch (error) {
    ElMessage.error(error.message || '验证码发送失败，请稍后再试')
  } finally {
    sendingCode.value = false
  }
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: registerForm.username,
          email: registerForm.email,
          email_code: registerForm.emailCode,
          nickname: registerForm.nickname || null,
          password: registerForm.password
        })
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        throw new Error(data.detail || data.message || '注册失败')
      }

      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (error) {
      ElMessage.error(error.message || '注册失败，请稍后再试')
    } finally {
      submitting.value = false
    }
  })
}

onBeforeUnmount(() => {
  if (countdownTimer) {
    window.clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(circle at 15% 20%, rgba(64, 158, 255, 0.2), transparent 28%),
    radial-gradient(circle at 85% 80%, rgba(103, 194, 58, 0.14), transparent 26%),
    linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.register-container {
  width: 100%;
  max-width: 1120px;
  min-height: 680px;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  overflow: hidden;
  border-radius: 28px;
  background: #ffffff;
  box-shadow: 0 30px 90px rgba(15, 23, 42, 0.16);
}

.register-hero {
  position: relative;
  padding: 64px;
  display: flex;
  align-items: center;
  color: #ffffff;
  background:
    linear-gradient(135deg, rgba(37, 99, 235, 0.96), rgba(30, 64, 175, 0.96)),
    url('https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80');
  background-size: cover;
  background-position: center;
}

.register-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.08), rgba(15, 23, 42, 0.32));
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 520px;
}

.hero-kicker {
  margin: 0 0 18px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.16em;
  opacity: 0.86;
}

.hero-content h1 {
  margin: 0;
  font-size: 44px;
  line-height: 1.16;
  font-weight: 800;
}

.hero-desc {
  margin: 22px 0 34px;
  max-width: 440px;
  font-size: 16px;
  line-height: 1.8;
  opacity: 0.9;
}

.hero-list {
  display: grid;
  gap: 16px;
}

.hero-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  opacity: 0.95;
}

.hero-item .el-icon {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.16);
}

.register-card {
  padding: 56px 54px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.register-title {
  margin-bottom: 28px;
}

.register-title h2 {
  margin: 0 0 8px;
  font-size: 30px;
  font-weight: 800;
  color: #111827;
}

.register-title p {
  margin: 0;
  font-size: 14px;
  color: #64748b;
}

.code-row {
  width: 100%;
  display: flex;
  gap: 12px;
}

.code-row .el-input {
  flex: 1;
}

.code-button {
  width: 128px;
  flex-shrink: 0;
}

.register-button {
  width: 100%;
  margin-top: 8px;
}

.register-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #64748b;
}

.register-footer a {
  color: #409eff;
  text-decoration: none;
  font-weight: 600;
}

.register-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 900px) {
  .register-page {
    padding: 24px;
  }

  .register-container {
    max-width: 520px;
    min-height: auto;
    grid-template-columns: 1fr;
  }

  .register-hero {
    padding: 36px 32px;
  }

  .hero-content h1 {
    font-size: 30px;
  }

  .hero-desc {
    margin: 16px 0 22px;
    font-size: 14px;
  }

  .hero-list {
    gap: 10px;
  }

  .register-card {
    padding: 34px 32px 38px;
  }

  .register-title h2 {
    font-size: 26px;
  }
}

@media (max-width: 480px) {
  .register-page {
    padding: 14px;
    align-items: flex-start;
  }

  .register-container {
    border-radius: 18px;
  }

  .register-hero {
    padding: 28px 22px;
  }

  .hero-kicker {
    margin-bottom: 12px;
    font-size: 12px;
  }

  .hero-content h1 {
    font-size: 25px;
  }

  .hero-desc {
    line-height: 1.7;
  }

  .hero-item {
    font-size: 13px;
  }

  .register-card {
    padding: 28px 22px 30px;
  }

  .code-row {
    gap: 8px;
  }

  .code-button {
    width: 112px;
    padding-left: 8px;
    padding-right: 8px;
  }
}
</style>