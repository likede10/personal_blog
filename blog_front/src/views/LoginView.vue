<script setup>
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

import { login_request } from '@/request/login'

const login =  async(item) => {
    const data = await login_request(item)
    console.log(data)
}

</script>

<template>
 <el-button type="success" :icon="Check" circle @click="login(9)" />
</template>

<style scoped>

</style>
