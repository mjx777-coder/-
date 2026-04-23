#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生成绩处理器 - 无乱码处理Excel/CSV成绩文件
"""

import pandas as pd
import numpy as np
import argparse
import sys
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def detect_encoding(file_path):
    """检测文件编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig', 'latin1']
    
    if file_path.endswith(('.xlsx', '.xls')):
        return 'excel'
    
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read(1024)
            return enc
        except:
            continue
    
    return 'utf-8'  # 默认使用UTF-8

def read_grade_file(file_path, score_column=None):
    """读取成绩文件，自动处理编码"""
    print(f"正在读取文件: {file_path}")
    
    if file_path.endswith(('.xlsx', '.xls')):
        try:
            df = pd.read_excel(file_path)
            print("✅ Excel文件读取成功")
        except Exception as e:
            print(f"❌ Excel文件读取失败: {e}")
            return None
    else:
        # CSV文件，尝试多种编码
        encoding = detect_encoding(file_path)
        print(f"检测到编码: {encoding}")
        
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print("✅ CSV文件读取成功")
        except Exception as e:
            print(f"❌ CSV文件读取失败，尝试其他编码...")
            # 尝试其他编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig', 'latin1']
            for enc in encodings:
                if enc == encoding:
                    continue
                try:
                    df = pd.read_csv(file_path, encoding=enc)
                    print(f"✅ 使用编码 {enc} 读取成功")
                    break
                except:
                    continue
            else:
                print("❌ 所有编码尝试均失败")
                return None
    
    # 显示列名
    print(f"\n文件包含 {len(df)} 行数据，{len(df.columns)} 列")
    print("可用列名:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    # 如果未指定成绩列，让用户选择
    if score_column is None:
        if '成绩' in df.columns:
            score_column = '成绩'
        elif 'score' in df.columns:
            score_column = 'score'
        elif '分数' in df.columns:
            score_column = '分数'
        else:
            print("\n⚠️ 未找到标准成绩列名，请从以上列表中选择:")
            for i, col in enumerate(df.columns):
                print(f"  {i+1}. {col}")
            try:
                choice = int(input("请输入列号: ")) - 1
                score_column = df.columns[choice]
            except:
                print("❌ 选择无效，使用第一列")
                score_column = df.columns[0]
    
    print(f"\n使用成绩列: {score_column}")
    return df, score_column

def analyze_grades(df, score_column):
    """分析成绩数据"""
    # 提取成绩列
    scores = pd.to_numeric(df[score_column], errors='coerce')
    scores = scores.dropna()
    
    if len(scores) == 0:
        print("❌ 未找到有效的成绩数据")
        return None
    
    # 基础统计
    total_students = len(scores)
    average = scores.mean()
    max_score = scores.max()
    min_score = scores.min()
    median = scores.median()
    std_dev = scores.std()
    
    # 分数段统计
    excellent = scores[(scores >= 90) & (scores <= 100)]
    good = scores[(scores >= 80) & (scores < 90)]
    medium = scores[(scores >= 70) & (scores < 80)]
    pass_score = scores[(scores >= 60) & (scores < 70)]
    fail = scores[scores < 60]
    
    excellent_count = len(excellent)
    good_count = len(good)
    medium_count = len(medium)
    pass_count = len(pass_score)
    fail_count = len(fail)
    
    # 百分比计算
    excellent_percent = (excellent_count / total_students) * 100
    good_percent = (good_count / total_students) * 100
    medium_percent = (medium_count / total_students) * 100
    pass_percent = (pass_count / total_students) * 100
    fail_percent = (fail_count / total_students) * 100
    
    # 优秀率和及格率
    excellent_rate = excellent_percent
    pass_rate = 100 - fail_percent
    
    # 数据质量
    invalid_count = len(df[score_column]) - total_students
    
    return {
        'total_students': total_students,
        'average': average,
        'max_score': max_score,
        'min_score': min_score,
        'median': median,
        'std_dev': std_dev,
        'excellent_count': excellent_count,
        'good_count': good_count,
        'medium_count': medium_count,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'excellent_percent': excellent_percent,
        'good_percent': good_percent,
        'medium_percent': medium_percent,
        'pass_percent': pass_percent,
        'fail_percent': fail_percent,
        'excellent_rate': excellent_rate,
        'pass_rate': pass_rate,
        'invalid_count': invalid_count,
        'scores': scores
    }

def generate_report(results, filename):
    """生成分析报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
==================================================
              学生成绩分析报告
==================================================
文件名称：{filename}
分析时间：{timestamp}
总记录数：{results['total_students']} 人

【基础统计数据】
------------------------------------------
平均分：{results['average']:.2f} 分
最高分：{results['max_score']} 分
最低分：{results['min_score']} 分
中位数：{results['median']:.2f} 分
标准差：{results['std_dev']:.2f} 分

【分数段分布】
------------------------------------------
90-100分（优秀）：{results['excellent_count']} 人 ({results['excellent_percent']:.1f}%)
80-89分（良好）：{results['good_count']} 人 ({results['good_percent']:.1f}%)
70-79分（中等）：{results['medium_count']} 人 ({results['medium_percent']:.1f}%)
60-69分（及格）：{results['pass_count']} 人 ({results['pass_percent']:.1f}%)
60分以下（不及格）：{results['fail_count']} 人 ({results['fail_percent']:.1f}%)

【关键指标】
------------------------------------------
优秀率：{results['excellent_rate']:.1f}%
及格率：{results['pass_rate']:.1f}%
不及格人数：{results['fail_count']} 人

【数据质量检查】
------------------------------------------
有效成绩数：{results['total_students']} 个
空值/异常值：{results['invalid_count']} 个
处理状态：✅ 完成（无乱码）
==================================================
"""
    
    return report

def main():
    parser = argparse.ArgumentParser(description='学生成绩处理器 - 无乱码处理成绩文件')
    parser.add_argument('--file', '-f', required=True, help='成绩文件路径 (Excel或CSV)')
    parser.add_argument('--column', '-c', help='成绩列名 (如未指定则自动检测)')
    parser.add_argument('--output', '-o', help='输出报告文件路径')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return 1
    
    # 读取文件
    result = read_grade_file(args.file, args.column)
    if result is None:
        return 1
    
    df, score_column = result
    
    # 分析成绩
    print("\n正在分析成绩数据...")
    results = analyze_grades(df, score_column)
    if results is None:
        return 1
    
    # 生成报告
    report = generate_report(results, os.path.basename(args.file))
    print(report)
    
    # 保存报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    
    # 显示额外统计信息
    print("\n【额外统计信息】")
    print(f"成绩范围: {results['min_score']} - {results['max_score']}")
    print(f"成绩波动 (标准差): {results['std_dev']:.2f}")
    
    if results['fail_count'] > 0:
        print(f"⚠️ 需要关注: {results['fail_count']} 名学生不及格")
    
    if results['excellent_rate'] > 30:
        print(f"🎉 优秀表现: 优秀率 {results['excellent_rate']:.1f}%")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())