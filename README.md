# AI_Teacher_MedGPT 药学AI课堂｜智能问答实验室

这是一个面向药学教育的智能问答系统，结合药品文献、嵌入模型、向量检索和大语言模型（OpenAI GPT），让学生可以在课堂中通过浏览器提问，系统自动从文献中提取答案并标注出处。

---

## ✅ 项目功能亮点

- 💬 网页问答（基于药学文献）
- 📚 引用文献出处（书名 + 页码）
- 🧠 OpenAI API 生成高质量回答
- 📝 自动记录学生提问日志
- 🌐 内网访问，适用于课堂部署

---

## 📁 项目结构

```
药学AI课堂/
├── app.py                  # 主应用程序（Streamlit）
├── faiss_index.index       # 文献段落向量索引
├── faiss_metadata.json     # 文献原文 + 出处信息
├── requirements.txt        # 项目依赖列表
├── .env                    # OpenAI API Key（需手动添加）
├── log/                    # 自动生成提问日志
└── README.md               # 本说明文档
```

---

## 🛠️ 安装与运行（Mac 环境）

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 添加 `.env` 文件

在项目根目录创建 `.env`，内容如下：

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
```

### 3️⃣ 启动服务（允许局域网访问）

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

---

## 🌍 学生访问方式（局域网）

在老师电脑终端执行：

```bash
ifconfig | grep inet
```

查找局域网地址（如 192.168.x.x）

学生浏览器输入地址：

```
http://192.168.x.x:8501
```

---

## 📋 提问日志记录

每次学生提问，系统会自动记录到：

```
log/questions_log.csv
```

记录格式：

```
时间,问题内容
2025-04-03T14:22:51, 阿司匹林和布洛芬哪个对胃刺激更小？
```

---

## 🧩 知识库更新说明

如需添加新文献：

1. 提取段落 → JSON（含页码、书名）
2. 使用嵌入模型构建向量
3. 更新 `faiss_index.index` 和 `faiss_metadata.json`

---

## 🧠 教学场景建议

- 教学辅助：学生随时提问、即时解答
- 考试复习：文献查阅与回顾
- AI素养教育：展示智能问答原理
