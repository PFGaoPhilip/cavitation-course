> Public reading copy: links to the original local ZIPs/PDFs are replaced with the included Markdown textbooks. The audit was performed on the original local archives.

> 公开阅读副本：原始本地 ZIP／PDF 下载链接已替换为所附 Markdown 教材。审核基于原始本地压缩包进行。

# Independent textbook audit / 独立教材审计

## Verdict / 结论

**PASS, after the atlas-heading repair.** I read both supplied ZIP archives directly and compared their source text with the saved course pages. Within the requested audit scope, I found no remaining missing chapter, source heading, source display equation, problem, plot, atlas card, source-theory page, or research appendix. The one presentation defect found during the audit—the escaped `<i>in vitro</i>` in the S387 paper title—was corrected in the saved atlas and coverage pages and rechecked as a real italic element.

**通过，且已修复文献地图标题问题。**我直接读取了两份所给 ZIP 压缩包，并将其中的源文本与保存的课程页面逐项比较。在本次审计范围内，没有发现仍缺失的章节、源标题、源显示公式、习题、图、文献卡、理论原页或研究附录。审计中发现的唯一显示问题——S387 文献题名中的 `<i>in vitro</i>` 被转义成普通文本——已在保存的文献地图和覆盖页面中修复，并确认现在是真正的斜体元素。

## Source routine and course order / 源教材学习顺序与课程安排

The generic-book README and Preface in [Supplied generic textbook](../../reading/Bubble_Cavitation_Dynamics.md) prescribe Chapters 1–7 and the Chapter 13 numerical lab first, followed by Chapters 8–12, measurement and inference in Chapter 14, the Chapter 15 capstone, and Chapter 16’s worked problems. The [saved schedule](../../SCHEDULE.html) follows this routine as G01–G07 → G13 → G08–G12 → G14 → G15 → G16. This keeps all 16 generic chapters ahead of the five project-theory stages T01–T05. The two research appendixes are listed after T05, after the core route.

[Supplied generic textbook](../../reading/Bubble_Cavitation_Dynamics.md) 中通用教材的 README 和前言规定：先学第 1–7 章并运行第 13 章数值实验，再学第 8–12 章、第 14 章测量与反演、第 15 章综合课題，最后学习第 16 章详解习题。[当前课程安排](../../SCHEDULE.html) 按 G01–G07 → G13 → G08–G12 → G14 → G15 → G16 执行。这样全部 16 个通用章节均先于项目理论 T01–T05；两份研究附录排在 T05 之后，也位于主路线完成之后。

The schedule offers all chapters together and labels the new route as prepared content rather than completed study. The page footers repeat that newly prepared chapters are not recorded as mastered. This status is clear in [SCHEDULE.html](../../SCHEDULE.html) and in the linked chapter pages.

课程安排一次备齐了全部章节，并明确将新路线标为已备妥内容，而非已完成学习。各页面页脚也说明，新编章节没有记作已经掌握。这一状态在 [SCHEDULE.html](../../SCHEDULE.html) 及其链接的章节页面中表述清楚。

## Source-text and equation coverage / 源文本与公式覆盖

I independently compared source Markdown headings and display equations from both ZIPs with headings and TeX annotations in the saved HTML pages. All 170 generic-book headings—including the Preface, notation/model-map appendix, and paper-atlas entries—and all 40 project-theory headings, including its orientation, five stages, conclusion, source notes, and preserved-page note, are present at their corresponding pages. All 46 generic-book display equations and all 165 project-theory display equations were found in the corresponding pages. Representative derivations are presented in the page bodies: continuity and Bernoulli lead into the Rayleigh–Plesset wall balance in [G03](../../course/chapters/G03-rayleigh-plesset.html); optical fluence is integrated to pulse energy in [T01](../../course/chapters/T01-optical-deposition.html); and the prescribed trajectory is distinguished from a forward activation/growth prediction in [T03](../../course/chapters/T03-bubble-load-mapping.html). These are lesson contents, not merely reading links or short summaries.

我独立将两份 ZIP 中源 Markdown 的标题与显示公式，同保存的 HTML 页面标题及 TeX 注释进行了比较。通用教材的 170 个标题——包括前言、符号／模型地图附录及文献地图条目——以及项目理论的 40 个标题——包括导读、五个阶段、结论、来源说明和原页说明——均出现在对应页面。通用教材的 46 个显示公式、项目理论的 165 个显示公式也全部出现在相应页面。代表性推导作为正文内容呈现：连续性与 Bernoulli 推导进入 [G03](../../course/chapters/G03-rayleigh-plesset.html) 的 Rayleigh–Plesset 壁面平衡；[T01](../../course/chapters/T01-optical-deposition.html) 从光斑能量面密度积分得到脉冲能量；[T03](../../course/chapters/T03-bubble-load-mapping.html) 则明确区分规定轨迹与正向预测激活／增长。这些是实质课程正文，不只是阅读链接或简短提要。

