#!/usr/bin/env python3
"""
上海五年级伴学导师 - 学情追踪与错题分析模块 (Student Learning Tracker)
支持：首次学情强制初始化、做题记录、错题本归纳、优势与薄弱点诊断、生成个性化查漏补缺练习。
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
        "profile": {
            "initialized": False,
            "name": "",
            "age": None,
            "grade": "上海小学五年级（五四学制毕业班）",
            "scores": {
                "math": None,
                "english": None,
                "chinese": None
            },
            "init_time": None
        },
        "records": [],
        "knowledge_map": {}
    }

def save_data(data, filepath=DEFAULT_DATA_FILE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_profile_initialized(filepath=DEFAULT_DATA_FILE):
    """
    检查学生档案是否已经完成初始化（必须包含年龄和语数英三科成绩）
    """
    data = load_data(filepath)
    profile = data.get("profile", {})
    if not profile.get("initialized"):
        return False
    scores = profile.get("scores", {})
    has_age = profile.get("age") is not None
    has_scores = (
        scores.get("math") is not None and
        scores.get("english") is not None and
        scores.get("chinese") is not None
    )
    return bool(has_age and has_scores)

def init_student_profile(age, math_score, english_score, chinese_score, name="宝贝", filepath=DEFAULT_DATA_FILE):
    """
    首次使用初始化学生档案
    """
    data = load_data(filepath)
    data["profile"] = {
        "initialized": True,
        "name": name if name else "宝贝",
        "age": int(age) if str(age).isdigit() else age,
        "grade": "上海小学五年级（五四学制毕业班）",
        "scores": {
            "math": float(math_score),
            "english": float(english_score),
            "chinese": float(chinese_score)
        },
        "init_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_data(data, filepath)
    return data["profile"]

def record_question(subject, topic, question_text, is_correct, mistake_reason="", child_answer="", correct_answer="", filepath=DEFAULT_DATA_FILE):
    """
    记录一次做题结果（必须在初始化后才能记录）
    """
    if not is_profile_initialized(filepath):
        raise ValueError("请先完成孩子学情信息的初始化建档（年龄、语数英成绩）！")
        
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
    生成学情分析报告：结合初始分数基线与互动做题记录，找出优势和薄弱项
    """
    data = load_data(filepath)
    profile = data.get("profile", {})
    if not profile.get("initialized"):
        return "⚠️ 当前尚未完成学情初始化建档。请先提供孩子的年龄及最近一次语文、数学、英语成绩！"
        
    name = profile.get("name", "宝贝")
    age = profile.get("age", 11)
    scores = profile.get("scores", {})
    records = data.get("records", [])
    
    total = len(records)
    correct_count = sum(1 for r in records if r["is_correct"])
    accuracy = (correct_count / total) * 100 if total > 0 else 0
    
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
            
    weaknesses.sort(key=lambda x: (x["accuracy"], -x["wrong"]))
    pending_mistakes = [r for r in records if not r["is_correct"] and r.get("review_status") == "pending"]
    
    report_lines = [
        f"# 📊 【{name}】上海五年级伴学诊断档案",
        f"- **年龄**：{age} 岁 | **学制**：上海五四学制小学毕业班",
        f"- **基线成绩**：数学 {scores.get('math', 0)} 分 | 英语 {scores.get('english', 0)} 分 | 语文 {scores.get('chinese', 0)} 分",
        f"- **伴学互动题数**：{total} 道 | **独立正确率**：{accuracy:.1f}%",
        "",
        "## 🌟 孩子的优势闪光点",
    ]
    
    # 结合基准成绩与做题表现
    highest_sub = max(scores, key=scores.get)
    sub_names = {"math": "数学", "english": "英语", "chinese": "语文"}
    report_lines.append(f"- **基线优势**：最近一次【{sub_names.get(highest_sub)}】考了 {scores.get(highest_sub)} 分，表现最为突出，具备良好的学科领悟力！")
    
    if strengths:
        for s in strengths:
            report_lines.append(f"- **互动亮点**：【{s['subject']}·{s['topic']}】练习 {s['total']} 次，正确率 {s['accuracy']:.0f}%，掌握牢固，逻辑清晰！👏")
    else:
        report_lines.append("- **学习态度**：能积极顺着启发思路主动探索，审题有耐心！")
        
    report_lines.append("")
    report_lines.append("## 🎯 薄弱点与知识漏洞诊断")
    lowest_sub = min(scores, key=scores.get)
    if scores.get(lowest_sub, 100) < 90:
        report_lines.append(f"- **重点关注**：最近【{sub_names.get(lowest_sub)}】（{scores.get(lowest_sub)} 分）存在一定提分空间，是小初衔接的关键发力点。")
    if weaknesses:
        for w in weaknesses:
            report_lines.append(f"- **具体漏洞**：【{w['subject']}·{w['topic']}】练习 {w['total']} 次中受阻 {w['wrong']} 次（掌握度 {w['accuracy']:.0f}%）。")
    else:
        report_lines.append("- 当前互动题目均顺利攻克，整体状态平稳！")
        
    report_lines.append("")
    report_lines.append("## 💡 查漏补缺攻坚建议")
    if pending_mistakes:
        report_lines.append(f"目前有 **{len(pending_mistakes)}** 道错题待复习巩固：")
        for idx, m in enumerate(pending_mistakes[:5], 1):
            reason_str = f"（难点：{m['mistake_reason']}）" if m.get("mistake_reason") else ""
            report_lines.append(f"{idx}. 【{m['subject']}·{m['topic']}】{m['question'][:40]}... {reason_str}")
        report_lines.append("\n**下一步行动**：对导师说“复习错题”，小希姐姐将带孩子进行同类型变式题的针对性强化！")
    else:
        report_lines.append("所有互动错题均已掌握！建议针对相对薄弱科目进行针对性变式拓展或新知识预热！")
        
    return "\n".join(report_lines)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "is_init":
        print("true" if is_profile_initialized() else "false")
    elif len(sys.argv) > 1 and sys.argv[1] == "init":
        # python3 tracker.py init <age> <math> <english> <chinese> [name]
        age = sys.argv[2]
        m = sys.argv[3]
        e = sys.argv[4]
        c = sys.argv[5]
        name = sys.argv[6] if len(sys.argv) > 6 else "宝贝"
        res = init_student_profile(age, m, e, c, name)
        print("初始化成功！" + json.dumps(res, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "report":
        print(generate_diagnostic_report())
    else:
        print(generate_diagnostic_report())
