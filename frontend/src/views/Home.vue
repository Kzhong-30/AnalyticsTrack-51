<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-content">
        <h1>专业法律咨询服务平台</h1>
        <p class="subtitle">汇聚全国优秀律师，为您提供专业、便捷的法律服务</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="goToConsult">立即咨询</el-button>
          <el-button size="large" @click="goToLawyers">找律师</el-button>
        </div>
      </div>
    </section>

    <section class="categories-section">
      <h2 class="section-title">法律领域</h2>
      <el-row :gutter="20">
        <el-col :span="8" v-for="cat in categories" :key="cat.id">
          <el-card class="category-card" shadow="hover" @click="goToCategory(cat)">
            <div class="cat-icon">{{ cat.icon }}</div>
            <h3>{{ cat.name }}</h3>
            <p>{{ cat.desc }}</p>
          </el-card>
        </el-col>
      </el-row>
    </section>

    <section class="lawyers-section">
      <div class="section-header">
        <h2 class="section-title">推荐律师</h2>
        <el-button type="text" @click="goToLawyers">查看更多 →</el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="6" v-for="lawyer in recommendedLawyers" :key="lawyer.id">
          <LawyerCard :lawyer="lawyer" />
        </el-col>
      </el-row>
    </section>

    <section class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6" v-for="stat in stats" :key="stat.label">
          <div class="stat-item">
            <div class="stat-number">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import LawyerCard from "../components/LawyerCard.vue"
import request from "../utils/request"

const router = useRouter()
const recommendedLawyers = ref([])

const categories = [
  { id: "marriage", name: "婚姻家庭", icon: "👨‍👩‍👧", desc: "离婚、财产分割、子女抚养" },
  { id: "labor", name: "劳动纠纷", icon: "💼", desc: "劳动合同、工伤赔偿、社保" },
  { id: "contract", name: "合同纠纷", icon: "📝", desc: "合同起草、违约纠纷" },
  { id: "property", name: "房产纠纷", icon: "🏠", desc: "房屋买卖、租赁、物业" },
  { id: "criminal", name: "刑事辩护", icon: "⚖️", desc: "刑事辩护、取保候审" },
  { id: "company", name: "公司法务", icon: "🏢", desc: "公司设立、股权、合规" }
]

const stats = [
  { value: "10000+", label: "认证律师" },
  { value: "50000+", label: "服务用户" },
  { value: "98%", label: "好评率" },
  { value: "24h", label: "快速响应" }
]

function goToConsult() {
  router.push("/consultation")
}

function goToLawyers() {
  router.push("/lawyers")
}

function goToCategory(cat) {
  router.push({ path: "/lawyers", query: { category: cat.id } })
}

async function fetchRecommendedLawyers() {
  try {
    const res = await request.get("/lawyers", { params: { page: 1, pageSize: 4 } })
    recommendedLawyers.value = res.data?.items || []
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchRecommendedLawyers()
})
</script>

<style scoped>
.home-page {
  padding-bottom: 60px;
}
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 80px 0;
  text-align: center;
}
.hero-content h1 {
  font-size: 42px;
  margin: 0 0 20px;
}
.subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin: 0 0 40px;
}
.hero-actions .el-button + .el-button {
  margin-left: 20px;
}
.section-title {
  font-size: 28px;
  text-align: center;
  margin: 0 0 40px;
  color: #333;
}
.categories-section,
.lawyers-section,
.stats-section {
  padding: 60px 0;
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 20px;
  padding-right: 20px;
}
.category-card {
  text-align: center;
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.3s;
}
.category-card:hover {
  transform: translateY(-5px);
}
.cat-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.category-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #333;
}
.category-card p {
  margin: 0;
  color: #999;
  font-size: 14px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}
.section-header .section-title {
  margin: 0;
  text-align: left;
}
.stats-section {
  background: #f5f7fa;
  max-width: 100%;
  margin: 0;
  padding: 60px 20px;
}
.stat-item {
  text-align: center;
  padding: 20px;
}
.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}
.stat-label {
  font-size: 16px;
  color: #666;
}
</style>
