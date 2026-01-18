# 📚 Tech English Agent

每周自动生成 3 篇英文技术短文（含中文词汇注释），推送至微信，助你提升技术英语阅读能力。

## ✨ 功能
- 主题：Java / AI / 架构 / 云原生
- 输出：英文原文 + 重点词中文解释
- 推送：每周日 20:00 自动发到你的微信

## 🔧 部署步骤
1. 注册 [阿里云百炼](https://bailian.console.aliyun.com)，获取 `DASHSCOPE_API_KEY`
2. 注册 [Server 酱](https://sct.ftqq.com)，扫码获取 `SendKey`
3. 在本仓库 Settings → Secrets → Actions 中添加两个 Secret：
   - `DASHSCOPE_API_KEY`
   - `SERVERCHAN_SENDKEY`
4. 手动运行一次 Action 测试

> 💡 免费额度足够使用，无需服务器！
