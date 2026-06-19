<template>
  <div class="lawyer-detail-page" v-loading="loading">
    <div class="lawyer-header">
      <div class="lawyer-avatar">
        <el-avatar :size="100" :src="lawyer.avatar">{{ lawyer.full_name?.charAt(0) }}</el-avatar>
      </div>
      <div class="lawyer-info">
        <h1 class="lawyer-name">{{ lawyer.full_name }}</h1>
        <div class="lawyer-meta">
          <span class="firm">{{ lawyer.firm_name }}</span>
          <span class="rating">
            <el-rate v-model="lawyer.rating" disabled show-score text-color="#ff9900" />
          </span>
          <span class="experience">执业{{ lawyer.years_of_experience }}年</span>
        </div>
        <div class="lawyer-tags">
          <el-tag v-for="tag in (lawyer.specialties || '').split(',').filter(s => s.trim())" :key="tag" type="info" style="margin-right: 8px;">{{ tag }}</el-tag>
        </div>
      </div>
      <div class="lawyer-price">
        <div class="price">¥{{ lawyer.consultation_fee }}<span>/次</span></div>
        <div class="price-label">咨询费用</div>
      </div>
    </div>
    <div class="appointment-section">
      <h2>预约咨询</h2>
      <div class="consult-types">
        <div class="consult-type" :class="{ active: consultType === 'text' }" @click="consultType = 'text'">
          <div class="type-icon">💬</div>
          <h3>文字咨询</h3>
          <p>在线文字交流</p>
          <div class="type-price">¥{{ lawyer.consultation_fee || 0 }}/次</div>
        </div>
        <div class="consult-type" :class="{ active: consultType === 'voice' }" @click="consultType = 'voice'">
          <div class="type-icon">🎙️</div>
          <h3>语音咨询</h3>
          <p>语音通话</p>
          <div class="type-price">¥{{ lawyer.appointment_fee || 0 }}/次</div>
        </div>
        <div class="consult-type" :class="{ active: consultType === 'video' }" @click="consultType = 'video'">
          <div class="type-icon">📹</div>
          <h3>视频咨询</h3>
          <p>视频面对面</p>
          <div class="type-price">¥{{ lawyer.appointment_fee || 0 }}/次</div>
        </div>
      </div>
      <div class="time-slots">
        <h3>选择时段</h3>
        <div class="slot-list">
          <div
            v-for="slot in availableSlots"
            :key="slot"
            class="time-slot"
            :class="{ active: selectedTime === slot }"
            @click="selectTime(slot)"
          >
            {{ slot }}
          </div>
        </div>
      </div>
      <div class="appointment-actions">
        <el-button type="primary" size="large" :disabled="!selectedTime" :loading="submitting" @click="handleAppointment">
          确认预约
        </el-button>
      </div>
    </div>
    <el-tabs v-model="activeTab" class="detail-tabs">
      <el-tab-pane label="执业资料" name="profile">
        <div class="profile-content">
          <h3>个人简介</h3>
          <p>{{ lawyer.bio || "暂无简介" }}</p>
          <h3>擅长领域</h3>
          <div class="specialties">
            <el-tag v-for="tag in (lawyer.specialties || '').split(',').filter(s => s.trim())" :key="tag" size="large" style="margin-right: 10px; margin-bottom: 10px;">{{ tag }}</el-tag>
          </div>
          <h3>执业信息</h3>
          <ul class="info-list">
            <li><span>执业证号：</span>{{ lawyer.license_number || "暂无" }}</li>
            <li><span>所属律所：</span>{{ lawyer.firm_name || "暂无" }}</li>
            <li><span>执业年限：</span>{{ lawyer.years_of_experience || 0 }}年</li>
          </ul>
        </div>
      </el-tab-pane>
      <el-tab-pane label="客户评价" name="reviews">
        <div class="reviews-list">
          <div v-if="reviews.length === 0" class="empty-reviews">
            <el-empty description="暂无评价" />
          </div>
          <div v-for="review in reviews" :key="review.id" class="review-item">
            <div class="review-header">
              <el-avatar :size="40" :src="review.userAvatar">{{ review.userName?.charAt(0) }}</el-avatar>
              <div class="review-info">
                <div class="user-name">{{ review.userName }}</div>
                <el-rate v-model="review.rating" disabled size="small" />
              </div>
              <div class="review-date">{{ review.createdAt }}</div>
            </div>
            <div class="review-content">{{ review.content }}</div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRoute } from "vue-router"
