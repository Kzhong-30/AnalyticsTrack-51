<template>
  <div class="knowledge-page">
    <el-card shadow="never" class="search-card">
      <el-row :gutter="20" align="middle">
        <el-col :span="12">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索法规、案例、模板..."
            size="large"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon :size="20"><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-select
            v-model="selectedCategory"
            placeholder="选择分类"
            size="large"
            style="width: 100%"
            clearable
            @change="handleCategoryChange"
          >
            <el-option
              v-for="cat in categories"
              :key="cat.value"
              :label="cat.label"
              :value="cat.value"
            />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" size="large" @click="handleSearch" style="width: 100%">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card shadow="never" class="content-card">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="法律法规" name="laws">
          <div class="knowledge-list">
            <div
              v-for="item in filteredList"
              :key="item.id"
              class="knowledge-item"
              @click="viewDetail(item)"
            >
              <div class="item-header">
                <el-icon class="item-icon" :size="24" color="#409EFF">
                  <Reading />
                </el-icon>
                <div class="item-info">
                  <h4 class="item-title">{{ item.title }}</h4>
                  <div class="item-meta">
                    <el-tag size="small" :type="getCategoryType(item.category)">
                      {{ getCategoryLabel(item.category) }}
                    </el-tag>
                    <span class="item-views">
                      <el-icon><View /></el-icon>
                      {{ item.view_count }} 次浏览
                    </span>
                    <span class="item-date">{{ formatDate(item.created_at) }}</span>
                  </div>
                </div>
              </div>
              <p class="item-summary">{{ item.summary || item.content?.substring(0, 100) + '...' }}</p>
            </div>
            <el-empty v-if="filteredList.length === 0" description="暂无数据" />
          </div>
        </el-tab-pane>

        <el-tab-pane label="经典案例" name="cases">
          <div class="knowledge-list">
            <div
              v-for="item in filteredList"
              :key="item.id"
              class="knowledge-item"
              @click="viewDetail(item)"
            >
              <div class="item-header">
                <el-icon class="item-icon" :size="24" color="#67c23a">
                  <Document />
                </el-icon>
                <div class="item-info">
                  <h4 class="item-title">{{ item.title }}</h4>
                  <div class="item-meta">
                    <el-tag size="small" :type="getCategoryType(item.category)">
                      {{ getCategoryLabel(item.category) }}
                    </el-tag>
                    <el-tag size="small" type="info">
                      {{ item.court || '某法院' }}
                    </el-tag>
                    <span class="item-views">
                      <el-icon><View /></el-icon>
                      {{ item.view_count }} 次浏览
                    </span>
                  </div>
                </div>
              </div>
              <p class="item-summary">{{ item.summary || '点击查看完整案例详情...' }}</p>
            </div>
            <el-empty v-if="filteredList.length === 0" description="暂无数据" />
          </div>
        </el-tab-pane>

        <el-tab-pane label="文书模板" name="templates">
          <div class="template-grid">
            <el-card
              v-for="item in filteredList"
              :key="item.id"
              class="template-card"
              shadow="hover"
              @click="viewDetail(item)"
            >
              <div class="template-icon">
                <el-icon :size="40" color="#409EFF"><Files /></el-icon>
              </div>
              <h4 class="template-name">{{ item.title || item.name }}</h4>
              <div class="template-meta">
                <el-tag size="small" :type="getCategoryType(item.category)">
                  {{ getCategoryLabel(item.category) }}
                </el-tag>
                <span class="template-count">
                  <el-icon><View /></el-icon>
                  {{ item.use_count || item.view_count || 0 }}
                </span>
              </div>
              <p class="template-desc">{{ item.description || '点击查看模板详情' }}</p>
            </el-card>
            <el-empty v-if="filteredList.length === 0" description="暂无数据" />
          </div>
        </el-tab-pane>
      </el-tabs>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
        @size-change="handlePageChange"
        @current-change="handlePageChange"
      />
    </el-card>

    <el-dialog
      v-model="detailVisible"
      title="详情"
      width="800px"
      class="detail-dialog"
    >
      <div v-if="currentItem" class="knowledge-detail">
        <div class="detail-header">
          <h2>{{ currentItem.title || currentItem.name }}</h2>
          <div class="detail-meta">
            <el-tag :type="getCategoryType(currentItem.category)">
              {{ getCategoryLabel(currentItem.category) }}
            </el-tag>
            <span class="meta-item">
              <el-icon><View /></el-icon>
              {{ currentItem.view_count || currentItem.use_count || 0 }} 次浏览
            </span>
            <span class="meta-item">
              <el-icon><Clock /></el-icon>
              {{ formatDate(currentItem.created_at) }}
            </span>
          </div>
        </div>
        <el-divider />
        <div class="detail-content" v-html="currentItem.content || currentItem.description">
        </div>
      </div>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button v-if="activeTab === 'templates'" type="primary" @click="useTemplate">
          使用模板
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const router = useRouter()

