---
title: Office Sim OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_file: inference.py
pinned: false
---

# OfficeSim Final Boss

Multi-task AI environment for:
- Email triage
- Meeting scheduling
- Document review

## Run locally

export API_BASE_URL=https://api.openai.com/v1  
export OPENAI_API_KEY=your_key  
export MODEL_NAME=gpt-4o-mini  

python inference.py