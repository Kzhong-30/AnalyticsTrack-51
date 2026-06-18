<template>
  <div class="appointment-list-page">
    <h1 class="page-title">我的预约</h1>
    <el-tabs v-model="activeTab" class="appointment-tabs">
      <el-tab-pane label="即将到来" name="upcoming">
        <div class="appointment-list">
          <div v-if="upcomingAppointments.length === 0" class="empty-state">
            <el-empty description="暂无即将到来的预约" />
          </div>
          <div v-for="appt in upcomingAppointments" :key="appt.id" class="appointment-card">
            <div class="card-header">
              <el-avatar :size="50" >{{ (appt.lawyer_name || '律师').charAt(0) }}</el-avatar>
              <div class="lawyer-info">
                <h3>{{ appt.lawyer_name || '律师' }}</h3>
                <p>{{ appt.lawyer_firm || '' }}</p>
              </div>
              <el-tag :type="getStatusType(appt.status)" class="status-tag">{{ getStatusText(appt.status) }}</el-tag>
            </div>
            <div class="card-body">
              <div class="info-row">
                <span class="label">咨询方式：</span>
                <span class="value">{{ getTypeText(appt.appointment_type) }}</span>
              </div>
              <div class="info-row">
                <span class="label">预约时间：</span>
                <span class="value">{{ appt.appointment_date + ' ' + appt.start_time }}</span>
              </div>
            </div>
            <div class="card-footer">
              <el-button v-if="appt.status === 'pending'" type="danger" size="small" @click="cancelAppointment(appt.id)">取消预约</el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="历史记录" name="history">
        <div class="appointment-list">
          <div v-if="historyAppointments.length === 0" class="empty-state">
            <el-empty description="暂无历史预约记录" />
          </div>
          <div v-for="appt in historyAppointments" :key="appt.id" class="appointment-card">
            <div class="card-header">
              <el-avatar :size="50" >{{ (appt.lawyer_name || '律师').charAt(0) }}</el-avatar>
              <div class="lawyer-info">
                <h3>{{ appt.lawyer_name || '律师' }}</h3>
                <p>{{ appt.lawyer_firm || '' }}</p>
              </div>
              <el-tag :type="getStatusType(appt.status)" class="status-tag">{{ getStatusText(appt.status) }}</el-tag>
            </div>
            <div class="card-body">
              <div class="info-row">
                <span class="label">咨询方式：</span>
                <span class="value">{{ getTypeText(appt.appointment_type) }}</span>
              </div>
              <div class="info-row">
                <span class="label">预约时间：</span>
                <span class="value">{{ appt.appointment_date + ' ' + appt.start_time }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { ElMessage, ElMessageBox } from "element-plus"
import request from "../utils/request"

const activeTab = ref("upcoming")
const appointments = ref([])
const loading = ref(false)

const upcomingAppointments = computed(() => {
  return appointments.value.filter(a => [
    "pending", "confirmed"
  ].includes(a.status))
})

const historyAppointments = computed(() => {
  return appointments.value.filter(a => [
    "completed", "cancelled", "rejected"
  ].includes(a.status))
})

function getStatusType(status) {
  const map = {
    pending: "warning",
    confirmed: "success",
    completed: "info",
    cancelled: "danger",
    rejected: "danger"
  }
  return map[status] || "info"
}

function getStatusText(status) {
  const map = {
    pending: "待确认",
    confirmed: "已确认",
    completed: "已完成",
    cancelled: "已取消",
    rejected: "已拒绝"
  }
  return map[status] || status
}

function getTypeText(type) {
  const map = {
    text: "文字咨询",
    voice: "语音咨询",
    video: "视频咨询"
  }
  return map[type] || type
}

async function fetchAppointments() {
  loading.value = true
  try {
    const res = await request.get("/appointments")
    appointments.value = Array.isArray(res) ? res : []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function cancelAppointment(id) {
  try {
    await ElMessageBox.confirm("确定要取消这个预约吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning"
    })
    await request.put('/appointments/' + id, { status: 'cancelled' })
    ElMessage.success("预约已取消")
    fetchAppointments()
  } catch (e) {
    if (e !== "cancel") console.error(e)
  }
}

onMounted(() => {
  fetchAppointments()
})
</script>

<style scoped>
.appointment-list-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px 20px;
}
.page-title {
  font-size: 28px;
  margin: 0 0 30px;
  color: #333;
}
.appointment-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.appointment-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  transition: box-shadow 0.3s;
}
.appointment-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}
.lawyer-info {
  flex: 1;
}
.lawyer-info h3 {
  margin: 0 0 5px;
  font-size: 18px;
  color: #333;
}
.lawyer-info p {
  margin: 0;
  color: #999;
  font-size: 14px;
}
.status-tag {
  align-self: flex-start;
}
.card-body {
  margin-bottom: 15px;
}
.info-row {
  display: flex;
  margin-bottom: 8px;
  font-size: 14px;
}
.info-row .label {
  color: #999;
  min-width: 80px;
}
.info-row .value {
  color: #333;
  flex: 1;
}
.card-footer {
  text-align: right;
}
.empty-state {
  padding: 60px 0;
}
</style>
