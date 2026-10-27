# Case B: Mistral 7B — 原 PDF 第 4 页 中文翻译

## 范围与来源
- 输入：`materials/input.pdf`（Mistral 7B, arXiv:2310.06825v1 原 PDF 第 4 页，单页 612×792 pt）。
- 输出：`out/translated.pdf`（1 页，页面尺寸与输入一致）。
- 排版依据为原 PDF；`materials/source.txt` 与 PDF 文本层一致，无抽取噪声差异（表格数字按行平铺，列对齐以 PDF 为准）。
- 翻译引擎：会话提供的 `skill/engine/pdf_zh_translator`（SuperTranslate 工作流），本地模型 `deepseek-v4-pro-0813`。

## 完成情况
- 正文全部自然段、图/表标题、小节标题均已译为中文，在原位置排版。
- 数学/编号/表格数字/图形全部保留：图4（位图）、表2（12 指标×4 模型）、表3（对话模型）数值原样保留；图内英文标签保留（位图无文本层，无法翻译）。
- 未用另附摘要页替代正文翻译。

## 核心阅读结果（含来源定位）
详见 `out/reading-audit.json`（8 个自然段，含 bbox、英文原文、中文、关键术语、说明）。要点：
1. **图4**（bbox 108,207–505,246）：Mistral 7B 在所有基准上显著优于 Llama 2 7B 与 13B，在数学/代码生成/推理上大幅超越 Llama 1 34B。
2. **表2**（bbox 108,266–500,321）：Mistral 7B 在所有指标上优于 Llama 2 13B，代码性能接近 Code-Llama 7B（HumanEval 30.5 vs 31.1、MBPP 47.5 vs 52.5），且不牺牲非代码基准。
3. **规模与效率**（bbox 108,381–506,446）：推理/理解/STEM 推理等效规模 >3x；知识基准压缩率 1.9x（作者推测因参数数量限制）。
4. **评估差异**（bbox 108,452–505,484）：MBPP 用人工验证子集；TriviaQA 不提供维基百科上下文。
5. **表3**（bbox 314,638–505,667）：Mistral 7B Instruct 在 MT-Bench 上优于所有 7B 模型（6.84 vs 6.27/6.17），与 13B Chat 相当（6.84 vs 6.65/6.57）。
6. **人工评估**（bbox 108,680–504,722）：截至 2023-10-06，Mistral 7B 被偏好 5020 次 vs Llama 2 13B 4143 次。

## 指标解释（仅依据本页信息）
- 表2 指标（MMLU、HellaSwag、WinoGrande、PIQA、Arc-e/Arc-c、NQ、TriviaQA、HumanEval、MBPP、MATH、GSM8K）为常见基准，本页仅给出各模型百分比得分，未给出指标定义；数值越高越好。
- 表3 指标：Chatbot Arena ELO Rating（Elo 评分，越高越好）与 MT-Bench（对话质量评分，越高越好，Mistral 7B Instruct 为 6.84±0.07）。
- 比较对象均为原始模型名（Llama 2 7B/13B、Code-Llama 7B、Llama 1 34B、WizardLM/Vicuna/Alpaca 等），未改写。

## 实际检查（机器可读）
`out/checks.json`：
- 页数一致：True；页面尺寸一致：True。
- 图保留：True；表格数字全部保留：True；关键数值（含 5020/4143）全部在位：True。
- 中文字符数：473；正文已译：True；残留英文整句：[]。
- 引擎 QA（`out/inspect.json`）：0 issue / 0 error。

## 未解决问题 / 缺口
- 图4为位图，其内部坐标轴/图例标签不在文本层，无法逐项翻译或核对图内具体基准名称与数值；仅能依据图4标题与表2数值解释。
- 图5（等效模型规模）与图6（人工评估界面）在本页之外，正文引用它们但本页无法核对其内容。
- 表2/表3的指标定义（如 MMLU、HellaSwag、WinoGrande、PIQA、Arc-e/Arc-c、NQ、TriviaQA、HumanEval、MBPP、MATH、GSM8K、MT-Bench、Chatbot Arena ELO）本页未给出定义，仅能按通用含义解释，不能从本页推断其具体评测细节。
- '所有基准上显著优于'、'未使用专有数据或训练技巧'、'可能由于参数数量限制'等均为作者主张/推测，本页未提供独立验证。
- source.txt 与 PDF 文本层一致（无抽取噪声差异），但 source.txt 将表格数字按行平铺，列对齐需以 PDF 为准。

## 运行记录
- 翻译：8 个文本块翻译，43 个块跳过（表格/图/页码保留）；耗时约 14s。
- 引擎警告：检测到 generic_two_column 布局（置信度 0.72）；保留源字体以维持图/公式字形映射；pikepdf 缺失故用标准保存（不影响结果）。
- 字体：使用 `common-assets/NotoSansSC.ttf`（SIL OFL）。注：PDF 文本层抽取时部分汉字以 CJK 兼容表意字符（如 不=不、理=理）形式出现，属字体 cmap 映射现象，字形渲染正确、缓存中为规范汉字，不影响阅读。
- 失败/人工干预：无。原文件未改动。

## 交付物
- `out/translated.pdf`（中文译文 PDF）
- `out/reading-audit.json`（双语阅读核对记录，含来源 bbox）
- `out/translated-text.txt` / `out/original-text.txt`（可核验文本导出）
- `out/checks.json`（机器可读检查）
- `out/translation-cache.jsonl`（翻译缓存）
- `out/inspect.json`（引擎 QA）
- `out/output.md`（本文件）