A separate paragraph-level comparison exactly matched 790 of 799 ordinary content blocks across the 16 generic chapters and five project stages after normalizing Markdown and inline math. I checked the remaining nine against the rendered pages: seven source figure captions are split into localized figure-caption and alt-text elements; one prose block contains inline formulas rendered as separate math nodes; and one G13 code example appears unchanged in the page. Additional direct comparisons matched the generic Preface (14/14 blocks), project-theory orientation (9/9), conclusion and source notes (15/15), notation/model-map appendix (18/18), and atlas prose (191/191). I found no source-prose omission.

另一次逐段比较在规范化 Markdown 与行内公式后，16 个通用章节及五个项目阶段中的 799 个普通内容块有 790 个逐字对应。我又逐项核对其余九项：七段源图注在页面中拆分为本地化图注和替代文本；一段正文含有被单独排版的行内公式；G13 的一段代码示例则与页面代码完全一致。其他直接比较也全部匹配：通用教材前言 14/14 段、项目理论导读 9/9 段、结论与来源说明 15/15 段、符号／模型地图附录 18/18 段，以及文献地图正文 191/191 段。我没有发现源正文遗漏。

Representative governing laws also agree with the source and their surrounding assumptions: the spherical Young–Laplace jump `p_B - p_inf = 2 sigma/R`, the Rayleigh–Plesset pressure balance including surface tension and viscous stress, the Gaussian-beam normalization `E_p = pi*w0^2*F0/2`, and the structural modal balance `M_n*qddot_n + C_n*qdot_n + K_n*q_n = Q_n(t)`. The pages retain definitions, units and model limits alongside these equations.

代表性支配关系与源文及其适用假设一致：球形界面的 Young–Laplace 压差 `p_B - p_inf = 2 sigma/R`、包含表面张力和黏性应力的 Rayleigh–Plesset 压力平衡、高斯光束能量归一化 `E_p = pi*w0^2*F0/2`，以及结构模态平衡 `M_n*qddot_n + C_n*qdot_n + K_n*q_n = Q_n(t)`。各页也保留了相应符号定义、单位和模型边界。

## Problems, plots, reference pages, and atlas / 习题、图、原页与文献地图

The [G16 problem page](../../course/chapters/G16-original-worked-problems.html) contains all 30 original problem sections and titles. Each original problem has a reference answer beginning with an equation, followed immediately by a figure whose alternative text includes a variable key. Dimensional answers carry units where applicable; examples include the three Laplace pressures 144, 14.4 and 1.44 kPa, collapse speed 21.514 m/s, and shape-mode frequency 148.09 kHz. Dimensionless results are presented as ratios rather than assigned artificial units.

[G16 习题页](../../course/chapters/G16-original-worked-problems.html) 包含全部 30 道原题及对应标题。每道原题的参考答案均以公式开头，紧接一幅图；图的替代文本中含有变量说明。具有量纲的结果在适用处均带单位，例如三个 Laplace 压力 144、14.4、1.44 kPa，塌缩速度 21.514 m/s，以及形状模态频率 148.09 kHz。无量纲结果按比值呈现，没有被赋予虚假的单位。

All seven original source plots were independently SHA-256 compared with the PNG files inside the generic-book ZIP; each project copy is byte-identical and appears in its expected chapter: the time-scale plot in G01, Blake-equilibrium plot in G02, Rayleigh-collapse plot in G05, linear-resonance plot in G06, ring-down and monopole-pressure plots in G07, and modal-impulse plot in G12. The [notation/model map](../../course/references/notation-and-model-map.html) retains the source appendix’s headings, equations, notation and model-selection prose.

我将七幅源图的 SHA-256 与通用教材 ZIP 内的 PNG 文件逐一比较，项目中的每份图像均与原文件逐字节一致，并位于对应章节：时间尺度图在 G01，Blake 平衡图在 G02，Rayleigh 塌缩图在 G05，线性共振图在 G06，衰减振荡和单极子压力图在 G07，模态冲量图在 G12。[符号／模型地图](../../course/references/notation-and-model-map.html) 保留了源附录的标题、公式、符号及模型选择正文。

