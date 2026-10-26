#!/usr/bin/env python3
"""
上海五年级伴学导师 - 学情追踪与错题分析模块 (Student Learning Tracker)
支持记录做题记录、错题本归纳、优势与薄弱点诊断、生成个性化查漏补缺练习。
"""

import json
import os
import sys
from datetime import datetime

DEFAULT_DATA_FILE = os.path.expanduser("~/.gemini/antigravity/skills/shanghai-grade5-tutor/student_data.json")

def load_data(filepath=DEFAULT_DATA_FILE):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "student_info": {
            "name": "宝贝",
            "grade": "上海小学五年级",
            "school_system": "五四学制"
        },
        "records": [],
        "knowledge_map": {}
    }

def save_data(data, filepath=DEFAULT_DATA_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_question(subject, topic, question_text, is_correct, mistake_reason="", child_answer="", correct_answer="", filepath=DEFAULT_DATA_FILE):
    """
    记录一次做题结果
    """
    data = load_data(filepath)
    entry = {
        "id": len(data["records"]) + 1,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "subject": subject,  # 数学 / 英语 / 语文
        "topic": topic,      # 如：列方程解应用题 / 长方体表面积 / 一般过去时
        "question": question_text,
        "is_correct": bool(is_correct),
        "mistake_reason": mistake_reason,  # 审题不仔细 / 计算失误 / 等量关系没找对 / 概念不清
        "child_answer": child_answer,
        "correct_answer": correct_answer,
        "review_status": "pending" if not is_correct else "mastered"
    }
    data["records"].append(entry)
    
    # 更新知识点统计
    k_key = f"{subject}::{topic}"
    if k_key not in data["knowledge_map"]:
        data["knowledge_map"][k_key] = {"total": 0, "correct": 0, "wrong": 0}
    data["knowledge_map"][k_key]["total"] += 1
    if is_correct:
        data["knowledge_map"][k_key]["correct"] += 1
    else:
        data["knowledge_map"][k_key]["wrong"] += 1
        
    save_data(data, filepath)
    return entry

def generate_diagnostic_report(filepath=DEFAULT_DATA_FILE):
    """
    生成学情分析报告：找出优势和薄弱项，给出补不足建议
    """
    data = load_data(filepath)
    records = data.get("records", [])
    if not records:
        return "当前还没有做题记录哦。和导师一起完成几道题目后，就可以为你生成专属学情分析报告！"
    
    total = len(records)
    correct_count = sum(1 for r in records if r["is_correct"])
    accuracy = (correct_count / total) * 100 if total > 0 else 0
    
    # 统计知识点
    km = data.get("knowledge_map", {})
    strengths = []
    weaknesses = []
    
    for k_key, stats in km.items():
        sub, top = k_key.split("::") if "::" in k_key else ("综合", k_key)
        acc = (stats["correct"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        item = {
            "subject": sub,
            "topic": top,
            "total": stats["total"],
            "correct": stats["correct"],
            "wrong": stats["wrong"],
            "accuracy": acc
        }
        if stats["total"] >= 2 and acc >= 80:
            strengths.append(item)
        elif stats["wrong"] >= 1:
            weaknesses.append(item)
            
    # 按错误率排序薄弱点
    weaknesses.sort(key=lambda x: (x["accuracy"], -x["wrong"]))
    
    # 提取待攻克的错题
    pending_mistakes = [r for r in records if not r["is_correct"] and r.get("review_status") == "pending"]
    
    report_lines = [
        f"# 📊 上海五年级伴学诊断报告 ({datetime.now().strftime('%Y-%m-%d')})",
        "",
        f"**累计互动题数**：{total} 道 | **独立正确率**：{accuracy:.1f}%",
        "",
        "## 🌟 孩子的优势闪光点",
    ]
    
    if strengths:
        for s in strengths:
            report_lines.append(f"- **【{s['subject']}】{s['topic']}**：共练习 {s['total']} 次，正确率 {s['accuracy']:.0f}%！这部分基础扎实，逻辑反应迅速，值得继续保持！🎉")
    else:
        report_lines.append("- 孩子思维很活跃，敢于探索新题型，每次能够主动尝试梳理已知条件，继续积累会有更多优势模块显现！✨")
        
    report_lines.append("")
    report_lines.append("## 🎯 薄弱点与知识漏洞诊断")
    if weaknesses:
        for w in weaknesses:
            report_lines.append(f"- **【{w['subject']}】{w['topic']}**：练习 {w['total']} 次，遇到困难 {w['wrong']} 次（掌握度 {w['accuracy']:.0f}%）。")
    else:
        report_lines.append("- 目前未发现明显知识漏洞，综合状态良好！")
        
    report_lines.append("")
    report_lines.append("## 💡 查漏补缺与专项攻坚处方")
    if pending_mistakes:
        report_lines.append(f"目前有 **{len(pending_mistakes)}** 道错题待复习巩固：")
        for idx, m in enumerate(pending_mistakes[:5], 1):
            reason_str = f"（难点：{m['mistake_reason']}）" if m.get("mistake_reason") else ""
            report_lines.append(f"{idx}. 【{m['subject']}·{m['topic']}】{m['question'][:40]}... {reason_str}")
        report_lines.append("\n**下一步建议**：输入 `/review` 或对我说“复习错题”，导师将带孩子进行同类型变式题的趣味巩固，彻底消除知识盲区！")
    else:
        report_lines.append("太棒了！所有错题均已攻克掌握。建议推进下一单元的新课预习或挑战小升初思维拓展题！")
        
    return "\n".join(report_lines)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        print(generate_diagnostic_report())
    elif len(sys.argv) > 1 and sys.argv[1] == "add":
        # 简单 CLI 测试
        record_question(
            subject=sys.argv[2] if len(sys.argv) > 2 else "数学",
            topic=sys.argv[3] if len(sys.argv) > 3 else "简易方程",
            question_text=sys.argv[4] if len(sys.argv) > 4 else "测试题目",
            is_correct=sys.argv[5].lower() == "true" if len(sys.argv) > 5 else True,
            mistake_reason=sys.argv[6] if len(sys.argv) > 6 else ""
        )
        print("记录成功！")
    else:
        print(generate_diagnostic_report())
