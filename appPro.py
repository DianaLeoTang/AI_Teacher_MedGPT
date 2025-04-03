import os
import json
import faiss
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv

# =====================
# 🔐 API Key 设置
# =====================
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 或直接填写 key

# =====================
# 📦 加载向量索引和元数据
# =====================
data_dir = os.path.dirname(__file__)
index = faiss.read_index(os.path.join(data_dir, "faiss_index.index"))

with open(os.path.join(data_dir, "faiss_metadata.json"), "r", encoding="utf-8") as f:
    metadata = json.load(f)

# =====================
# 🔍 嵌入模型
# =====================
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# =====================
# 🌐 页面界面
# =====================
st.set_page_config(page_title="药学AI课堂｜智能问答实验室", layout="wide")
st.title("💊 药学AI课堂｜智能问答实验室")
st.markdown("请在下方输入你的问题，系统将从药品文献中提取答案并引用出处。")

query = st.text_input("请输入你的问题：", "阿司匹林和布洛芬哪个对胃刺激更小？")
submit = st.button("提交问题")

# =====================
# 🔄 检索 + 生成函数
# =====================
def search_faiss(question, top_k=5):
    vec = embedder.encode([question], convert_to_numpy=True).astype("float32")
    D, I = index.search(vec, top_k)
    return [metadata[i] for i in I[0]]

def generate_answer(question, contexts):
    context_text = "\n\n".join(
        [f"[文献{idx+1} 来自《{c['meta']['book']}》 第{c['meta']['page']}页]\n{c['text']}"
         for idx, c in enumerate(contexts)]
    )

    prompt = f"""
你是一位专业的药学知识助手，请根据下列资料回答用户的问题。

{context_text}

问题：{question}
请基于上述资料简洁回答问题，并列出参考出处（书名+页码）。如资料不足，请明确说明。
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# =====================
# 🚀 执行问答
# =====================
if submit:
    with st.spinner("正在检索并生成答案..."):
        top_contexts = search_faiss(query)
        answer = generate_answer(query, top_contexts)

        st.success("✅ 回答完成：")
        st.markdown(answer)

        with st.expander("📚 查看引用段落"):
            for i, item in enumerate(top_contexts):
                st.markdown(f"**文献{i+1} - 第{item['meta']['page']}页 - {item['meta']['book']}**")
                st.markdown(f"> {item['text']}")
