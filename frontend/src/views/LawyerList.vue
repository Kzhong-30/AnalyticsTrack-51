<template>
  <div class="lawyer-list-page">
    <div class="filter-bar">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="领域">
          <el-select v-model="filterForm.category" placeholder="全部领域" clearable style="width: 150px">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="城市">
          <el-select v-model="filterForm.city" placeholder="全部城市" clearable style="width: 150px">
            <el-option v-for="city in cities" :key="city" :label="city" :value="city" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-select v-model="filterForm.sort" style="width: 150px">
            <el-option label="综合排序" value="default" />
            <el-option label="评分最高" value="rating" />
            <el-option label="价格最低" value="price" />
            <el-option label="经验最多" value="experience" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchLawyers">搜索</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="lawyer-list">
      <el-row :gutter="20">
        <el-col :span="6" v-for="lawyer in lawyers" :key="lawyer.id">
          <LawyerCard :lawyer="lawyer" />
        </el-col>
      </el-row>
      <div v-if="lawyers.length === 0" class="empty-state">
        <el-empty description="暂无律师数据" />
      </div>
    </div>
    <div class="pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[8, 16, 24, 32]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchLawyers"
        @current-change="fetchLawyers"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRoute } from "vue-router"
import LawyerCard from "../components/LawyerCard.vue"
import request from "../utils/request"

const route = useRoute()
const lawyers = ref([])
const loading = ref(false)

const filterForm = reactive({
  category: "",
  city: "",
  sort: "default"
})

const pagination = reactive({
  page: 1,
  pageSize: 8,
  total: 0
})

const categories = [
  { id: "marriage", name: "婚姻家庭" },
  { id: "labor", name: "劳动纠纷" },
  { id: "contract", name: "合同纠纷" },
  { id: "property", name: "房产纠纷" },
  { id: "criminal", name: "刑事辩护" },
  { id: "company", name: "公司法务" }
]

const cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "重庆"]

async function fetchLawyers() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize
    }
    if (filterForm.category) params.category = filterForm.category
    if (filterForm.city) params.city = filterForm.city
    if (filterForm.sort) params.sort = filterForm.sort
    const res = await request.get("/lawyers", { params })
    lawyers.value = res.data?.items || []
    pagination.total = res.data?.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (route.query.category) filterForm.category = route.query.category
  if (route.query.city) filterForm.city = route.query.city
  fetchLawyers()
})
</script>

<style scoped>
.lawyer-list-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}
.filter-bar {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.lawyer-list {
  min-height: 400px;
}
.empty-state {
  padding: 60px 0;
}
.pagination {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}
</style>
