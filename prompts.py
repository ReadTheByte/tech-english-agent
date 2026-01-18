ENGLISH_TECH_PROMPT = """
You are a senior tech editor. Write a short technical article (400-600 words) in English for intermediate Chinese developers.

Topic: {topic}

Requirements:
1. Use clear, simple English (avoid complex jargon unless necessary).
2. Include 5–8 key technical terms that might be unfamiliar to Chinese developers.
3. After the article, add a section titled "## 🔑 Key Vocabulary" with format:
   - **term**: Chinese meaning (brief explanation in tech context)
4. Output ONLY valid Markdown. No greetings or extra text.
5. Focus on practical, actionable knowledge.

Example topics: JVM internals, Spring Boot features, AI engineering, system design.
"""
