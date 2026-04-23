---
name: grade-processor
description: 学生成绩处理器：无乱码处理Excel/CSV成绩文件，输出完整统计数据
---

# 学生成绩处理器

专门处理学生成绩文件，确保无乱码输出，提供完整的成绩数据分析。

## 功能特点

✅ **无乱码处理** - 自动检测并处理文件编码问题
✅ **多格式支持** - Excel (.xlsx, .xls) 和 CSV 文件
✅ **完整统计** - 提供详细的成绩分布分析
✅ **可视化输出** - 清晰的表格和图表格式
✅ **安全可靠** - 不泄露学生隐私信息

## 工作流程

### 1. 文件准备
- 支持Excel (.xlsx, .xls) 和 CSV格式
- 自动检测文件编码（UTF-8, GBK, GB2312等）
- 处理中文字符乱码问题

### 2. 数据读取
```python
# 自动检测编码
if file.endswith('.csv'):
    # 尝试多种编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
    for enc in encodings:
        try:
            df = pd.read_csv(file, encoding=enc)
            break
        except:
            continue
elif file.endswith(('.xlsx', '.xls')):
    df = pd.read_excel(file)
```

### 3. 成绩分析指标

**基础统计：**
- 总人数
- 平均分（保留2位小数）
- 最高分
- 最低分
- 中位数
- 标准差

**分数段分布：**
- 优秀 (90-100分)
- 良好 (80-89分)
- 中等 (70-79分)
- 及格 (60-69分)
- 不及格 (<60分)

**百分比计算：**
- 优秀率 = 优秀人数 / 总人数 × 100%
- 及格率 = (总人数 - 不及格人数) / 总人数 × 100%

### 4. 输出格式

```
==================================================
              学生成绩分析报告
==================================================
文件名称：{filename}
分析时间：{timestamp}
总记录数：{total_students} 人

【基础统计数据】
------------------------------------------
平均分：{average:.2f} 分
最高分：{max_score} 分
最低分：{min_score} 分
中位数：{median:.2f} 分
标准差：{std_dev:.2f} 分

【分数段分布】
------------------------------------------
90-100分（优秀）：{excellent_count} 人 ({excellent_percent:.1f}%)
80-89分（良好）：{good_count} 人 ({good_percent:.1f}%)
70-79分（中等）：{medium_count} 人 ({medium_percent:.1f}%)
60-69分（及格）：{pass_count} 人 ({pass_percent:.1f}%)
60分以下（不及格）：{fail_count} 人 ({fail_percent:.1f}%)

【关键指标】
------------------------------------------
优秀率：{excellent_rate:.1f}%
及格率：{pass_rate:.1f}%
不及格人数：{fail_count} 人

【数据质量检查】
------------------------------------------
有效成绩数：{valid_scores} 个
空值/异常值：{invalid_count} 个
处理状态：✅ 完成（无乱码）
==================================================
```

### 5. 可选输出

**成绩分布直方图：**
```python
import matplotlib.pyplot as plt
plt.hist(scores, bins=10, edgecolor='black')
plt.title('成绩分布直方图')
plt.xlabel('分数')
plt.ylabel('人数')
plt.grid(True, alpha=0.3)
```

**数据导出：**
- 导出分析结果为CSV文件
- 导出统计摘要为文本文件
- 可选生成可视化图表

## 使用示例

```bash
# 处理Excel文件
python grade_processor.py --file "学生成绩.xlsx" --column "成绩"

# 处理CSV文件（指定编码）
python grade_processor.py --file "成绩.csv" --column "score" --encoding "gbk"

# 输出详细报告
python grade_processor.py --file "data.xlsx" --output "分析报告.txt"
```

## 错误处理

1. **文件不存在** → 提示用户检查路径
2. **编码错误** → 自动尝试多种编码
3. **列名不存在** → 显示可用列名列表
4. **数据格式错误** → 跳过无效行并报告
5. **内存不足** → 分块处理大文件

## 隐私保护

- 不输出学生姓名与成绩的对应关系
- 分析完成后可删除临时文件
- 不在日志中记录原始数据
- 支持数据脱敏处理

## 安装依赖

```bash
pip install pandas openpyxl matplotlib
```

## 更新日志

- v1.0: 基础成绩处理功能
- v1.1: 增强编码处理，解决乱码问题
- v1.2: 添加可视化输出选项
- v1.3: 优化错误处理和用户提示

---

**教学龙虾提示**：使用此skill时，请确保成绩文件格式正确。如有乱码问题，系统会自动尝试多种编码解决方案。