import { ElMessage } from "element-plus"
import request from "../utils/request"

const route = useRoute()
const lawyerId = route.params.id
const loading = ref(false)
const submitting = ref(false)
const activeTab = ref("profile")
const consultType = ref("text")
const selectedTime = ref("")

const lawyer = reactive({
  id: null,
  full_name: "",
  avatar: "",
  firm_name: "",
  rating: 0,
  review_count: 0,
  years_of_experience: 0,
  specialties: "",
  consultation_fee: 0,
  appointment_fee: 0,
  bio: "",
  license_number: ""
})

const reviews = ref([])
function generateSlots() {
  const slots = []
  const now = new Date()
  for (let d = 1; d <= 3; d++) {
    const date = new Date(now)
    date.setDate(date.getDate() + d)
    const dateStr = date.toISOString().split('T')[0]
    for (let h = 9; h <= 17; h++) {
      slots.push(`${dateStr} ${h.toString().padStart(2, '0')}:00`)
    }
  }
  return slots
}
const availableSlots = generateSlots()

function selectTime(slot) {
  selectedTime.value = slot
}

async function fetchLawyerDetail() {
  loading.value = true
  try {
    const res = await request.get(`/lawyers/${lawyerId}`)
    Object.assign(lawyer, res || {})
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function fetchReviews() {
  try {
    const res = await request.get(`/lawyers/${lawyerId}/reviews`)
    reviews.value = res || []
  } catch (e) {
    console.error(e)
  }
}

async function handleAppointment() {
  if (!selectedTime.value) return
  submitting.value = true
  try {
    const typeMap = { text: "online", voice: "phone", video: "online" }
    await request.post("/appointments", {
      lawyer_id: parseInt(lawyerId),
      appointment_type: typeMap[consultType.value] || "online",
      appointment_time: selectedTime.value
    })
    ElMessage.success("预约成功，请等待律师确认")
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchLawyerDetail()
  fetchReviews()
})
</script>

<style scoped>
.lawyer-detail-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px 20px;
}
.lawyer-header {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 30px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.lawyer-info {
  flex: 1;
}
.lawyer-name {
  margin: 0 0 15px;
  font-size: 28px;
  color: #333;
}
.lawyer-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 15px;
  color: #666;
  font-size: 14px;
}
.lawyer-price {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  min-width: 150px;
}
.price {
  font-size: 28px;
  font-weight: bold;
  color: #f56c6c;
  margin-bottom: 5px;
}
.price span {
  font-size: 14px;
  font-weight: normal;
  color: #999;
}
.price-label {
  color: #999;
  font-size: 14px;
}
.appointment-section {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.appointment-section h2 {
  margin: 0 0 20px;
  font-size: 20px;
  color: #333;
}
.consult-types {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}
.consult-type {
  flex: 1;
  text-align: center;
  padding: 20px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}
.consult-type:hover {
  border-color: #409eff;
}
.consult-type.active {
  border-color: #409eff;
  background: #ecf5ff;
}
.type-icon {
  font-size: 36px;
  margin-bottom: 10px;
}
.consult-type h3 {
  margin: 0 0 5px;
  font-size: 16px;
  color: #333;
}
.consult-type p {
  margin: 0 0 10px;
  color: #999;
  font-size: 13px;
}
.type-price {
  color: #f56c6c;
  font-weight: bold;
}
.time-slots h3 {
  margin: 0 0 15px;
  font-size: 16px;
  color: #333;
}
.slot-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.time-slot {
  padding: 10px 20px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}
.time-slot:hover {
  border-color: #409eff;
  color: #409eff;
}
.time-slot.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
.appointment-actions {
  text-align: center;
}
.detail-tabs {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.profile-content h3 {
  margin: 20px 0 10px;
  font-size: 16px;
  color: #333;
}
.profile-content p {
  color: #666;
  line-height: 1.8;
}
.info-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.info-list li {
  padding: 8px 0;
  color: #666;
}
.info-list span {
  color: #999;
}
.review-item {
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
}
.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.review-info {
  flex: 1;
}
.user-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}
.review-date {
  color: #999;
  font-size: 13px;
}
.review-content {
  color: #666;
  line-height: 1.6;
}
.empty-reviews {
  padding: 40px 0;
}
</style>
