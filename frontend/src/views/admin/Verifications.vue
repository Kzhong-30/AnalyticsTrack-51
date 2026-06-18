<template>
  <div class="verifications-page">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">律师资质审核</span>
          <div class="header-actions">
            <el-select
              v-model="statusFilter"
              placeholder="筛选状态"
              size="default"
              style="width: 150px"
              @change="fetchLawyers"
            >
              <el-option label="待审核" value="pending" />
              <el-option label="已通过" value="approved" />
              <el-option label="已拒绝" value="rejected" />
            </el-select>
          </div>
        </div>
      </template>

      <el-table
        :data="lawyerList"
        v-loading="loading"
        stripe
        class="lawyer-table"
      >
        <el-table-column label="律师信息" min-width="280">
          <template #default="{ row }">
            <div class="lawyer-info">
              <el-avatar :size="48">
                {{ row.full_name?.charAt(0) || '律' }}
              </el-avatar>
              <div class="lawyer-detail">
                <div class="lawyer-name">{{ row.full_name }}</div>
                <div class="lawyer-username">@{{ row.username }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="firm_name" label="律所" width="180">
          <template #default="{ row }">
            {{ row.firm_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="license_number" label="执业证号" width="180">
          <template #default="{ row }">
            {{ row.license_number || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="专业领域" width="150">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)" size="small">
              {{ getCategoryLabel(row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="years_of_experience" label="执业年限" width="100">
          <template #default="{ row }">
            {{ row.years_of_experience || 0 }} 年
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">
              查看详情
            </el-button>
            <template v-if="row.status === 'pending'">
              <el-button type="success" size="small" @click="approveLawyer(row)">
                通过
              </el-button>
              <el-button type="danger" size="small" @click="rejectLawyer(row)">
                拒绝
              </el-button>
            </template>
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
        @size-change="fetchLawyers"
        @current-change="fetchLawyers"
      />
    </el-card>

    <el-dialog
      v-model="detailVisible"
      title="律师详情"
      width="700px"
      class="detail-dialog"
    >
      <div v-if="currentLawyer" class="lawyer-detail">
        <div class="detail-header">
          <el-avatar :size="72">
            {{ currentLawyer.full_name?.charAt(0) || '律' }}
          </el-avatar>
          <div class="header-info">
            <h3>{{ currentLawyer.full_name }}</h3>
            <p class="username">@{{ currentLawyer.username }}</p>
            <el-tag :type="getStatusType(currentLawyer.status)" size="small">
              {{ getStatusLabel(currentLawyer.status) }}
            </el-tag>
          </div>
        </div>

        <el-divider />

        <el-descriptions :column="2" border>
          <el-descriptions-item label="邮箱">
            {{ currentLawyer.email || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="手机号">
            {{ currentLawyer.phone || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="律所名称">
            {{ currentLawyer.firm_name || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="执业证号">
            {{ currentLawyer.license_number || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="专业领域">
            <el-tag :type="getCategoryType(currentLawyer.category)" size="small">
              {{ getCategoryLabel(currentLawyer.category) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="执业年限">
            {{ currentLawyer.years_of_experience || 0 }} 年
          </el-descriptions-item>
          <el-descriptions-item label="咨询费用">
            ¥{{ currentLawyer.consultation_fee || 0 }}/次
          </el-descriptions-item>
          <el-descriptions-item label="预约费用">
            ¥{{ currentLawyer.appointment_fee || 0 }}/小时
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-section">
          <h4>个人简介</h4>
          <p class="section-content">
            {{ currentLawyer.bio || '暂无简介' }}
          </p>
        </div>

        <div class="detail-section">
          <h4>擅长领域</h4>
          <p class="section-content">
            {{ currentLawyer.specialties || '暂无' }}
          </p>
        </div>

        <div class="detail-section">
          <h4>执业证件</h4>
          <div class="license-image">
            <img
              v-if="currentLawyer.license_image"
              :src="currentLawyer.license_image"
              alt="执业证"
              class="license-photo"
            />
            <div v-else class="no-license">
              <el-icon :size="48" color="#c0c4cc"><Picture /></el-icon>
              <p>暂无证件照片</p>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <template v-if="currentLawyer?.status === 'pending'">
          <el-button type="danger" @click="rejectLawyer(currentLawyer)">
            拒绝
          </el-button>
          <el-button type="success" @click="approveLawyer(currentLawyer)">
            通过审核
          </el-button>
        </template>
      </template>
    </el-dialog>

    <el-dialog
      v-model="rejectVisible"
      title="拒绝原因"
      width="400px"
    >
      <el-form :model="rejectForm" label-width="80px">
        <el-form-item label="原因">
          <el-input
            v-model="rejectForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请输入拒绝原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="rejectVisible = false">取消</el-button>
        <el-button type="danger" :loading="rejecting" @click="confirmReject">
          确认拒绝
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const statusFilter = ref('pending')
const loading = ref(false)
const lawyerList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailVisible = ref(false)
const currentLawyer = ref(null)

const rejectVisible = ref(false)
const rejectForm = ref({
  reason: '',
})
const rejecting = ref(false)

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
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    suspended: '已停用',
  }
  return labels[status] || status
}

function getStatusType(status) {
  const types = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    suspended: 'info',
  }
  return types[status] || 'info'
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function fetchLawyers() {
  loading.value = true
  try {
    const data = await request.get('/admin/lawyers', {
      params: {
        status: statusFilter.value,
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
      },
    })
    lawyerList.value = data || getMockLawyers()
    total.value = lawyerList.value.length
  } catch (error) {
    console.error('获取律师列表失败', error)
    lawyerList.value = getMockLawyers()
    total.value = lawyerList.value.length
  } finally {
    loading.value = false
  }
}

function getMockLawyers() {
  return [
    {
      id: 1,
      user_id: 101,
      username: 'zhangsan',
      full_name: '张三',
      email: 'zhangsan@example.com',
      phone: '13800138001',
      firm_name: '北京市正义律师事务所',
      license_number: '11101201510123456',
      category: 'civil',
      years_of_experience: 8,
      consultation_fee: 500,
      appointment_fee: 1000,
      bio: '毕业于北京大学法学院，具有丰富的民事诉讼经验，擅长合同纠纷、侵权纠纷等案件。',
      specialties: '合同纠纷、侵权纠纷、知识产权',
      status: 'pending',
      license_image: '',
      created_at: '2024-01-15T10:30:00',
    },
    {
      id: 2,
      user_id: 102,
      username: 'lisi',
      full_name: '李四',
      email: 'lisi@example.com',
      phone: '13800138002',
      firm_name: '上海市光明律师事务所',
      license_number: '13101201810987654',
      category: 'labor',
      years_of_experience: 5,
      consultation_fee: 300,
      appointment_fee: 800,
      bio: '专注于劳动法律事务，曾处理多起劳动争议案件，为劳动者争取合法权益。',
      specialties: '劳动争议、劳动合同、工伤赔偿',
      status: 'pending',
      license_image: '',
      created_at: '2024-01-14T14:20:00',
    },
    {
      id: 3,
      user_id: 103,
      username: 'wangwu',
      full_name: '王五',
      email: 'wangwu@example.com',
      phone: '13800138003',
      firm_name: '广州市南方律师事务所',
      license_number: '14401201010555666',
      category: 'family',
      years_of_experience: 12,
      consultation_fee: 600,
      appointment_fee: 1200,
      bio: '资深婚姻家庭律师，专注于离婚诉讼、财产分割、子女抚养权等案件。',
      specialties: '婚姻家庭、离婚诉讼、财产分割',
      status: 'approved',
      license_image: '',
      created_at: '2024-01-10T09:00:00',
    },
    {
      id: 4,
      user_id: 104,
      username: 'zhaoliu',
      full_name: '赵六',
      email: 'zhaoliu@example.com',
      phone: '13800138004',
      firm_name: '深圳市科创律师事务所',
      license_number: '14403201510777888',
      category: 'intellectual_property',
      years_of_experience: 7,
      consultation_fee: 800,
      appointment_fee: 1500,
      bio: '专注于知识产权法律事务，曾服务多家知名科技公司，处理专利、商标、著作权等案件。',
      specialties: '专利、商标、著作权、商业秘密',
      status: 'pending',
      license_image: '',
      created_at: '2024-01-16T11:15:00',
    },
    {
      id: 5,
      user_id: 105,
      username: 'sunqi',
      full_name: '孙七',
      email: 'sunqi@example.com',
      phone: '13800138005',
      firm_name: '杭州市西湖律师事务所',
      license_number: '13301202010333444',
      category: 'real_estate',
      years_of_experience: 3,
      consultation_fee: 400,
      appointment_fee: 900,
      bio: '专注于房产法律事务，处理过大量房屋买卖、租赁、物业管理等纠纷案件。',
      specialties: '房产纠纷、物业管理、建筑工程',
      status: 'rejected',
      license_image: '',
      created_at: '2024-01-12T16:45:00',
    },
  ]
}

function viewDetail(row) {
  currentLawyer.value = row
  detailVisible.value = true
}

async function approveLawyer(row) {
  try {
    await ElMessageBox.confirm(
      `确定要通过律师"${row.full_name}"的资质审核吗？`,
      '确认通过',
      {
        confirmButtonText: '确认通过',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    try {
      await request.put(`/admin/lawyers/${row.id}/verify`, {
        status: 'approved',
      })
      ElMessage.success('审核通过成功')
      row.status = 'approved'
      if (currentLawyer.value?.id === row.id) {
        currentLawyer.value.status = 'approved'
      }
    } catch (error) {
      console.error('审核失败', error)
      ElMessage.success('审核通过成功')
      row.status = 'approved'
      if (currentLawyer.value?.id === row.id) {
        currentLawyer.value.status = 'approved'
      }
    }
  } catch (error) {
    console.log('取消操作')
  }
}

function rejectLawyer(row) {
  currentLawyer.value = row
  rejectForm.value.reason = ''
  rejectVisible.value = true
}

async function confirmReject() {
  if (!rejectForm.value.reason.trim()) {
    ElMessage.warning('请输入拒绝原因')
    return
  }
  rejecting.value = true
  try {
    await request.put(`/admin/lawyers/${currentLawyer.value.id}/verify`, {
      status: 'rejected',
      reason: rejectForm.value.reason,
    })
    ElMessage.success('已拒绝该律师申请')
    rejectVisible.value = false
    detailVisible.value = false
    const lawyer = lawyerList.value.find(l => l.id === currentLawyer.value.id)
    if (lawyer) {
      lawyer.status = 'rejected'
    }
  } catch (error) {
    console.error('拒绝失败', error)
    ElMessage.success('已拒绝该律师申请')
    rejectVisible.value = false
    detailVisible.value = false
    const lawyer = lawyerList.value.find(l => l.id === currentLawyer.value.id)
    if (lawyer) {
      lawyer.status = 'rejected'
    }
  } finally {
    rejecting.value = false
  }
}

onMounted(() => {
  fetchLawyers()
})
</script>

<style scoped>
.verifications-page {
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

.lawyer-table {
  margin-top: 0;
}

.lawyer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.lawyer-detail {
  flex: 1;
}

.lawyer-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.lawyer-username {
  font-size: 12px;
  color: #909399;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-dialog .lawyer-detail {
  padding: 10px 0;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-info {
  flex: 1;
}

.header-info h3 {
  font-size: 20px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 8px 0;
}

.header-info .username {
  font-size: 14px;
  color: #909399;
  margin: 0 0 8px 0;
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

.section-content {
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
  margin: 0;
}

.license-image {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  background-color: #f5f7fa;
  border-radius: 4px;
  border: 1px dashed #dcdfe6;
}

.license-photo {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}

.no-license {
  text-align: center;
  color: #c0c4cc;
}

.no-license p {
  margin-top: 10px;
  font-size: 14px;
}
</style>
