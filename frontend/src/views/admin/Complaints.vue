<template>
  <div class="complaints-page">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">投诉处理</span>
          <div class="header-actions">
            <el-select
              v-model="statusFilter"
              placeholder="筛选状态"
              size="default"
              style="width: 150px; margin-right: 10px"
              @change="fetchComplaints"
            >
              <el-option label="全部" value="" />
              <el-option label="待处理" value="pending" />
              <el-option label="处理中" value="processing" />
              <el-option label="已完成" value="resolved" />
              <el-option label="已关闭" value="closed" />
            </el-select>
            <el-input
              v-model="searchKeyword"
              placeholder="搜索投诉标题"
              style="width: 250px"
              clearable
              @keyup.enter="fetchComplaints"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </template>

      <el-table
        :data="complaintList"
        v-loading="loading"
        stripe
        class="complaint-table"
      >
        <el-table-column prop="id" label="编号" width="80" />
        <el-table-column prop="title" label="投诉标题" min-width="200" />
        <el-table-column label="投诉人" width="150">
          <template #default="{ row }">
            <div class="user-info">
              <el-avatar :size="32">
                {{ row.complainant_name?.charAt(0) || '用' }}
              </el-avatar>
              <span class="user-name">{{ row.complainant_name || '未知用户' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="target_type" label="投诉类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTargetType(row.target_type)" size="small">
              {{ getTargetLabel(row.target_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="投诉时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
            <el-button
              v-if="row.status === 'pending' || row.status === 'processing'"
              type="success"
              size="small"
              @click="handleComplaint(row)"
            >
              处理
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
        @size-change="fetchComplaints"
        @current-change="fetchComplaints"
      />
    </el-card>

    <el-dialog
      v-model="detailVisible"
      title="投诉详情"
      width="700px"
      class="detail-dialog"
    >
      <div v-if="currentComplaint" class="complaint-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="投诉编号">
            {{ currentComplaint.id }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentComplaint.status)">
              {{ getStatusLabel(currentComplaint.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="投诉标题">
            {{ currentComplaint.title }}
          </el-descriptions-item>
          <el-descriptions-item label="投诉类型">
            <el-tag :type="getTargetType(currentComplaint.target_type)">
              {{ getTargetLabel(currentComplaint.target_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="投诉人">
            {{ currentComplaint.complainant_name || '未知用户' }}
          </el-descriptions-item>
          <el-descriptions-item label="被投诉方">
            {{ currentComplaint.target_name || '未知' }}
          </el-descriptions-item>
          <el-descriptions-item label="投诉时间" :span="2">
            {{ formatDate(currentComplaint.created_at) }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>投诉内容</h4>
          <div class="content-text">
            {{ currentComplaint.content || '暂无内容' }}
          </div>
        </div>

        <div v-if="currentComplaint.reply" class="detail-section">
          <h4>处理回复</h4>
          <div class="reply-content">
            <p class="reply-text">{{ currentComplaint.reply }}</p>
            <p class="reply-time">
              处理时间：{{ formatDate(currentComplaint.handled_at) }}
            </p>
          </div>
        </div>

        <div
          v-if="currentComplaint.status === 'pending' || currentComplaint.status === 'processing'"
          class="detail-section"
        >
          <h4>处理回复</h4>
          <el-input
            v-model="replyForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入处理回复内容..."
          />
        </div>
      </div>

      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <template
          v-if="currentComplaint?.status === 'pending' || currentComplaint?.status === 'processing'"
        >
          <el-button type="warning" @click="markProcessing">
            标记处理中
          </el-button>
          <el-button type="primary" :loading="submitting" @click="submitReply">
            提交回复
          </el-button>
        </template>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const statusFilter = ref('')
const searchKeyword = ref('')
const loading = ref(false)
const complaintList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailVisible = ref(false)
const currentComplaint = ref(null)

const replyForm = ref({
  content: '',
})
const submitting = ref(false)

function getTargetLabel(type) {
  const labels = {
    lawyer: '投诉律师',
    user: '投诉用户',
    platform: '投诉平台',
    service: '服务投诉',
    other: '其他投诉',
  }
  return labels[type] || type
}

function getTargetType(type) {
  const types = {
    lawyer: 'warning',
    user: 'info',
    platform: 'danger',
    service: 'primary',
    other: '',
  }
  return types[type] || 'info'
}

function getStatusLabel(status) {
  const labels = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已完成',
    closed: '已关闭',
  }
  return labels[status] || status
}

function getStatusType(status) {
  const types = {
    pending: 'warning',
    processing: 'primary',
    resolved: 'success',
    closed: 'info',
  }
  return types[status] || 'info'
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function fetchComplaints() {
  loading.value = true
  try {
    const data = await request.get('/admin/complaints', {
      params: {
        status: statusFilter.value || undefined,
        search: searchKeyword.value || undefined,
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
      },
    })
    complaintList.value = data || getMockComplaints()
    total.value = complaintList.value.length
  } catch (error) {
    console.error('获取投诉列表失败', error)
    complaintList.value = getMockComplaints()
    total.value = complaintList.value.length
  } finally {
    loading.value = false
  }
}

function getMockComplaints() {
  return [
    {
      id: 1001,
      title: '律师服务态度差',
      content: '我预约了张律师的咨询，但是律师态度非常不好，对我的问题敷衍了事，没有给出专业的解答。我要求退款并投诉该律师。',
      target_type: 'lawyer',
      target_id: 1,
      target_name: '张三律师',
      complainant_id: 101,
      complainant_name: '李四',
      status: 'pending',
      reply: null,
      handled_at: null,
      created_at: '2024-01-16T10:30:00',
      updated_at: '2024-01-16T10:30:00',
    },
    {
      id: 1002,
      title: '预约后律师未按时出席',
      content: '我预约了昨天下午2点的线上咨询，但是等了半小时律师都没有上线，也没有提前通知我。这次预约给我造成了很大的不便。',
      target_type: 'lawyer',
      target_id: 2,
      target_name: '王五律师',
      complainant_id: 102,
      complainant_name: '赵六',
      status: 'processing',
      reply: '您好，我们已经收到您的投诉，正在与该律师核实情况，请您耐心等待。',
      handled_at: '2024-01-15T14:20:00',
      created_at: '2024-01-15T09:00:00',
      updated_at: '2024-01-15T14:20:00',
    },
    {
      id: 1003,
      title: '平台功能bug',
      content: '在使用支付功能时，页面出现了崩溃，导致我重复支付了两次费用。请尽快修复并退还我的款项。',
      target_type: 'platform',
      target_id: 0,
      target_name: '平台',
      complainant_id: 103,
      complainant_name: '孙七',
      status: 'resolved',
      reply: '您好，非常抱歉给您带来不便。我们已经确认了重复支付的问题，款项将在3个工作日内原路退回。感谢您的反馈！',
      handled_at: '2024-01-14T16:00:00',
      created_at: '2024-01-14T10:15:00',
      updated_at: '2024-01-14T16:00:00',
    },
    {
      id: 1004,
      title: '咨询费用不合理',
      content: '咨询费用太贵了，而且咨询时间很短，感觉不值这个价格。希望平台能够调整收费标准。',
      target_type: 'service',
      target_id: 0,
      target_name: '咨询服务',
      complainant_id: 104,
      complainant_name: '周八',
      status: 'pending',
      reply: null,
      handled_at: null,
      created_at: '2024-01-16T11:45:00',
      updated_at: '2024-01-16T11:45:00',
    },
    {
      id: 1005,
      title: '律师信息不真实',
      content: '我发现平台上某位律师的介绍信息与实际不符，声称有10年执业经验，但实际上只有3年。这属于虚假宣传。',
      target_type: 'lawyer',
      target_id: 3,
      target_name: '吴九律师',
      complainant_id: 105,
      complainant_name: '郑十',
      status: 'closed',
      reply: '您好，感谢您的监督。我们已经核实了该律师的信息，并对其资料进行了更正。平台会加强对律师信息的审核，避免类似问题再次发生。',
      handled_at: '2024-01-12T15:30:00',
      created_at: '2024-01-11T14:00:00',
      updated_at: '2024-01-12T15:30:00',
    },
  ]
}

function viewDetail(row) {
  currentComplaint.value = { ...row }
  replyForm.value.content = ''
  detailVisible.value = true
}

function handleComplaint(row) {
  viewDetail(row)
}

async function markProcessing() {
  try {
    await request.put(`/admin/complaints/${currentComplaint.value.id}`, {
      status: 'processing',
    })
    ElMessage.success('已标记为处理中')
    currentComplaint.value.status = 'processing'
    const complaint = complaintList.value.find(c => c.id === currentComplaint.value.id)
    if (complaint) {
      complaint.status = 'processing'
    }
  } catch (error) {
    console.error('标记失败', error)
    ElMessage.error('标记失败')
  }
}
async function submitReply() {
  if (!replyForm.value.content.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  submitting.value = true
  try {
    await request.put(`/admin/complaints/${currentComplaint.value.id}`, {
      status: 'resolved',
      reply: replyForm.value.content,
    })
    ElMessage.success('回复提交成功')
    currentComplaint.value.reply = replyForm.value.content
    currentComplaint.value.status = 'resolved'
    currentComplaint.value.handled_at = new Date().toISOString()
    const complaint = complaintList.value.find(c => c.id === currentComplaint.value.id)
    if (complaint) {
      complaint.status = 'resolved'
      complaint.reply = replyForm.value.content
      complaint.handled_at = currentComplaint.value.handled_at
    }
  } catch (error) {
    console.error('提交回复失败', error)
    ElMessage.error('提交回复失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchComplaints()
})
</script>

<style scoped>
.complaints-page {
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

.header-actions {
  display: flex;
  align-items: center;
}

.complaint-table {
  margin-top: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-name {
  font-size: 14px;
  color: #303133;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-dialog .complaint-detail {
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

.content-text {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
}

.reply-content {
  padding: 15px;
  background-color: #f0f9eb;
  border-radius: 4px;
  border-left: 4px solid #67c23a;
}

.reply-text {
  margin: 0 0 10px 0;
  line-height: 1.6;
  color: #303133;
}

.reply-time {
  margin: 0;
  font-size: 12px;
  color: #909399;
  text-align: right;
}
</style>
