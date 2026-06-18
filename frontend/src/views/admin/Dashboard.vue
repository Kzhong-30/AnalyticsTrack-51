<template>
  <div class="dashboard-page">
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon user-icon">
              <el-icon :size="36"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_users }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><Top /></el-icon>
              12%
            </span>
            <span class="stat-text">较上月</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon lawyer-icon">
              <el-icon :size="36"><Avatar /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_lawyers }}</div>
              <div class="stat-label">律师总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><Top /></el-icon>
              8%
            </span>
            <span class="stat-text">较上月</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon consult-icon">
              <el-icon :size="36"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_consultations }}</div>
              <div class="stat-label">咨询总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><Top /></el-icon>
              25%
            </span>
            <span class="stat-text">较上月</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon appt-icon">
              <el-icon :size="36"><Calendar /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_appointments }}</div>
              <div class="stat-label">预约总数</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-trend up">
              <el-icon><Top /></el-icon>
              15%
            </span>
            <span class="stat-text">较上月</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-content">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>数据趋势</span>
              <el-radio-group v-model="chartPeriod" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
                <el-radio-button label="year">本年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <div class="chart-placeholder">
              <div class="chart-bars">
                <div
                  v-for="(item, index) in chartData"
                  :key="index"
                  class="chart-bar-wrapper"
                >
                  <div class="chart-bar" :style="{ height: item.value + '%' }"></div>
                  <div class="chart-label">{{ item.label }}</div>
                </div>
              </div>
              <div class="chart-legend">
                <span class="legend-item">
                  <span class="legend-dot blue"></span>
                  咨询量
                </span>
                <span class="legend-item">
                  <span class="legend-dot green"></span>
                  预约量
                </span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" class="todo-card">
          <template #header>
            <div class="card-header">
              <span>待办事项</span>
              <el-button type="primary" link size="small" @click="goToVerifications">
                查看全部
              </el-button>
            </div>
          </template>
          <div class="todo-list">
            <div class="todo-item" @click="goToVerifications">
              <div class="todo-icon pending">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="todo-info">
                <div class="todo-title">待审核律师</div>
                <div class="todo-desc">{{ pendingLawyers }} 位律师等待审核</div>
              </div>
              <el-badge :value="pendingLawyers" class="todo-badge" />
            </div>
            <div class="todo-item" @click="goToComplaints">
              <div class="todo-icon warning">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="todo-info">
                <div class="todo-title">待处理投诉</div>
                <div class="todo-desc">{{ pendingComplaints }} 条投诉待处理</div>
              </div>
              <el-badge :value="pendingComplaints" class="todo-badge" />
            </div>
            <div class="todo-item">
              <div class="todo-icon info">
                <el-icon><Document /></el-icon>
              </div>
              <div class="todo-info">
                <div class="todo-title">待发布知识</div>
                <div class="todo-desc">3 条知识条目待审核</div>
              </div>
              <el-badge :value="3" class="todo-badge" />
            </div>
          </div>
        </el-card>

        <el-card shadow="never" class="quick-actions" style="margin-top: 20px;">
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="action-grid">
            <div class="action-item" @click="goToVerifications">
              <el-icon :size="24" color="#409EFF"><CircleCheck /></el-icon>
              <span>资质审核</span>
            </div>
            <div class="action-item" @click="goToComplaints">
              <el-icon :size="24" color="#e6a23c"><Warning /></el-icon>
              <span>投诉处理</span>
            </div>
            <div class="action-item">
              <el-icon :size="24" color="#67c23a"><DocumentAdd /></el-icon>
              <span>发布知识</span>
            </div>
            <div class="action-item">
              <el-icon :size="24" color="#f56c6c"><Files /></el-icon>
              <span>模板管理</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
              <el-button type="primary" link size="small">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentActivities" stripe>
            <el-table-column prop="type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getActivityType(row.type)" size="small">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="内容" min-width="300" />
            <el-table-column prop="user" label="操作人" width="150" />
            <el-table-column prop="time" label="时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.time) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewActivity(row)">
                  查看
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const router = useRouter()