const searchKeyword = ref('')
const activeTab = ref('laws')
const selectedCategory = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const knowledgeList = ref([])
const loading = ref(false)

const detailVisible = ref(false)
const currentItem = ref(null)

const categories = [
  { value: 'civil', label: '民事' },
  { value: 'criminal', label: '刑事' },
  { value: 'commercial', label: '商事' },
  { value: 'labor', label: '劳动' },
  { value: 'family', label: '婚姻家庭' },
  { value: 'real_estate', label: '房产' },
  { value: 'intellectual_property', label: '知识产权' },
  { value: 'administrative', label: '行政' },
  { value: 'other', label: '其他' },
]

const mockData = {
  laws: [
    {
      id: 101,
      title: '中华人民共和国民法典',
      category: 'civil',
      content: '<p>《中华人民共和国民法典》被称为"社会生活的百科全书"，是新中国第一部以法典命名的法律...</p><p>第一编 总则</p><p>第一章 基本规定</p><p>第一条 为了保护民事主体的合法权益，调整民事关系，维护社会和经济秩序，适应中国特色社会主义发展要求，弘扬社会主义核心价值观，根据宪法，制定本法。</p>',
      view_count: 15234,
      created_at: '2023-01-01T00:00:00',
      summary: '新中国第一部以法典命名的法律，共7编、1260条。',
    },
    {
      id: 102,
      title: '中华人民共和国劳动合同法',
      category: 'labor',
      content: '<p>第一章 总则</p><p>第一条 为了完善劳动合同制度，明确劳动合同双方当事人的权利和义务，保护劳动者的合法权益，构建和发展和谐稳定的劳动关系，制定本法。</p>',
      view_count: 8956,
      created_at: '2023-02-15T00:00:00',
      summary: '规范劳动合同的订立、履行、变更、解除和终止等行为。',
    },
    {
      id: 103,
      title: '中华人民共和国刑法',
      category: 'criminal',
      content: '<p>第一编 总则</p><p>第一章 刑法的任务、基本原则和适用范围</p><p>第一条 为了惩罚犯罪，保护人民，根据宪法，结合我国同犯罪作斗争的具体经验及实际情况，制定本法。</p>',
      view_count: 12456,
      created_at: '2023-03-01T00:00:00',
      summary: '规定犯罪和刑罚的法律，是国家的基本法律之一。',
    },
    {
      id: 104,
      title: '中华人民共和国公司法',
      category: 'commercial',
      content: '<p>第一章 总则</p><p>第一条 为了规范公司的组织和行为，保护公司、股东和债权人的合法权益，维护社会经济秩序，促进社会主义市场经济的发展，制定本法。</p>',
      view_count: 6789,
      created_at: '2023-04-10T00:00:00',
      summary: '规范公司的设立、组织、运营、变更、解散等行为。',
    },
  ],
  cases: [
    {
      id: 201,
      title: '张某诉李某民间借贷纠纷案',
      category: 'civil',
      court: '北京市朝阳区人民法院',
      content: '<h3>案情简介</h3><p>原告张某与被告李某系朋友关系。2022年3月，被告因资金周转向原告借款10万元，约定月利率2%，借期6个月。借款到期后，被告仅偿还了2万元本金，剩余款项一直未还。</p><h3>法院判决</h3><p>法院认为，原被告之间的借贷关系合法有效，被告应当按照约定偿还借款本息。判决被告偿还原告借款本金8万元及相应利息。</p>',
      view_count: 3456,
      created_at: '2024-01-10T00:00:00',
      summary: '典型的民间借贷纠纷案例，涉及利息计算和举证责任。',
    },
    {
      id: 202,
      title: '王某劳动争议案',
      category: 'labor',
      court: '上海市浦东新区人民法院',
      content: '<h3>案情简介</h3><p>原告王某于2020年入职某科技公司，月薪15000元。2023年公司以业务调整为由解除劳动合同，仅支付了1个月工资的经济补偿金。王某认为公司违法解除劳动合同，要求支付赔偿金。</p><h3>法院判决</h3><p>法院认为，公司未能举证证明解除劳动合同的合法性，属于违法解除。判决公司支付王某违法解除劳动合同赔偿金。</p>',
      view_count: 5678,
      created_at: '2024-01-12T00:00:00',
      summary: '违法解除劳动合同的认定及赔偿金计算标准。',
    },
    {
      id: 203,
      title: '某科技公司著作权侵权案',
      category: 'intellectual_property',
      court: '深圳市南山区人民法院',
      content: '<h3>案情简介</h3><p>原告某科技公司开发了一款办公软件，被告某公司未经许可在其网站上提供该软件的破解版下载。原告起诉要求被告停止侵权并赔偿损失。</p><h3>法院判决</h3><p>法院认为，被告的行为构成著作权侵权，判决被告停止侵权并赔偿原告经济损失50万元。</p>',
      view_count: 4321,
      created_at: '2024-01-15T00:00:00',
      summary: '软件著作权保护及侵权损害赔偿计算。',
    },
  ],
  templates: [
    {
      id: 301,
      name: '民事起诉状模板',
      title: '民事起诉状模板',
      category: 'civil',
      description: '适用于一般民事纠纷的起诉状模板，包含原被告信息、诉讼请求、事实与理由等内容。',
      use_count: 2345,
      view_count: 8765,
      created_at: '2023-05-20T00:00:00',
    },
    {
      id: 302,
      name: '劳动合同模板',
      title: '劳动合同模板',
      category: 'labor',
      description: '标准劳动合同模板，包含工作内容、劳动报酬、工作时间、社会保险等条款。',
      use_count: 5678,
      view_count: 12345,
      created_at: '2023-06-10T00:00:00',
    },
    {
      id: 303,
      name: '律师函模板',
      title: '律师函模板',
      category: 'commercial',
      description: '正式律师函模板，可用于催收欠款、告知侵权、催告履约等场景。',
      use_count: 1234,
      view_count: 6543,
      created_at: '2023-07-15T00:00:00',
    },
    {
      id: 304,
      name: '离婚协议书模板',
      title: '离婚协议书模板',
      category: 'family',
      description: '自愿离婚协议书模板，包含子女抚养、财产分割、债务承担等内容。',
      use_count: 3456,
      view_count: 9876,
      created_at: '2023-08-01T00:00:00',
    },
    {
      id: 305,
      name: '房屋买卖合同模板',
      title: '房屋买卖合同模板',
      category: 'real_estate',
      description: '商品房买卖合同模板，包含房屋基本信息、价格、付款方式、交付时间等条款。',
      use_count: 2100,
      view_count: 7890,
      created_at: '2023-09-10T00:00:00',
    },
    {
      id: 306,
      name: '授权委托书模板',
      title: '授权委托书模板',
      category: 'civil',
      description: '通用授权委托书模板，可用于诉讼代理、事务委托等场景。',
      use_count: 1800,
      view_count: 5678,
      created_at: '2023-10-01T00:00:00',
    },
  ],
}

