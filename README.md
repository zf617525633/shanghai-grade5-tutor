# 上海小学五年级知心伴学导师（Shanghai Grade 5 AI Tutor Agent Skill）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Ready-brightgreen.svg)](https://github.com/zf617525633/shanghai-grade5-tutor/blob/main/SKILL.md)
[![Shanghai 5-4 System](https://img.shields.io/badge/Curriculum-Shanghai%20Grade%205-blue.svg)](https://github.com/zf617525633/shanghai-grade5-tutor/blob/main/references/shanghai_curriculum_guide.md)
[![Platform Supported](https://img.shields.io/badge/Platforms-Doubao%20%7C%20WorkBuddy%20%7C%20OpenClaw%20%7C%20Antigravity-orange.svg)](https://github.com/zf617525633/shanghai-grade5-tutor/blob/main/INSTALL_GUIDE.md)

专为**上海小学五年级（五四学制小学毕业班）**学生量身打造的 AI 伴学导师与启发式家教 Agent Skill。严格适配上海本土教材体系（**沪教版数学**、**牛津上海版英语**、**部编版语文**）。

具备**“防抄作业启发教学”、“正题与错题全闭环追踪”、“优势发现”与“薄弱点查漏补缺”**四大核心能力。

---

## 🎯 核心特色与功能

### 1. 🛡️ 防抄作业硬红线（Anti-Cheating）
* 无论孩子以任何借口索要答案（“快告诉我选A还是B”、“我作业来不及了”），**坚决不给现成答案、计算结果或代写作文**。
* 以温柔但坚定的话术接住情绪，通过给出一个微小台阶（Hint 1）引导孩子迈出第一步。

### 2. 🪜 苏格拉底四步阶梯启发法（Socratic Scaffolding）
* **单次单问，小步快跑**：每次回复只抛出 1 个关键问题或 1 个线索，绝不发长篇大论，避免认知超载。
* **阶梯流程**：
  1. **审题提取**：引导孩子找出题目已知什么，最后求什么；
  2. **搭脚手架**：提示数量关系/等量关系或时态线索；
  3. **自主推导**：让孩子自己列出方程/算式并得出结果；
  4. **变式巩固**：一句话提炼方法，出同类型趣味题巩固。

### 3. 📊 正题+错题全追踪，智能学情诊断
* **记录优势档案**：孩子独立做对的题目，自动提炼思维优势（如：列方程等量关系敏锐、计算细心、英语时态语感好），给予正向激励。
* **记录待攻克错题本**：卡壳或出错的题目，精准诊断错因（审题漏看单位、图形无盖漏减面、动词单三遗漏、计算失误）。
* **四大高频指令**：
  * `/report`（“分析我的优势和不足”）：生成结构化学情报告。
  * `/review`（“复习错题 / 查漏补缺”）：调取历史易错点，出生活化“双胞胎变式题”进行攻坚。
  * `/mistakes`（“查看错题本”）：查看当前待攻克的错题清单。
  * `/strengths`（“夸夸我的强项”）：帮助孩子建立学科自信。

### 4. 🏙️ 深度适配上海本土教育特色
* **学制**：上海为“五四学制”，五年级为毕业年级，注重向初中预初的抽象逻辑思维过渡。
* **数学（沪教版/上教版）**：攻克简易方程（一）（二）列方程解应用题（找等量关系）、长方体正方体表面积体积（几何小实践）。
* **英语（牛津上海版）**：攻克时态综合（一般现在/过去/将来/进行）、不规则动词、写作（三段式思维导图）。
* **语文（统编版）**：攻克文言启蒙（《杨氏之子》）、说明文方法、细节描写。

---

## 🚀 跨平台安装指引

### 1. 腾讯 WorkBuddy（桌面 AI 智能体工作台）
* **本地导入**：打开 WorkBuddy，进入【设置 $\to$ 技能扩展 / 专家管理 $\to$ 导入本地技能】，选择本仓库目录即可。
* **创建专家**：点击【+ 创建专家】，将 [`INSTALL_GUIDE.md`](INSTALL_GUIDE.md) 中的 Prompt 复制粘贴即可。

### 2. 字节跳动 豆包（Doubao 手机 App / 网页端）
1. 打开 [豆包官网](https://www.doubao.com) 或 App，进入【智能体 $\to$ + 创建智能体】；
2. 名称填写：`小希姐姐（上海五年级伴学导师）`；
3. 将 [`INSTALL_GUIDE.md`](INSTALL_GUIDE.md) 中的【人设与回复逻辑】复制到配置中；
4. 保存发布，可直接分享给孩子的平板或手机使用。

### 3. Antigravity / OpenClaw / Claude Code
将仓库克隆至技能目录即可自动识别：
```bash
git clone https://github.com/zf617525633/shanghai-grade5-tutor.git ~/.gemini/antigravity/skills/shanghai-grade5-tutor
```

---

## 💬 常用辅导对话示例

* **求助列方程**：
  > **孩子**：“小明买了3支钢笔和5本笔记本一共45元，每本笔记本3元，钢笔每支多少元？直接告诉我答案！”  
  > **导师**：“收到！这道题很有意思，我们一起来秒杀它~ 第一步，题目里说‘每本笔记本3元，买了5本’，小明买笔记本一共花掉了多少钱？你先算算告诉姐姐？”

* **学情诊断**：
  > **家长/孩子**：“姐姐，帮我分析一下最近我的优势和不足吧！”  
  > **导师**：自动生成包含【🌟 优势闪光点】、【🎯 薄弱点诊断】与【💡 查漏补缺处方】的结构化报告。

* **错题攻坚**：
  > **孩子**：“我想复习错题，给我出两道针对性的变式练习题吧！”  
  > **导师**：提取长方体表面积易错点，换成“制作一个无盖手账收纳盒”的生活情景变式题进行巩固。

---

## 📁 目录结构

```text
shanghai-grade5-tutor/
├── SKILL.md                          # 核心技能与交互规则定义
├── INSTALL_GUIDE.md                  # 豆包与腾讯 WorkBuddy 跨平台配置指引
├── README.md                         # 详细介绍与使用文档
├── LICENSE                           # MIT 开源协议
├── references/
│   └── shanghai_curriculum_guide.md  # 沪教版/牛津版/统编版全科知识图谱与考点清单
└── scripts/
    └── tracker.py                    # 学情追踪、错题记录与诊断报告生成引擎
```

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。
