<template>
  <div class="consultation-wizard">
    <div class="wizard-header">
      <h1>发布法律咨询</h1>
      <el-steps :active="activeStep" finish-status="success" align-center>
        <el-step title="选择领域" />
        <el-step title="描述问题" />
        <el-step title="选择地区" />
      </el-steps>
    </div>

    <div class="wizard-content">
      <div v-show="activeStep === 0" class="step-content">
        <h2>请选择咨询的法律领域</h2>
        <el-row :gutter="20">
          <el-col :span="8" v-for="cat in categories" :key="cat.id">
            <div class="category-card" :class="{ active: form.category === cat.id }" @click="selectCategory(cat.id)">
              <div class="cat-icon">{{ cat.icon }}</div>
              <h3>{{ cat.name }}</h3>
              <p>{{ cat.desc }}</p>
            </div>
          </el-col>
        </el-row>
      </div>
      <div v-show="activeStep === 1" class="step-content">
        <h2>请详细描述您的问题</h2>
        <el-form :model="form" :rules="step2Rules" ref="step2FormRef" label-width="100px">
          <el-form-item label="问题标题" prop="title">
            <el-input v-model="form.title" placeholder="请简要概括您的问题" maxlength="100" show-word-limit />
          </el-form-item>
          <el-form-item label="详细描述" prop="description">
            <el-input v-model="form.description" type="textarea" :rows="6" placeholder="请详细描述您遇到的法律问题..." maxlength="2000" show-word-limit />
          </el-form-item>
          <el-form-item label="上传附件">
            <el-upload v-model:file-list="fileList" action="#" multiple :auto-upload="false">
              <el-button>点击上传</el-button>
              <template #tip>
                <div class="el-upload__tip">支持图片、PDF等格式，单文件不超过10MB</div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </div>
      <div v-show="activeStep === 2" class="step-content">
        <h2>请选择您所在的城市</h2>
        <el-form :model="form" :rules="step3Rules" ref="step3FormRef" label-width="100px">
          <el-form-item label="所在城市" prop="city">
            <el-select v-model="form.city" placeholder="请选择城市" style="width: 100%" size="large">
              <el-option v-for="city in cities" :key="city" :label="city" :value="city" />
            </el-select>
          </el-form-item>
          <el-form-item label="详细说明">
            <p class="summary">我们将根据您选择的领域和城市，为您匹配最合适的律师。</p>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <div class="wizard-footer">
      <el-button v-if="activeStep > 0" @click="prevStep">上一步</el-button>
      <el-button v-if="activeStep < 2" type="primary" @click="nextStep">下一步</el-button>
      <el-button v-if="activeStep === 2" type="primary" :loading="submitting" @click="handleSubmit">提交并匹配律师</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import request from "../utils/request"

const router = useRouter()
const activeStep = ref(0)
const submitting = ref(false)
const fileList = ref([])
const step2FormRef = ref(null)
const step3FormRef = ref(null)

const categories = [
  { id: "marriage", name: "婚姻家庭", icon: "👨‍👩‍👧", desc: "离婚、财产分割、子女抚养" },
  { id: "labor", name: "劳动纠纷", icon: "💼", desc: "劳动合同、工伤赔偿、社保" },
  { id: "contract", name: "合同纠纷", icon: "📝", desc: "合同起草、违约纠纷" },
  { id: "property", name: "房产纠纷", icon: "🏠", desc: "房屋买卖、租赁、物业" },
  { id: "criminal", name: "刑事辩护", icon: "⚖️", desc: "刑事辩护、取保候审" },
  { id: "company", name: "公司法务", icon: "🏢", desc: "公司设立、股权、合规" }
]

const cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉", "西安", "重庆"]

const form = reactive({
  category: "",
  title: "",
  description: "",
  city: ""
})

const step2Rules = {
  title: [{ required: true, message: "请输入问题标题", trigger: "blur" }],
  description: [{ required: true, message: "请输入详细描述", trigger: "blur" }]
}

const step3Rules = {
  city: [{ required: true, message: "请选择城市", trigger: "change" }]
}

function selectCategory(id) {
  form.category = id
}

async function nextStep() {
  if (activeStep.value === 0) {
    if (!form.category) {
      ElMessage.warning("请选择法律领域")
      return
    }
  } else if (activeStep.value === 1) {
    await step2FormRef.value?.validate()
  }
  activeStep.value++
}

function prevStep() {
  activeStep.value--
}

async function handleSubmit() {
  await step3FormRef.value?.validate()
  submitting.value = true
  try {
    await request.post("/consultations", {
      title: form.title,
      description: form.description,
      category: form.category
    })
    ElMessage.success("发布成功，正在为您匹配律师...")
    setTimeout(() => {
      router.push("/lawyers")
    }, 1000)
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.consultation-wizard {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}
.wizard-header h1 {
  text-align: center;
  margin: 0 0 40px;
  color: #333;
}
.wizard-content {
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-height: 400px;
}
.step-content h2 {
  margin: 0 0 30px;
  font-size: 20px;
  color: #333;
}
.category-card {
  text-align: center;
  padding: 30px 20px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s;
}
.category-card:hover {
  border-color: #409eff;
  transform: translateY(-3px);
}
.category-card.active {
  border-color: #409eff;
  background: #ecf5ff;
}
.cat-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.category-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
  color: #333;
}
.category-card p {
  margin: 0;
  color: #999;
  font-size: 14px;
}
.wizard-footer {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}
.summary {
  color: #666;
  font-size: 14px;
  margin: 0;
  line-height: 1.6;
}
</style>