const filteredList = computed(() => {
  let list = knowledgeList.value
  if (selectedCategory.value) {
    list = list.filter(item => item.category === selectedCategory.value)
  }
  if (searchKeyword.value) {
    list = list.filter(item => 
      item.title?.includes(searchKeyword.value) ||
      item.name?.includes(searchKeyword.value) ||
      item.content?.includes(searchKeyword.value) ||
      item.summary?.includes(searchKeyword.value)
    )
  }
  return list
})

function getCategoryLabel(category) {
  const cat = categories.find(c => c.value === category)
  return cat?.label || category
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

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}

function handleTabChange(tab) {
  currentPage.value = 1
  selectedCategory.value = ''
  fetchKnowledgeList()
}

function handleCategoryChange() {
  currentPage.value = 1
}

function handleSearch() {
  currentPage.value = 1
  fetchKnowledgeList()
}

function handlePageChange() {
  fetchKnowledgeList()
}

async function fetchKnowledgeList() {
  loading.value = true
  try {
    const data = await request.get('/knowledge', {
      params: {
        category: selectedCategory.value || undefined,
        search: searchKeyword.value || undefined,
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
      },
    })
    knowledgeList.value = data || mockData[activeTab.value] || []
    total.value = knowledgeList.value.length
  } catch (error) {
    console.error('获取知识列表失败', error)
    knowledgeList.value = mockData[activeTab.value] || []
    total.value = knowledgeList.value.length
  } finally {
    loading.value = false
  }
}

function viewDetail(item) {
  currentItem.value = item
  detailVisible.value = true
}

function useTemplate() {
  ElMessage.success('正在跳转到文书生成页面...')
  router.push('/lawyer/documents')
}

onMounted(() => {
  fetchKnowledgeList()
})
</script>

<style scoped>
.knowledge-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.search-card {
  margin-bottom: 0;
}

.content-card {
  flex: 1;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.knowledge-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.knowledge-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.item-icon {
  flex-shrink: 0;
}

.item-info {
  flex: 1;
}

.item-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 8px;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.item-views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.item-date {
  margin-left: auto;
}

.item-summary {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.template-card {
  cursor: pointer;
  transition: all 0.3s;
}

.template-card:hover {
  transform: translateY(-4px);
}

.template-icon {
  text-align: center;
  margin-bottom: 12px;
}

.template-name {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
  text-align: center;
  margin-bottom: 8px;
}

.template-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.template-count {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.template-desc {
  font-size: 13px;
  color: #909399;
  text-align: center;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.detail-dialog .knowledge-detail {
  padding: 10px 0;
}

.detail-header h2 {
  font-size: 20px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 12px;
}

.detail-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #909399;
}

.detail-content {
  line-height: 1.8;
  color: #303133;
  font-size: 14px;
}

.detail-content :deep(h3) {
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 16px;
}

.detail-content :deep(p) {
  margin-bottom: 10px;
  text-indent: 2em;
}
</style>
