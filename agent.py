# agent.py
import os
import random
import time
import requests
from bs4 import BeautifulSoup

# === 非技术主题库（文学/思维/写作/科普）===
NON_TECH_TOPICS = [
    "Why Reading Fiction Builds Better Minds",
    "How Shakespeare’s Language Shapes Modern English",
    "What '1984' Teaches Us About Digital Privacy",
    "The Art of Writing Clear Technical Documentation",
    "Why Curiosity Beats Memorization in Learning",
    "How to Explain Complex Ideas Simply",
    "The Power of Analogies in Communication",
    "Why Silence Helps You Think Better",
    "How Metaphors Shape Our Understanding of Technology",
    "The Difference Between Knowledge and Wisdom"
]

def get_github_trending_topics():
    """从 GitHub Trending 获取本周热门技术主题（国内可访问）"""
    url = "https://github.com/trending?since=weekly"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        topics = []
        for repo in soup.select('article')[:8]:
            name_elem = repo.select_one('h2 a')
            if not name_elem:
                continue
            full_name = name_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
            desc_elem = repo.select_one('p')
            desc = desc_elem.get_text(strip=True) if desc_elem else ""
            topic = f"What is {full_name}? {desc}" if desc else f"Introduction to {full_name}"
            topics.append(topic[:90])
        return topics
    except Exception as e:
        print(f"⚠️ 获取 GitHub Trending 失败: {e}")
        return []

def call_qwen(prompt: str, max_retries=3) -> str:
    """调用 Qwen API，带重试和超时处理"""
    DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
    if not DASHSCOPE_API_KEY:
        raise Exception("DASHSCOPE_API_KEY 未设置")

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"max_tokens": 1200}
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=60)
            if resp.status_code == 200:
                result = resp.json()
                if "output" in result and "text" in result["output"]:
                    return result["output"]["text"]
                else:
                    raise Exception(f"Unexpected API response: {result}")
            else:
                error_msg = resp.json().get("message", resp.text)
                print(f"❌ Qwen API 错误 (尝试 {attempt+1}/{max_retries}): {resp.status_code} - {error_msg}")
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络错误 (尝试 {attempt+1}/{max_retries}): {e}")

        if attempt < max_retries - 1:
            time.sleep(5)  # 等待后重试

    raise Exception("Qwen API 调用失败，已重试多次")

def main():
    print("🔍 正在获取 GitHub 本周热门技术主题...")
    tech_topics = get_github_trending_topics()
    
    # 备用技术主题（抓取失败时使用）
    if not tech_topics:
        tech_topics = [
            "Understanding Modern API Design",
            "Why Observability Matters in Cloud Systems",
            "The Rise of AI-Powered Development Tools"
        ]
        print("🔄 使用备用技术主题")
    
    # 选择 2 个技术主题 + 1 个非技术主题
    selected_tech = random.sample(tech_topics, min(2, len(tech_topics)))
    non_tech = [random.choice(NON_TECH_TOPICS)]
    all_topics = selected_tech + non_tech
    random.shuffle(all_topics)  # 打乱顺序

    articles = []
    for i, topic in enumerate(all_topics, 1):
        print(f"📝 正在生成第 {i} 篇: {topic[:50]}...")
        try:
            # 构造提示词（确保与 prompts.py 一致）
            prompt = f"""You are a senior tech writer creating content for Chinese developers who want to improve their English reading skills.

Write a short article (400–600 words) in clear, natural English about the following topic:

Topic: {topic}

Requirements:
1. Use fluent, professional but accessible English — like articles on Medium or official documentation.
2. Focus on explaining concepts, trends, or best practices. DO NOT include code snippets, config files, or architecture diagrams.
3. Use real-world context so readers can guess word meanings from sentences.
4. After the article, add a section titled exactly:
   ## 🔑 Key Vocabulary
   List 5–8 technical terms that might be unfamiliar to intermediate learners, in this format:
   - **term**: Chinese meaning (brief explanation in tech context)
5. Output ONLY valid Markdown. No greetings, no summary, no extra sections.
6. Keep sentences clear and engaging. Avoid overly complex grammar.
"""
            article = call_qwen(prompt)
            articles.append(f"## 📝 {topic}\n\n{article}\n---\n")
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            continue

    if not articles:
        raise Exception("所有文章生成失败，无法继续")

    # ✅ 关键修复：定义 full_content
    full_content = "\n".join(articles)

    # 保存到文件（供后续 deploy 使用）
    with open("latest_digest.md", "w", encoding="utf-8") as f:
        f.write(full_content)

    print("✅ 文章已成功保存为 latest_digest.md")

if __name__ == "__main__":
    main()
