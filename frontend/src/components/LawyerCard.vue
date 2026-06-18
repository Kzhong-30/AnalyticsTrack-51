<template>
  <el-card class="lawyer-card" shadow="hover" @click="goDetail">
    <div class="card-top">
      <el-avatar :size="72" :src="lawyer.avatar">
        {{ lawyer.full_name?.charAt(0) || '律' }}
      </el-avatar>
      <div class="top-info">
        <div class="name-row">
          <span class="name">{{ lawyer.full_name }}</span>
          <el-tag v-if="lawyer.status === 'approved'" type="success" size="small" effect="light">
            <el-icon><CircleCheck /></el-icon>
            已认证
          </el-tag>
        </div>
        <div class="firm">{{ lawyer.firm_name || '暂无律所信息' }}</div>
        <div class="stats-row">
          <span class="rating">
            <el-rate v-model="ratingValue" disabled :size="14" />
            <span class="rating-num">{{ lawyer.rating || 0 }}</span>
          </span>
          <span class="divider">|</span>
          <span class="review-count">{{ lawyer.review_count || 0 }}条评价</span>
        </div>
      </div>
    </div>
    <div class="card-middle">
      <div class="info-item">
        <el-icon color="#409eff"><Briefcase /></el-icon>
        <span>执业 {{ lawyer.years_of_experience || 0 }} 年</span>
      </div>
      <div class="info-item">
        <el-icon color="#409eff"><Collection /></el-icon>
        <span class="specialties-text">{{ lawyer.specialties || '暂无专长' }}</span>
      </div>
    </div>
    <div class="card-bottom">
      <div class="fee">
        <span class="fee-label">咨询费</span>
        <span class="fee-amount">¥{{ lawyer.consultation_fee || 0 }}</span>
        <span class="fee-unit">/次</span>
      </div>
      <el-button type="primary" size="small" @click.stop="goDetail">
        立即咨询
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  lawyer: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const ratingValue = computed(() => Number(props.lawyer.rating) || 0)

function goDetail() {
  router.push('/lawyer/' + props.lawyer.id)
}
</script>

<style scoped>
.lawyer-card {
  cursor: pointer;
  transition: transform 0.25s, box-shadow 0.25s;
  border-radius: 8px;
}
.lawyer-card:hover {
  transform: translateY(-4px);
}
.card-top {
  display: flex;
  gap: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}
.top-info {
  flex: 1;
  min-width: 0;
}
.name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}
.name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}
.firm {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}
.stats-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}
.rating {
  display: flex;
  align-items: center;
  gap: 4px;
}
.rating-num {
  color: #f56c6c;
  font-weight: 600;
}
.divider {
  color: #dcdfe6;
}
.review-count {
  color: #909399;
}
.card-middle {
  padding: 16px 0;
  min-height: 80px;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #606266;
}
.info-item:last-child {
  margin-bottom: 0;
}
.specialties-text {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}
.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}
.fee {
  display: flex;
  align-items: baseline;
  gap: 2px;
}
.fee-label {
  font-size: 12px;
  color: #909399;
}
.fee-amount {
  font-size: 20px;
  font-weight: 700;
  color: #f56c6c;
}
.fee-unit {
  font-size: 12px;
  color: #909399;
}
</style>
