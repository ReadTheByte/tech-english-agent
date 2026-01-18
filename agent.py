import os
import requests

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
SERVERCHAN_SENDKEY = os.getenv("SERVERCHAN_SENDKEY")

TOPICS = [
    "How Spring Boot Auto-Configuration Works",
    "Understanding Java Virtual Machine (JVM) Memory Model",
    "Building a Simple RAG Application with LangChain",
    "Kubernetes Pods vs Deployments: What's the Difference?",
    "Why Vector Databases Matter for AI Applications",
    "Best Practices for RESTful API Design in 2026",
    "Introduction to Observability: Logs, Metrics, and Traces"
]

def call_qwen(prompt: str) -> str:
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
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 200:
        return resp.json()["output"]["text"]
    else:
        raise Exception(f"Qwen API error: {resp.status_code} - {resp.text}")

def send_to_wechat(title: str, content: str):
    if not SERVERCHAN_SENDKEY:
        print("⚠️ SERVERCHAN_SENDKEY not set. Skipping WeChat push.")
        return
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {"title": title, "desp": content}
    requests.post(url, data=data)

def main():
    articles = []
    selected_topics = TOPICS[:3]  # Generate 3 articles per run
    
    for topic in selected_topics:
        print(f"📝 Generating: {topic}")
        prompt = ENGLISH_TECH_PROMPT.format(topic=topic)
        try:
            article = call_qwen(prompt)
            articles.append(f"## 📝 {topic}\n\n{article}\n---\n")
        except Exception as e:
            print(f"❌ Failed to generate {topic}: {e}")
            continue

    if not articles:
        print("❌ No articles generated.")
        return

    full_content = "\n".join(articles)
    send_to_wechat("📚 Weekly Tech English Digest (with Vocabulary)", full_content)
    print("✅ Sent to WeChat!")

    # Also save locally for review
    with open("latest_digest.md", "w") as f:
        f.write(full_content)

if __name__ == "__main__":
    main()
