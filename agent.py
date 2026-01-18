# agent.py
import os
import random
import requests
from bs4 import BeautifulSoup
from prompts import ENGLISH_TECH_PROMPT

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")

# === 非技术主题库（文学/思维/写作/科普）===
NON_TECH_TOPICS = [
    # 文学与思想
    "How Shakespeare’s Language Shapes Modern English",
    "What '1984' Teaches Us About Digital Privacy",
    "Why Metaphors in Poetry Help Us Understand Technology",
    "The Power of Storytelling in Technical Documentation",
    "How Jane Austen’s Dialogue Reveals Human Nature",
    
    # 写作与沟通
    "Why Clear Writing Is a Sign of Clear Thinking",
    "The Art of the One-Sentence Summary",
    "How to Explain Complex Ideas Simply",
    
    # 思维与学习
    "Why Curiosity Beats Memorization in Learning",
    "How to Build Mental Models for Problem Solving",
    "The Difference Between Being Smart and Being Wise",
    
    # 语言与文化
    "Why English Has So Many Words for 'Big'",
    "How Idioms Reveal Cultural Values",
    "The Hidden Logic Behind English Phrasal Verbs"
]

def get_github_trending_topics():
    """获取 GitHub 本周热门技术主题"""
    url = "https://github.com/trending?since=weekly"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
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
        print(f"⚠️ GitHub Trending 抓取失败: {e}")
        return []

def call_qwen(prompt: str) -> str:
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": prompt}]},
        "parameters": {"max_tokens": 1200}
    }
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code == 200:
        return resp.json()["output"]["text"]
    else:
        raise Exception(f"Qwen error: {resp.status_code} - {resp.text}")

def send_to_wechat(title: str, content: str):
    if not SERVERCHAN_SENDKEY:
        print("⚠️ WeChat push skipped (no key)")
        return
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    requests.post(url, data={"title": title, "desp": content}, timeout=10)

def main():
    print("🔍 获取技术主题...")
    tech_topics = get_github_trending_topics()
    
    # 如果抓取失败，用备用技术主题
    if not tech_topics:
        tech_topics = [
            "Understanding Modern API Design",
            "Why Observability Matters in Cloud Systems",
            "The Rise of AI-Powered Development Tools"
        ]
    
    # 选 2 个技术主题
    selected_tech = random.sample(tech_topics, min(2, len(tech_topics)))
    
    # 选 1 个非技术主题
    non_tech = [random.choice(NON_TECH_TOPICS)]
    
    all_topics = selected_tech + non_tech
    random.shuffle(all_topics)  # 打乱顺序，避免固定模式

    articles = []
    for i, topic in enumerate(all_topics, 1):
        print(f"📝 生成第 {i} 篇: {topic[:50]}...")
        try:
            prompt = ENGLISH_TECH_PROMPT.format(topic=topic)
            article = call_qwen(prompt)
            articles.append(f"## 📝 {topic}\n\n{article}\n---\n")
        except Exception as e:
            print(f"❌ 失败: {e}")
            continue

    if not articles:
        print("❌ 无文章生成")
        return

    full_content = "\n".join(articles)
    
    # send_to_wechat("📚 Weekly English Digest (Tech + Mind)", full_content)
    # print("✅ 已推送至微信！")

    with open("latest_digest.md", "w") as f:
        f.write(full_content)
    print("✅ 文章已保存为 latest_digest.md")

    # with open("latest_digest.md", "w") as f:
        # f.write(full_content)

if __name__ == "__main__":
    main()
