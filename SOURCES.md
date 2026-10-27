# 来源、许可与贡献

## 论文与图表

Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, William El Sayed. **Mistral 7B**. arXiv:2310.06825v1，2023-10-10。来源：https://arxiv.org/abs/2310.06825v1 。论文页面的 license 链接为 CC BY 4.0：https://creativecommons.org/licenses/by/4.0/ 。于 2026-10-27 核对。

`paper/input.pdf` 为原 PDF 第4页的单页提取；`paper/source.txt` 是该页文本导出，附来源标题。提取改变页数，不改写页面。`verification/table2-original.png` 为此页表2区域的渲染；`verification/page-comparison.png` 添加了并排版式和标签，右侧为模型生成的中文翻译。`practice/out/translated.pdf` 与双语阅读记录包含原文的翻译/改编，未获论文作者背书。图表差值图与 CSV 由原表2数据整理、计算，不是新的性能测量。论文材料、这些翻译与图表改编继续注明原作者，并按 CC BY 4.0 分享。

## 上游工具与本次代码

SuperTranslate 上游：https://github.com/asimfish/super_translate 。使用 commit `f16a641b9c7be155938d6b0e047b24e944dd4668`，许可 AGPL-3.0-or-later；完整许可在根目录 `LICENSE`。上游翻译引擎没有修改，本包不重新分发整个引擎；安装时从该固定版本取得。引擎的实现、上游示例和上游开发成果不属于本次原创贡献。

本仓库新增的核查/重放脚本及原会话产生的脚本按 AGPL-3.0-or-later 提供，完整可编辑源码已随包给出。`practice/SKILL.md` 是上次实践为跨平台调用与阅读证据输出整理的入口，沿用上游工作流并注明来源，不是全新翻译算法。原始 AI 提示、请求、输出和执行记录保留实际内容；其事实准确性由正文与核查结果单独说明。

本文、新增的核查记录、说明文档按 CC BY 4.0 分享，署名为 Suguangliunian / Codex-assisted case study（2026）。本次新增工作是问题界定、证据整理、数值交叉核查、失败分析、配图和复核脚本。Codex 辅助实现、分析和写作，未声称由人手逐句完成；也未宣称本工作获得论文作者、上游作者或比赛主办方背书。

## 字体

`assets/NotoSansSC.ttf` 来自 Google Fonts 的 Noto Sans SC，可变字体原文件 `ofl/notosanssc/NotoSansSC[wght].ttf`，2026-10-27 下载，未修改。来源：https://github.com/google/fonts/tree/main/ofl/notosanssc 。字体按 SIL Open Font License 1.1 分发，随附 `assets/OFL.txt`。原文件 SHA256 在 `practice/provenance.json` 中记录；重放用随包字体，不依赖动态下载到的新版。

## 公开范围

本包仅含公开论文片段、开源工具的使用方法、已获用户委托的实践记录与新增核查。网关 API Token、Bohrium AK、GitHub 凭据、用户登录资料、其他会话及其他论文案例不在包内。日志中的 localhost 地址与 `local-session-only` 是原实验的临时代理配置，不是可复用服务或真实凭据。
