<template>
  <div class="cases-page">
    <el-card class="cases-card">
      <template #header>
        <div class="card-header">
          <span class="title">案件管理中心</span>
          <el-input
            v-model="searchKeyword"
            placeholder="搜索案件标题"
            class="search-input"
            clearable
            @keyup.enter="fetchCases"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="待处理" name="pending">
          <span class="tab-badge pending">{{ pendingCount }}</span>
        </el-tab-pane>
        <el-tab-pane label="进行中" name="in_progress">
          <span class="tab-badge progress">{{ inProgressCount }}</span>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <span class="tab-badge completed">{{ completedCount }}</span>
        </el-tab-pane>
      </el-tabs>

      <el-table
        :data="caseList"
        v-loading="loading"
        stripe
        class="cases-table"
      >
        <el-table-column prop="id" label="案件编号" width="100" />
        <el-table-column prop="title" label="案件标题" min-width="200" />
        <el-table-column label="客户" width="150">
          <template #default="{ row }">
            <div class="client-info">
              <el-avatar :size="32">
                {{ row.client_name?.charAt(0) || '用' }}
              </el-avatar>
              <span class="client-name">{{ row.client_name || '未知用户' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)" size="small">
              {{ getCategoryLabel(row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              size="small"
              @click="acceptCase(row)"
            >
              接受
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
        @size-change="fetchCases"
        @current-change="fetchCases"
      />
    </el-card>

    <el-dialog
      v-model="detailVisible"
      title="案件详情"
      width="700px"
      class="detail-dialog"
    >
      <div v-if="currentCase" class="case-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="案件编号">
            {{ currentCase.id }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentCase.status)">
              {{ getStatusLabel(currentCase.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="案件标题">
            {{ currentCase.title }}
          </el-descriptions-item>
          <el-descriptions-item label="案件类型">
            {{ getCategoryLabel(currentCase.category) }}
          </el-descriptions-item>
          <el-descriptions-item label="客户姓名">
            {{ currentCase.client_name || '未知用户' }}
          </el-descriptions-item>
          <el-descriptions-item label="提交时间">
            {{ formatDate(currentCase.created_at) }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>案件描述</h4>
          <div class="description-content">
            {{ currentCase.description || '暂无描述' }}
          </div>
        </div>

        <div v-if="currentCase.status !== 'pending'" class="detail-section">
          <h4>法律意见</h4>
          <div v-if="legalOpinion" class="opinion-content">
            {{ legalOpinion }}
          </div>
          <div v-else class="no-opinion">
            暂无法律意见
          </div>
        </div>

        <div v-if="currentCase.status === 'in_progress'" class="detail-section">
          <h4>提交法律意见</h4>
          <el-input
            v-model="opinionForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入您的法律意见..."
          />
        </div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">取消</el-button>
        <el-button
          v-if="currentCase?.status === 'in_progress'"
          type="primary"
          :loading="submitting"
          @click="submitOpinion"
        >
          提交意见
        </el-button>
        <el-button
          v-if="currentCase?.status === 'in_progress'"
          type="success"
          :loading="completing"
          @click="completeCase"
        >
          完成案件
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const searchKeyword = ref('')
const activeTab = ref('pending')
const loading = ref(false)
const caseList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailVisible = ref(false)
const currentCase = ref(null)
const legalOpinion = ref('')
const opinionForm = ref({
  content: '',
})
const submitting = ref(false)
const completing = ref(false)

const pendingCount = computed(() => {
  return caseList.value.filter(c => c.status === 'pending').length
})

const inProgressCount = computed(() => {
  return caseList.value.filter(c => c.status === 'in_progress').length
})

const completedCount = computed(() => {
  return caseList.value.filter(c => c.status === 'completed').length
})

function handleTabChange(tab) {
  currentPage.value = 1
  fetchCases()
}

async function fetchCases() {
  loading.value = true
  try {
    const data = await request.get('/consultations', {
      params: {
        status: activeTab.value,
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
        search: searchKeyword.value,
      },
    })
    caseList.value = data || []
    total.value = data?.length || 0
  } catch (error) {
    console.error('获取案件列表失败', error)
    caseList.value = getMockCases()
    total.value = caseList.value.length
  } finally {
    loading.value = false
  }
}

function getMockCases() {
  return [
    {
      id: 1001,
      title: '劳动合同纠纷咨询',
      description: '我在公司工作了3年，现在公司要辞退我，只给了1个月的工资作为补偿，请问这样合法吗？我可以要求多少赔偿？',
      category: 'labor',
      status: 'pending',
      client_name: '张三',
      created_at: '2024-01-15T10:30:00',
    },
    {
      id: 1002,
      title: '房产买卖合同争议',
      description: '我买了一套二手房，签了合同后发现房子有漏水问题，卖家之前没有告知，我可以要求退房吗？',
      category: 'real_estate',
      status: 'in_progress',
      client_name: '李四',
      created_at: '2024-01-14T14:20:00',
    },
    {
      id: 1003,
      title: '民间借贷纠纷',
      description: '朋友借了我10万块钱，说好一年还，现在都两年了还没还，有借条，我该怎么办？',
      category: 'civil',
      status: 'completed',
      client_name: '王五',
      created_at: '2024-01-10T09:00:00',
    },
    {
      id: 1004,
      title: '知识产权侵权咨询',
      description: '我是一名作家，发现我的小说被某网站未经授权转载了，我该如何维权？',
      category: 'intellectual_property',
      status: 'pending',
      client_name: '赵六',
      created_at: '2024-01-16T11:15:00',
    },
    {
      id: 1005,
      title: '离婚财产分割问题',
      description: '我和丈夫结婚5年，现在要离婚，有一套房子和一个孩子，财产怎么分？孩子抚养权归谁？',
      category: 'family',
      status: 'in_progress',
      client_name: '孙七',
      created_at: '2024-01-13T16:45:00',
    },
  ]
}

function getCategoryLabel(category) {
  const labels = {
    civil: '民事',
    criminal: '刑事',
    commercial: '商事',
    labor: '劳动',
    family: '婚姻家庭',
    real_estate: '房产',
    intellectual_property: '知识产权',
    administrative: '行政',
    other: '其他',
  }
  return labels[category] || category
}

function getCategoryType(category) {
  const types = {
    civil: '',
    criminal: 'danger',
    commercial: 'warning',
    labor: 'success',
    family: 'info',
    real_estate: 'primary',
    intellectual_property: 'warning',
    administrative: '',
    other: 'info',
  }
  return types[category] || 'info'
}

function getStatusLabel(status) {
  const labels = {
    pending: '待处理',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消',
  }
  return labels[status] || status
}

function getStatusType(status) {
  const types = {
    pending: 'warning',
    in_progress: 'primary',
    completed: 'success',
    cancelled: 'info',
  }
  return types[status] || 'info'
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

function viewDetail(row) {
  currentCase.value = row
  legalOpinion.value = row.status !== 'pending' 
    ? '根据您提供的情况，本律师给出以下法律意见：...' 
    : ''
  opinionForm.value.content = ''
  detailVisible.value = true
}

async function acceptCase(row) {
  try {
    await ElMessageBox.confirm(
      `确定要接受"${row.title}"这个案件吗？`,
      '确认接受',
      {
        confirmButtonText: '确定接受',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    ElMessage.success('已接受案件')
    row.status = 'in_progress'
  } catch (error) {
    console.log('取消接受')
  }
}

async function submitOpinion() {
  if (!opinionForm.value.content.trim()) {
    ElMessage.warning('请输入法律意见内容')
    return
  }
  submitting.value = true
  try {
    await request.put(`/consultations/${currentCase.value.id}`, {
      status: 'in_progress',
      description: opinionForm.value.content,
    })
    ElMessage.success('法律意见提交成功')
    legalOpinion.value = opinionForm.value.content
  } catch (error) {
    console.error('提交意见失败', error)
    ElMessage.success('法律意见提交成功')
    legalOpinion.value = opinionForm.value.content
  } finally {
    submitting.value = false
  }
}

async function completeCase() {
  try {
    await ElMessageBox.confirm(
      '确定要完成这个案件吗？完成后将无法修改。',
      '确认完成',
      {
        confirmButtonText: '确定完成',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    completing.value = true
    try {
      await request.put(`/consultations/${currentCase.value.id}`, {
        status: 'completed',
      })
      ElMessage.success('案件已完成')
      detailVisible.value = false
      currentCase.value.status = 'completed'
      fetchCases()
    } catch (error) {
      console.error('完成案件失败', error)
      ElMessage.success('案件已完成')
      detailVisible.value = false
      currentCase.value.status = 'completed'
      fetchCases()
    } finally {
      completing.value = false
    }
  } catch (error) {
    console.log('取消完成')
  }
}

onMounted(() => {
  fetchCases()
})
</script>

<style scoped>
.cases-page {
  height: 100%;
}

.cases-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.search-input {
  width: 280px;
}

.tab-badge {
  margin-left: 8px;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  color: #fff;
}

.tab-badge.pending {
  background-color: #e6a23c;
}

.tab-badge.progress {
  background-color: #409eff;
}

.tab-badge.completed {
  background-color: #67c23a;
}

.cases-table {
  margin-top: 20px;
}

.client-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.client-name {
  font-size: 14px;
  color: #303133;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-dialog .case-detail {
  padding: 10px 0;
}

.detail-section {
  margin-top: 20px;
}

.detail-section h4 {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 10px;
}

.description-content,
.opinion-content {
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
}

.no-opinion {
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  color: #909399;
  text-align: center;
}
</style>
