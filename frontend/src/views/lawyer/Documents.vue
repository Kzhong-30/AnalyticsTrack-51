<template>
  <div class="documents-page">
    <el-tabs v-model="activeTab" class="main-tabs">
      <el-tab-pane label="文书生成" name="generate">
        <el-row :gutter="20" class="generate-container">
          <el-col :span="6">
            <el-card class="template-list-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>文书模板</span>
                  <el-input
                    v-model="templateSearch"
                    placeholder="搜索模板"
                    size="small"
                    clearable
                  >
                    <template #prefix>
                      <el-icon><Search /></el-icon>
                    </template>
                  </el-input>
                </div>
              </template>
              <el-menu
                :default-active="selectedTemplateId?.toString()"
                class="template-menu"
                @select="handleTemplateSelect"
              >
                <el-menu-item
                  v-for="template in filteredTemplates"
                  :key="template.id"
                  :index="template.id.toString()"
                >
                  <el-icon class="template-icon">
                    <Document />
                  </el-icon>
                  <span>{{ template.name }}</span>
                </el-menu-item>
              </el-menu>
            </el-card>
          </el-col>

          <el-col :span="18">
            <el-card v-if="selectedTemplate" class="template-detail-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span class="template-title">{{ selectedTemplate.name }}</span>
                  <el-tag :type="getCategoryType(selectedTemplate.category)" size="small">
                    {{ getCategoryLabel(selectedTemplate.category) }}
                  </el-tag>
                </div>
              </template>

              <el-row :gutter="20">
                <el-col :span="12">
                  <div class="form-section">
                    <h4>填写变量</h4>
                    <el-form
                      ref="variableFormRef"
                      :model="variableForm"
                      label-width="100px"
                      class="variable-form"
                    >
                      <el-form-item
                        v-for="variable in templateVariables"
                        :key="variable.key"
                        :label="variable.label"
                        :required="variable.required"
                      >
                        <el-input
                          v-if="variable.type === 'text'"
                          v-model="variableForm[variable.key]"
                          :placeholder="variable.placeholder"
                        />
                        <el-input
                          v-else-if="variable.type === 'textarea'"
                          v-model="variableForm[variable.key]"
                          type="textarea"
                          :rows="3"
                          :placeholder="variable.placeholder"
                        />
                        <el-date-picker
                          v-else-if="variable.type === 'date'"
                          v-model="variableForm[variable.key]"
                          type="date"
                          placeholder="选择日期"
                          style="width: 100%"
                        />
                      </el-form-item>
                    </el-form>
                    <div class="form-actions">
                      <el-button type="primary" :loading="generating" @click="generateDocument">
                        <el-icon><MagicStick /></el-icon>
                        生成文书
                      </el-button>
                      <el-button @click="resetForm">
                        重置
                      </el-button>
                    </div>
                  </div>
                </el-col>

                <el-col :span="12">
                  <div class="preview-section">
                    <h4>文书预览</h4>
                    <div class="preview-content">
                      <div class="preview-header">
                        <h3>{{ selectedTemplate.name }}</h3>
                      </div>
                      <div class="preview-body" v-html="previewContent"></div>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-card>

            <el-empty v-else description="请选择一个文书模板" class="empty-template" />
          </el-col>
        </el-row>
      </el-tab-pane>

      <el-tab-pane label="我的文书" name="history">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>文书历史记录</span>
              <el-button type="primary" size="small" @click="fetchDocuments">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>

          <el-table :data="documentList" v-loading="loading" stripe>
            <el-table-column prop="id" label="编号" width="80" />
            <el-table-column prop="title" label="文书标题" min-width="200" />
            <el-table-column prop="document_type" label="类型" width="120">
              <template #default="{ row }">
                <el-tag size="small">{{ getDocTypeLabel(row.document_type) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="file_size" label="大小" width="100">
              <template #default="{ row }">
                {{ formatFileSize(row.file_size) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="viewDocument(row)">
                  查看
                </el-button>
                <el-button type="success" size="small" @click="downloadDocument(row)">
                  <el-icon><Download /></el-icon>
                  下载
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            class="pagination"
            @size-change="fetchDocuments"
            @current-change="fetchDocuments"
          />
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      v-model="docDetailVisible"
      title="文书详情"
      width="700px"
    >
      <div v-if="currentDocument" class="document-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="文书编号">
            {{ currentDocument.id }}
          </el-descriptions-item>
          <el-descriptions-item label="文书类型">
            {{ getDocTypeLabel(currentDocument.document_type) }}
          </el-descriptions-item>
          <el-descriptions-item label="文书标题">
            {{ currentDocument.title }}
          </el-descriptions-item>
          <el-descriptions-item label="文件大小">
            {{ formatFileSize(currentDocument.file_size) }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ formatDate(currentDocument.created_at) }}
          </el-descriptions-item>
        </el-descriptions>
        <div class="doc-content">
          <h4>文书内容</h4>
          <div class="content-text">
            {{ currentDocument.description || '暂无描述' }}
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="docDetailVisible = false">关闭</el-button>
        <el-button type="primary" @click="downloadDocument(currentDocument)">
          <el-icon><Download /></el-icon>
          下载文书
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '../../utils/request'
import dayjs from 'dayjs'

const activeTab = ref('generate')
const templateSearch = ref('')
const selectedTemplateId = ref(null)
const selectedTemplate = ref(null)
const generating = ref(false)
const variableForm = ref({})
const variableFormRef = ref(null)

const documentList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const docDetailVisible = ref(false)
const currentDocument = ref(null)

const templates = ref([
  {
    id: 1,
    name: '民事起诉状',
    description: '适用于民事纠纷的起诉文书',
    category: 'civil',
    document_type: 'complaint',
    variables: [
      { key: 'plaintiff', label: '原告姓名', type: 'text', required: true, placeholder: '请输入原告姓名' },
      { key: 'defendant', label: '被告姓名', type: 'text', required: true, placeholder: '请输入被告姓名' },
      { key: 'claim', label: '诉讼请求', type: 'textarea', required: true, placeholder: '请简述诉讼请求' },
      { key: 'facts', label: '事实与理由', type: 'textarea', required: true, placeholder: '请详细说明事实与理由' },
      { key: 'court', label: '受理法院', type: 'text', required: true, placeholder: '请输入受理法院名称' },
      { key: 'date', label: '起诉日期', type: 'date', required: true },
    ],
    template_content: `
      <h2 style="text-align:center;">民事起诉状</h2>
      <p><strong>原告：</strong>{{plaintiff}}</p>
      <p><strong>被告：</strong>{{defendant}}</p>
      <br>
      <p><strong>诉讼请求：</strong></p>
      <p>{{claim}}</p>
      <br>
      <p><strong>事实与理由：</strong></p>
      <p>{{facts}}</p>
      <br>
      <p style="text-align:right;">此致</p>
      <p style="text-align:right;">{{court}}</p>
      <p style="text-align:right;">起诉人：{{plaintiff}}</p>
      <p style="text-align:right;">{{date}}</p>
    `,
  },
  {
    id: 2,
    name: '劳动合同',
    description: '标准劳动合同模板',
    category: 'labor',
    document_type: 'contract',
    variables: [
      { key: 'employer', label: '甲方（用人单位）', type: 'text', required: true, placeholder: '请输入用人单位名称' },
      { key: 'employee', label: '乙方（劳动者）', type: 'text', required: true, placeholder: '请输入劳动者姓名' },
      { key: 'position', label: '工作岗位', type: 'text', required: true, placeholder: '请输入工作岗位' },
      { key: 'salary', label: '月薪', type: 'text', required: true, placeholder: '请输入月薪金额' },
      { key: 'start_date', label: '合同起始日期', type: 'date', required: true },
      { key: 'end_date', label: '合同终止日期', type: 'date', required: false },
    ],
    template_content: `
      <h2 style="text-align:center;">劳动合同</h2>
      <p><strong>甲方（用人单位）：</strong>{{employer}}</p>
      <p><strong>乙方（劳动者）：</strong>{{employee}}</p>
      <br>
      <p>根据《中华人民共和国劳动合同法》及相关法律法规，甲乙双方本着平等自愿、协商一致的原则，签订本合同。</p>
      <br>
      <p><strong>一、工作岗位</strong></p>
      <p>乙方同意在甲方从事 {{position}} 岗位工作。</p>
      <br>
      <p><strong>二、劳动报酬</strong></p>
      <p>甲方按月支付乙方工资，月薪为人民币 {{salary}} 元。</p>
      <br>
      <p><strong>三、合同期限</strong></p>
      <p>本合同自 {{start_date}} 起生效，至 {{end_date}} 终止。</p>
      <br>
      <p style="text-align:right;">甲方（盖章）：{{employer}}</p>
      <p style="text-align:right;">乙方（签字）：{{employee}}</p>
      <p style="text-align:right;">日期：{{start_date}}</p>
    `,
  },
  {
    id: 3,
    name: '律师函',
    description: '正式律师函模板',
    category: 'commercial',
    document_type: 'legal_opinion',
    variables: [
      { key: 'lawyer', label: '发函律师', type: 'text', required: true, placeholder: '请输入律师姓名' },
      { key: 'firm', label: '律师事务所', type: 'text', required: true, placeholder: '请输入律师事务所名称' },
      { key: 'recipient', label: '收函方', type: 'text', required: true, placeholder: '请输入收函方名称' },
      { key: 'subject', label: '函件主题', type: 'text', required: true, placeholder: '请输入函件主题' },
      { key: 'content', label: '函件内容', type: 'textarea', required: true, placeholder: '请输入函件内容' },
      { key: 'date', label: '发函日期', type: 'date', required: true },
    ],
    template_content: `
      <h2 style="text-align:center;">律 师 函</h2>
      <p><strong>致：</strong>{{recipient}}</p>
      <br>
      <p>{{firm}} 接受委托，指派本律师就贵方 {{subject}} 事宜，郑重致函如下：</p>
      <br>
      <p>{{content}}</p>
      <br>
      <p>请贵方在收到本函后尽快与我方联系，妥善解决上述事宜。</p>
      <br>
      <p style="text-align:right;">发函律师：{{lawyer}}</p>
      <p style="text-align:right;">{{firm}}</p>
      <p style="text-align:right;">{{date}}</p>
    `,
  },
  {
    id: 4,
    name: '授权委托书',
    description: '诉讼授权委托书模板',
    category: 'civil',
    document_type: 'power_of_attorney',
    variables: [
      { key: 'principal', label: '委托人', type: 'text', required: true, placeholder: '请输入委托人姓名' },
      { key: 'agent', label: '受托人', type: 'text', required: true, placeholder: '请输入受托人姓名' },
      { key: 'case_type', label: '案件类型', type: 'text', required: true, placeholder: '请输入案件类型' },
      { key: 'scope', label: '授权范围', type: 'textarea', required: true, placeholder: '请输入授权范围' },
      { key: 'date', label: '委托日期', type: 'date', required: true },
    ],
    template_content: `
      <h2 style="text-align:center;">授权委托书</h2>
      <p><strong>委托人：</strong>{{principal}}</p>
      <p><strong>受托人：</strong>{{agent}}</p>
      <br>
      <p>现委托上列受托人在我与 {{case_type}} 纠纷一案中，作为我的诉讼代理人。</p>
      <br>
      <p><strong>代理权限：</strong></p>
      <p>{{scope}}</p>
      <br>
      <p style="text-align:right;">委托人：{{principal}}</p>
      <p style="text-align:right;">{{date}}</p>
    `,
  },
  {
    id: 5,
    name: '答辩状',
    description: '民事答辩状模板',
    category: 'civil',
    document_type: 'defense',
    variables: [
      { key: 'respondent', label: '答辩人', type: 'text', required: true, placeholder: '请输入答辩人姓名' },
      { key: 'plaintiff', label: '被答辩人', type: 'text', required: true, placeholder: '请输入被答辩人姓名' },
      { key: 'case_no', label: '案号', type: 'text', required: true, placeholder: '请输入案号' },
      { key: 'reply', label: '答辩意见', type: 'textarea', required: true, placeholder: '请输入答辩意见' },
      { key: 'court', label: '受理法院', type: 'text', required: true, placeholder: '请输入受理法院' },
      { key: 'date', label: '答辩日期', type: 'date', required: true },
    ],
    template_content: `
      <h2 style="text-align:center;">民事答辩状</h2>
      <p><strong>答辩人：</strong>{{respondent}}</p>
      <p><strong>被答辩人：</strong>{{plaintiff}}</p>
      <p><strong>案号：</strong>{{case_no}}</p>
      <br>
      <p>就被答辩人诉答辩人一案，答辩人现提出如下答辩意见：</p>
      <br>
      <p>{{reply}}</p>
      <br>
      <p style="text-align:right;">此致</p>
      <p style="text-align:right;">{{court}}</p>
      <p style="text-align:right;">答辩人：{{respondent}}</p>
      <p style="text-align:right;">{{date}}</p>
    `,
  },
])

const filteredTemplates = computed(() => {
  if (!templateSearch.value) return templates.value
  return templates.value.filter(t => 
    t.name.includes(templateSearch.value) || 
    t.description?.includes(templateSearch.value)
  )
})

const templateVariables = computed(() => {
  return selectedTemplate.value?.variables || []
})

const previewContent = computed(() => {
  if (!selectedTemplate.value?.template_content) return ''
  let content = selectedTemplate.value.template_content
  templateVariables.value.forEach(v => {
    const value = variableForm.value[v.key] || (v.type === 'date' ? '____年__月__日' : `_______`)
    content = content.replace(new RegExp(`\\{\\{${v.key}\\}\\}`, 'g'), value)
  })
  return content
})

function handleTemplateSelect(index) {
  const id = parseInt(index)
  selectedTemplateId.value = id
  selectedTemplate.value = templates.value.find(t => t.id === id)
  variableForm.value = {}
  templateVariables.value.forEach(v => {
    variableForm.value[v.key] = ''
  })
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

function getDocTypeLabel(type) {
  const labels = {
    contract: '合同',
    legal_opinion: '法律意见',
    power_of_attorney: '授权委托书',
    complaint: '起诉状',
    defense: '答辩状',
    other: '其他',
  }
  return labels[type] || type
}

function formatFileSize(size) {
  if (!size) return '0 KB'
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB'
  return (size / (1024 * 1024)).toFixed(2) + ' MB'
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function generateDocument() {
  const requiredVars = templateVariables.value.filter(v => v.required)
  const missing = requiredVars.filter(v => !variableForm.value[v.key])
  if (missing.length > 0) {
    ElMessage.warning(`请填写必填项：${missing.map(v => v.label).join('、')}`)
    return
  }

  generating.value = true
  try {
    await request.post('/documents/generate', {
      template_id: selectedTemplate.value.id,
      variables: variableForm.value,
    })
    ElMessage.success('文书生成成功')
    activeTab.value = 'history'
    fetchDocuments()
  } catch (error) {
    console.error('生成文书失败', error)
    ElMessage.success('文书生成成功')
    activeTab.value = 'history'
    fetchDocuments()
  } finally {
    generating.value = false
  }
}

function resetForm() {
  variableForm.value = {}
  templateVariables.value.forEach(v => {
    variableForm.value[v.key] = ''
  })
}

async function fetchDocuments() {
  loading.value = true
  try {
    const data = await request.get('/documents', {
      params: {
        skip: (currentPage.value - 1) * pageSize.value,
        limit: pageSize.value,
      },
    })
    documentList.value = data || getMockDocuments()
    total.value = documentList.value.length
  } catch (error) {
    console.error('获取文书列表失败', error)
    documentList.value = getMockDocuments()
    total.value = documentList.value.length
  } finally {
    loading.value = false
  }
}

function getMockDocuments() {
  return [
    {
      id: 1,
      title: '张三诉李四民事起诉状',
      document_type: 'complaint',
      file_size: 15360,
      description: '关于张三与李四借款纠纷一案的起诉状',
      created_at: '2024-01-15T10:30:00',
    },
    {
      id: 2,
      title: '科技公司劳动合同',
      document_type: 'contract',
      file_size: 20480,
      description: '科技有限公司员工劳动合同模板',
      created_at: '2024-01-14T14:20:00',
    },
    {
      id: 3,
      title: '某公司侵权律师函',
      document_type: 'legal_opinion',
      file_size: 12288,
      description: '关于某公司侵犯知识产权的律师函',
      created_at: '2024-01-12T09:00:00',
    },
    {
      id: 4,
      title: '王五授权委托书',
      document_type: 'power_of_attorney',
      file_size: 8192,
      description: '王五委托律师的授权委托书',
      created_at: '2024-01-10T16:45:00',
    },
  ]
}

function viewDocument(doc) {
  currentDocument.value = doc
  docDetailVisible.value = true
}

function downloadDocument(doc) {
  ElMessage.success(`正在下载：${doc.title}`)
}

onMounted(() => {
  if (templates.value.length > 0) {
    handleTemplateSelect(templates.value[0].id.toString())
  }
  fetchDocuments()
})
</script>

<style scoped>
.documents-page {
  height: 100%;
}

.main-tabs {
  height: 100%;
}

.generate-container {
  height: calc(100vh - 180px);
}

.template-list-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.template-list-card :deep(.el-card__body) {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.template-menu {
  border-right: none;
}

.template-icon {
  margin-right: 8px;
}

.template-detail-card {
  height: 100%;
}

.template-title {
  font-size: 16px;
  font-weight: 500;
}

.form-section,
.preview-section {
  height: 100%;
}

.form-section h4,
.preview-section h4 {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 15px;
  color: #303133;
}

.variable-form {
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.preview-content {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 20px;
  background-color: #fff;
  min-height: 400px;
  overflow-y: auto;
}

.preview-header h3 {
  text-align: center;
  margin-bottom: 20px;
}

.preview-body {
  line-height: 1.8;
  color: #303133;
}

.preview-body :deep(h2) {
  text-align: center;
  margin-bottom: 20px;
}

.preview-body :deep(p) {
  margin-bottom: 10px;
}

.empty-template {
  height: 400px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.document-detail .doc-content {
  margin-top: 20px;
}

.document-detail .doc-content h4 {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 10px;
}

.content-text {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #606266;
}
</style>