const stats = ref({
  total_users: 0,
  total_lawyers: 0,
  total_consultations: 0,
  total_appointments: 0,
})

const pendingLawyers = ref(0)
const pendingComplaints = ref(0)
const chartPeriod = ref('week')
const loading = ref(false)

const chartData = ref([
  { label: '周一', value: 30 },
  { label: '周二', value: 45 },
  { label: '周三', value: 60 },
  { label: '周四', value: 40 },
  { label: '周五', value: 70 },
  { label: '周六', value: 55 },
  { label: '周日', value: 35 },
])

const recentActivities = ref([
  {
    id: 1,
    type: '注册',
    content: '新用户 张三 完成注册',
    user: '系统',
    time: '2024-01-16 15:30:00',
  },
  {
    id: 2,
    type: '咨询',
    content: '用户 李四 提交了法律咨询',
    user: '李四',
    time: '2024-01-16 14:20:00',
  },
  {
    id: 3,
    type: '预约',
    content: '用户 王五 预约了律师 赵六',
    user: '王五',
    time: '2024-01-16 12:15:00',
  },
  {
    id: 4,
    type: '审核',
    content: '律师 孙七 的资质申请待审核',
    user: '系统',
    time: '2024-01-16 10:00:00',
  },
  {
    id: 5,
    type: '投诉',
    content: '用户 周八 投诉律师 吴九',
    user: '周八',
    time: '2024-01-15 18:45:00',
  },
  {
    id: 6,
    type: '注册',
    content: '新律师 郑十 提交资质申请',
    user: '系统',
    time: '2024-01-15 16:30:00',
  },
])

function getActivityType(type) {
  const types = {
    注册: 'success',
    咨询: 'primary',
    预约: 'warning',
    审核: 'info',
    投诉: 'danger',
  }
  return types[type] || 'info'
}

function formatTime(time) {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

async function fetchStats() {
  loading.value = true
  try {
    const data = await request.get('/admin/stats')
    stats.value = {
      total_users: data.total_users || 0,
      total_lawyers: data.total_lawyers || 0,
      total_consultations: data.total_consultations || 0,
      total_appointments: data.total_appointments || 0,
    }
    pendingLawyers.value = data.pending_lawyers || 0
    pendingComplaints.value = data.pending_complaints || 0
  } catch (error) {
    console.error('获取统计数据失败', error)
  } finally {
    loading.value = false
  }
}

function goToVerifications() {
  router.push('/admin/verifications')
}

function goToComplaints() {
  router.push('/admin/complaints')
}

function viewActivity(row) {
  ElMessage.info(`查看活动：${row.content}`)
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-cards {
  margin-bottom: 0;
}

.stat-card {
  border-radius: 8px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.user-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.lawyer-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.consult-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.appt-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.stat-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  border-top: 1px solid #f0f2f5;
  padding-top: 12px;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 500;
}

.stat-trend.up {
  color: #67c23a;
}

.stat-text {
  font-size: 13px;
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 20px;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-bars {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: 20px;
  padding: 20px 0;
}

.chart-bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.chart-bar {
  width: 60%;
  background: linear-gradient(180deg, #409eff 0%, #66b1ff 100%);
  border-radius: 4px 4px 0 0;
  min-height: 10px;
  transition: height 0.3s ease;
}

.chart-label {
  font-size: 12px;
  color: #909399;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding-top: 16px;
  border-top: 1px solid #f0f2f5;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-dot.blue {
  background-color: #409eff;
}

.legend-dot.green {
  background-color: #67c23a;
}

.todo-card {
  height: fit-content;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.todo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.todo-item:hover {
  background-color: #ecf5ff;
}

.todo-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
}

.todo-icon.pending {
  background-color: #e6a23c;
}

.todo-icon.warning {
  background-color: #f56c6c;
}

.todo-icon.info {
  background-color: #409eff;
}

.todo-info {
  flex: 1;
}

.todo-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.todo-desc {
  font-size: 12px;
  color: #909399;
}

.todo-badge {
  flex-shrink: 0;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 8px;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background-color: #ecf5ff;
  transform: translateY(-2px);
}

.action-item span {
  font-size: 13px;
  color: #606266;
}
</style>