The [paper atlas](../../course/references/paper-atlas.html) has all 35 source IDs and all 35 cards; its prose maps directly to the source atlas. The S387 heading now contains an actual italic `in vitro` element. The [original-theory-pages page](../../course/references/original-theory-pages.html) embeds five local landscape images, each 1516 × 1072 pixels, and links them to pages 33–37 of the supplied theory PDF at [Cavitation_Theory_Step_by_Step_EN_ZH.pdf](../../reading/Cavitation_Theory_Step_by_Step_EN_ZH.md).

[文献地图](../../course/references/paper-atlas.html) 包含全部 35 个源编号和 35 张文献卡；其正文与源地图逐项对应。S387 标题中的 `in vitro` 现在是实际斜体元素。[原理论页面](../../course/references/original-theory-pages.html) 嵌入了五幅本地横向页面图，每幅尺寸为 1516 × 1072 像素，并链接至所给理论 PDF 的第 33–37 页：[Cavitation_Theory_Step_by_Step_EN_ZH.pdf](../../reading/Cavitation_Theory_Step_by_Step_EN_ZH.md)。

## Project-theory qualifications and extension appendixes / 项目理论限定条件与扩展附录

The course preserves the source project’s uneven evidence status: activation remains uncalibrated, (R(t)) is prescribed in the bubble stage, the near-wall loading calculation is conditional on its spherical-flow approximation, and cohesive release remains unresolved. These qualifications appear directly in T02–T04 and in the integrated summaries.

课程保留了源项目各阶段证据强度不均衡这一事实：激活模型尚未标定，气泡阶段规定 (R(t))，近壁载荷计算依赖球形流动近似这一条件，黏聚界面释放仍未解决。这些限定直接出现在 T02–T04 及其综合说明中。

The two separate research extensions, [Appendix A](../../course/appendixes/A-hydrogel.html) and [Appendix B](../../course/appendixes/B-pressure-limits.html), follow the five project stages in the schedule. Appendix A describes the supplied hydrogel stamp as a millisecond water-vapor blister and interfacial-fracture actuator. It says the paper does not prove that embedding PFC droplets stabilizes a cavitation jet, and proposes tests for recoil, damping, activation changes and gel damage. This keeps the paper’s demonstrated mechanism separate from the project hypothesis.

两份独立研究扩展——[附录 A](../../course/appendixes/A-hydrogel.html) 和 [附录 B](../../course/appendixes/B-pressure-limits.html)——在课程安排中位于项目理论五阶段之后。附录 A 将所给水凝胶印章描述为毫秒级水蒸气鼓泡与界面断裂致动器，并明确说明论文没有证明将 PFC 液滴嵌入凝胶即可稳定空化射流；附录提出检验回弹、阻尼、激活变化和凝胶损伤的方案。论文已展示的机制与项目假设因此得到区分。

Appendix B attaches evidence type to the high-end values: Reuter and Ohl’s (`>850 m/s`) is a measured lower bound; Brujan et al.’s 960 m/s is a measured maximum; Fan et al.’s roughly 1400 m/s is an imaging average while roughly 3000 m/s is a simulated brief peak; Liang et al.’s 13.5 GPa is a model collapse pressure; and Vassholz et al.’s (`>20 GPa`) shock peak is inferred from X-ray density using an equation of state. It explicitly rejects a universal cavitation maximum and states that measured jet speed is not measured target pressure. The (`U_j = 1400 m/s`) water-hammer calculation is marked unreliable quantitatively at `M = 0.945`.

附录 B 为高值明确标注证据类型：Reuter 与 Ohl 的 (`>850 m/s`) 是实测下界；Brujan 等人的 960 m/s 是实测最大值；Fan 等人的约 1400 m/s 是成像得到的平均速度，而约 3000 m/s 是模拟的短时峰值；Liang 等人的 13.5 GPa 是模型计算的塌缩压力；Vassholz 等人的 (`>20 GPa`) 冲击峰值则是依据 X 射线密度和状态方程反演得到。附录明确否定普适空化最大值，并指出实测射流速度不等于实测目标压力。它还将 (`U_j = 1400 m/s`)、`M = 0.945` 条件下的水锤计算标记为不具可靠定量地位。

## Audit limit / 审计边界

This verdict covers source fidelity, course order, the requested figures and references, answer structure, and scientific qualifications in the saved local pages. I did not require or perform new physical experiments. I also did not certify final layout in every browser; this report is a content and local-asset audit.

本结论覆盖保存的本地页面中的源内容忠实度、课程顺序、指定图与参考资料、答案结构及科学限定条件。我没有要求或开展新的物理实验，也没有认证所有浏览器中的最终页面布局；本报告属于内容与本地资源审计。
