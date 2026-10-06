---
title: "From Laser Energy to Film Release"
subtitle: "A Step-by-Step Derivation of Cavitation-Transfer Theory"
chinese-title: "从激光能量到薄膜释放"
chinese-subtitle: "空化转印理论的逐步推导"
date: "25 September 2026 / 2026年9月25日"
---

# Reader’s orientation / 阅读导引

**Scope.** This English–Chinese edition translates the preceding explanation. It distinguishes the five-stage framework and screening results in the supplied PDF [S1] from the intermediate explanatory derivations. Equations are shared by both languages. Citations use the original source-page numbers; the five original pages are reproduced unchanged in Appendix A.

**范围。** 本英汉双语版翻译前文的逐步讲解，并区分所提供 PDF [S1] 中的五阶段框架与筛查结果，以及为讲解而补充的中间推导。两种语言共用公式。引文使用原始材料页码，五页原文在附录 A 中原样收录。

For a mechanics graduate, the most useful starting point is to regard a bubble as a **moving internal boundary**. Its radius is a displacement coordinate, its internal pressure provides a driving force, and the surrounding liquid supplies inertia and viscous resistance.

对于具有力学背景的毕业生，最有用的切入点是把气泡看作一个**运动的内部边界**。它的半径是一个位移坐标，内部压力提供驱动力，而周围液体提供惯性与黏性阻力。

The difficulty is connecting that familiar mechanics to two additional questions: **how the bubble becomes activated, and how its motion causes an interface to separate**.

难点在于把这些熟悉的力学概念与另外两个问题连接起来：**气泡如何被激活，以及气泡运动如何导致界面分离**。

The source organizes this into five stages:

原始材料将这一过程组织为五个阶段：

$$
\begin{gathered}
\text{Optical energy deposition / 光能沉积}\\
\downarrow\\
\text{Activation probability / 激活概率}\\
\downarrow\\
\text{Bubble motion and pressure / 气泡运动与压力}\\
\downarrow\\
\text{Structural response and release / 结构响应与释放}\\
\downarrow\\
\text{Sensitivity and measurements / 敏感性与测量}
\end{gathered}
$$

A central distinction in the source is that these stages are not equally established: the optical source is energy-normalized, the activation law is uncalibrated, the bubble trajectory is prescribed, and interface release remains unresolved. We must retain those distinctions while deriving the mathematics. [S1, pp. 1–4]

原始材料中的一个核心区分是：这些阶段的确立程度并不相同。光学源已经过能量归一化；激活规律尚未标定；气泡轨迹是人为规定的；界面释放仍未解决。在进行数学推导时，必须始终保留这些区分。[S1，第1–4页]

# 1. Optical deposition / 光能沉积

*Where does the laser energy go? Corresponding to Theory 01, source page 1.*

*激光能量去了哪里？对应 Theory 01，原始材料第1页。*

The first task is not yet to predict cavitation. It is to construct a heating field whose integral equals the intended absorbed energy.

第一项任务还不是预测空化，而是构造一个热源场，使其积分等于设定的吸收能量。

## 1.1 From beam fluence to total pulse energy / 从光束能量面密度到脉冲总能量

**Fluence** is the laser energy delivered per unit area during one pulse:

**能量面密度（fluence）**是单个脉冲期间单位面积接收到的激光能量：

$$[F]=\mathrm{J\,m^{-2}}.$$

It is different from intensity, which is power per unit area:

它不同于光强，后者是单位面积上的功率：

$$[I]=\mathrm{W\,m^{-2}}.$$

The source assumes an axisymmetric Gaussian fluence profile,

原始材料假设能量面密度具有轴对称高斯分布：

$$F(r)=F_0\exp\left(-\frac{2r^2}{w_0^2}\right),$$

where $F_0$ is the on-axis fluence and $w_0$ is the radius at which the fluence has fallen to $F_0e^{-2}$. The total pulse energy is the area integral. An annular element has area $dA=2\pi r\,dr$, so

其中，$F_0$ 是轴线上能量面密度，$w_0$ 是能量面密度下降至 $F_0e^{-2}$ 时的半径。脉冲总能量由面积积分得到。环形微元的面积为 $dA=2\pi r\,dr$，因此

$$E_p=2\pi F_0\int_0^\infty r\exp\left(-\frac{2r^2}{w_0^2}\right)\,dr.$$

Set

令

$$u=\frac{2r^2}{w_0^2},\qquad r\,dr=\frac{w_0^2}{4}\,du.$$

Then

于是

$$E_p=\frac{\pi w_0^2F_0}{2}\int_0^\infty e^{-u}\,du,$$

which gives

得到

$$\boxed{E_p=\frac{\pi w_0^2F_0}{2}}.$$

This explains the factor $1/2$: the beam is Gaussian, not a uniformly illuminated disk. This is the spatial normalization used in the source. [S1, p. 1]

这就解释了系数 $1/2$ 的来源：光束是高斯分布，而不是均匀照明的圆盘。这正是原始材料采用的空间归一化关系。[S1，第1页]

For the reference inputs,

代入参考输入：

$$w_0=25\times10^{-6}\ \mathrm m,\qquad F_0=0.10\ \mathrm{J\,cm^{-2}}=1000\ \mathrm{J\,m^{-2}},$$

we obtain

可得

$$E_p=\frac{\pi(25\times10^{-6})^2(1000)}{2}=9.8175\times10^{-7}\ \mathrm J.$$

Thus,

因此

$$\boxed{E_p=0.98175\ \mu\mathrm J}.$$

With the assumed absorbed fraction $\eta_{\mathrm{abs}}=0.30$,

采用假设的吸收比例 $\eta_{\mathrm{abs}}=0.30$，得到

$$\boxed{E_{\mathrm{abs}}=\eta_{\mathrm{abs}}E_p=0.29452\ \mu\mathrm J}.$$

These reproduce the reference energy values in the document. They are scenario calculations, not a measured cavitation threshold. [S1, p. 5]

这些结果复现了原始材料中的参考能量值。它们属于情景计算结果，并非实测空化阈值。[S1，第5页]

## 1.2 From pulse energy to a time-dependent source / 从脉冲能量到时变热源

We now distribute that energy over time. Write

现在将这部分能量沿时间分配，写成

$$I(r,t)=F(r)g(t),$$

and require

并要求

$$\int_{-\infty}^{\infty}g(t)\,dt=1.$$

This ensures that integrating intensity over the pulse recovers fluence:

这样就保证了对整个脉冲的光强进行时间积分，可以恢复能量面密度：

$$\int_{-\infty}^{\infty}I(r,t)\,dt=F(r).$$

For a Gaussian pulse with full width at half maximum $\tau_L$, the normalized function shown in the slide is

对于半高全宽为 $\tau_L$ 的高斯脉冲，原始页面给出的归一化函数为

$$\boxed{g(t)=\frac{1}{\tau_L}\sqrt{\frac{4\ln2}{\pi}}\exp\left[-4\ln2\left(\frac{t-t_c}{\tau_L}\right)^2\right]}.$$

Why this expression? At $t=t_c\pm\tau_L/2$, the exponential becomes $e^{-\ln2}=1/2$, establishing the specified full width. The prefactor follows from the Gaussian integral and makes the total integral unity.

为什么是这个表达式？在 $t=t_c\pm\tau_L/2$ 时，指数项变为 $e^{-\ln2}=1/2$，因此满足指定的半高全宽。前面的系数由高斯积分得到，使总积分等于1。

Notice that

注意

$$[g]=\mathrm{s^{-1}}.$$

Therefore $Fg$ has units of intensity rather than energy density.

因此，$Fg$ 的单位是光强的单位，而不是能量密度的单位。

## 1.3 From surface intensity to volumetric heating / 从表面光强到体积热源

Let $z$ measure depth into the absorbing material. The Beer–Lambert assumption is

以 $z$ 表示进入吸收材料内部的深度。Beer–Lambert 假设为

$$\frac{\partial I}{\partial z}=-\mu_a I,$$

where $\mu_a$ is an absorption coefficient with units $\mathrm{m^{-1}}$. Solving gives

其中，$\mu_a$ 是吸收系数，单位为 $\mathrm{m^{-1}}$。求解可得

$$I(z)=I(0)e^{-\mu_a z}.$$

The optical power removed from the beam per unit volume is

单位体积内从光束中吸收的光功率为

$$-\frac{\partial I}{\partial z}=\mu_a I(0)e^{-\mu_a z}.$$

Combining spatial, temporal, and depth dependence produces the source’s heating field:

将空间分布、时间分布和深度衰减结合起来，得到原始材料采用的热源场：

$$\boxed{Q'''(r,z,t)=\eta_{\mathrm{abs}}F(r)g(t)\mu_a e^{-\mu_a z}},\qquad \mu_a=\frac{1}{\delta_{\mathrm{abs}}}.$$

Here $Q'''$ is volumetric heating power:

这里的 $Q'''$ 是单位体积发热功率：

$$[Q''']=\underbrace{\mathrm{J\,m^{-2}}}_{F}\underbrace{\mathrm{s^{-1}}}_{g}\underbrace{\mathrm{m^{-1}}}_{\mu_a}=\mathrm{W\,m^{-3}}.$$

For the infinite lateral plane and semi-infinite depth used in this normalization,

在该归一化所采用的横向无限平面与半无限深度范围内，

$$
\begin{aligned}
\int_{-\infty}^{\infty}\int_V Q'''\,dV\,dt
&=\eta_{\mathrm{abs}}\left(\int_A F\,dA\right)\left(\int g\,dt\right)\\
&\quad\times\left(\int_0^\infty\mu_a e^{-\mu_a z}\,dz\right)\\
&=\eta_{\mathrm{abs}}E_p.
\end{aligned}
$$

Every factor has a clear purpose: the spatial integral supplies pulse energy; the time and depth integrals equal one. This is the energy closure emphasized on source page 1. [S1, p. 1]

每个因子都有明确作用：空间积分给出脉冲能量，时间积分与深度积分均等于1。这就是原始材料第1页强调的能量闭合。[S1，第1页]

**A finite simulation domain needs its own accounting.** For example, a layer of thickness $h$ contains only the depth fraction

**有限仿真域需要单独进行能量核算。** 例如，厚度为 $h$ 的材料层仅包含如下深度积分比例：

$$1-e^{-\mu_a h}.$$

Consequently, the source above integrates to $\eta_{\mathrm{abs}}E_p(1-e^{-\mu_a h})$ over that layer. Whether this is the correct target, or whether the depth profile should be renormalized, depends on whether $\eta_{\mathrm{abs}}$ denotes absorption over the entire deposition profile or absorption specifically in the finite layer. That interpretation must be fixed before implementing the source.

因此，在这一材料层内，上述热源的积分为 $\eta_{\mathrm{abs}}E_p(1-e^{-\mu_a h})$。这是否就是正确的目标值，或者是否需要重新归一化深度分布，取决于 $\eta_{\mathrm{abs}}$ 表示整个沉积分布范围内的吸收比例，还是专指该有限厚度层内的吸收比例。在实现热源之前，必须明确这一含义。

The source’s numerical check is

原始材料给出的数值检查条件为

$$\boxed{\epsilon_E=\frac{\left|\displaystyle\int\!\!\int_V Q'''\,dV\,dt-E_{\mathrm{abs,target}}\right|}{E_{\mathrm{abs,target}}}<0.01}.$$

Passing this check establishes correct energy bookkeeping—not correct cavitation physics.

通过这项检查说明能量核算正确，并不意味着空化物理模型已经正确。

## 1.4 Local dose, peak rate, and temperature rise / 局部剂量、峰值速率与温升

The local absorbed energy per unit volume is

局部单位体积吸收能量为

$$D_{\mathrm{abs}}(\mathbf x)=\int Q'''(\mathbf x,t)\,dt.$$

Using the normalized pulse,

利用归一化脉冲可得

$$\boxed{D_{\mathrm{abs}}(r,z)=\eta_{\mathrm{abs}}F(r)\mu_a e^{-\mu_a z}},\qquad [D_{\mathrm{abs}}]=\mathrm{J\,m^{-3}}.$$

The peak deposition rate is

峰值沉积速率为

$$\boxed{\dot q'''_{\max}(\mathbf x)=D_{\mathrm{abs}}(\mathbf x)\frac{1}{\tau_L}\sqrt{\frac{4\ln2}{\pi}}}.$$

Thus, for this pulse family, equal dose delivered in a shorter pulse means a larger peak heating rate. These are the two local predictors carried into source page 2. [S1, p. 2]

因此，对于这一类脉冲，在更短的时间内沉积相同剂量，就意味着更高的峰值加热速率。这两个量正是原始材料第2页采用的局部预测量。[S1，第2页]

To interpret the temperature-rise estimate on source page 5, add the following simple local energy balance. Assume constant properties, negligible heat loss during deposition, and no phase change:

为了理解原始材料第5页的温升估计，可引入下述简单的局部能量平衡。假设材料参数不变、沉积过程中热损失可忽略，且不发生相变：

$$\rho_{\mathrm{abs}}c_p\frac{\partial T}{\partial t}=Q'''.$$

Integrating over the pulse gives

对整个脉冲积分得到

$$\boxed{\Delta T_{\mathrm{ad}}=\frac{D_{\mathrm{abs}}}{\rho_{\mathrm{abs}}c_p}}.$$

At the beam centre and deposition surface,

在光束中心的能量沉积表面处，

$$\boxed{\Delta T_{\mathrm{ad},0}=\frac{\eta_{\mathrm{abs}}F_0}{\rho_{\mathrm{abs}}c_p\delta_{\mathrm{abs}}}}.$$

The density and heat capacity must belong to the material receiving the heat. They need not be those of the surrounding liquid.

这里的密度和比热容必须对应实际接收热量的材料，不一定是周围液体的参数。

The source reports a reference adiabatic rise of $7.19\ \mathrm K$, but the five pages do not provide all thermal properties and deposition-depth values needed to independently reproduce it. More importantly, this adiabatic calculation does not include latent heat or determine whether a droplet activates. [S1, p. 5]

原始材料给出的参考绝热温升为 $7.19\ \mathrm K$，但这五页并未提供独立复现该结果所需的全部热物性与沉积深度数值。更重要的是，这项绝热计算不包含潜热，也不能判断液滴是否会被激活。[S1，第5页]

## 1.5 Why enough energy does not guarantee a bubble / 为什么能量足够并不保证气泡形成

The pressure–volume work plot asks a narrower question: suppose a fraction $\eta_B$ of absorbed energy were available for bubble expansion. What radius could that energy support against a constant pressure difference?

压强–体积功曲线回答的是一个更有限的问题：假设吸收能量中有比例 $\eta_B$ 可用于气泡膨胀，那么在克服恒定压差的条件下，这部分能量最多能够支持多大的气泡半径？

With a resisting pressure $\Delta p>0$,

对于阻碍膨胀的压差 $\Delta p>0$，

$$W_{PV}=\int_{V_0}^{V_{\max}}\Delta p\,dV=\frac{4\pi}{3}\Delta p\left(R_{\max}^3-R_0^3\right).$$

Equating this to the available energy gives the screening radius

令其等于可用能量，得到筛查半径

$$\boxed{R_{\mathrm{ceiling}}=\left[R_0^3+\frac{3\eta_BE_{\mathrm{abs}}}{4\pi\Delta p}\right]^{1/3}}.$$

Neglecting $R_0$,

忽略 $R_0$ 后，

$$R_{\mathrm{ceiling}}\sim\left(\frac{\eta_BE_{\mathrm{abs}}}{\Delta p}\right)^{1/3}.$$

This is not a complete bubble-energy balance. In particular, the plot explicitly excludes latent heat and contains no nucleation barrier or activation kinetics. It therefore cannot establish either activation or the actual $R_{\max}$. [S1, p. 1]

这并不是完整的气泡能量平衡。尤其需要注意的是，该图明确排除了潜热，也没有包含成核势垒或激活动力学。因此，它既不能确定是否发生激活，也不能确定实际的 $R_{\max}$。[S1，第1页]

**The output of Stage 1 is a heating field and an energy budget—not yet a bubble.**

**阶段1的输出是一个热源场和一份能量预算，还不是一个气泡。**

# 2. Activation / 激活

*From local heating to the probability of an event. Corresponding to Theory 02, source page 2.*

*从局部加热到事件发生概率。对应 Theory 02，原始材料第2页。*

The source does not supply a thermodynamic nucleation-barrier model. Instead, it introduces an empirical, conditioned probability model. Its functional form can be explained mathematically, but its coefficients cannot be derived from energy conservation.

原始材料没有提供热力学成核势垒模型，而是引入了一个经验性的条件概率模型。可以从数学上解释其函数形式，但无法由能量守恒推导出其系数。

## 2.1 Why use a logistic model? / 为什么使用逻辑概率模型？

Let $p_1$ be the probability of an event associated with one available droplet. A probability must satisfy

以 $p_1$ 表示一个可参与激活的液滴发生事件的概率。概率必须满足

$$0\le p_1\le1.$$

A linear expression in dose and other variables does not automatically respect those bounds. The logistic construction instead makes the **logarithm of the odds** linear:

直接将剂量和其他变量线性相加，并不能自动满足这些取值范围。逻辑模型转而将**优势比的对数**设为线性形式：

$$\operatorname{logit}(p_1)=\ln\left(\frac{p_1}{1-p_1}\right)=\ell.$$

Solving,

求解得到

$$\frac{p_1}{1-p_1}=e^\ell\quad\Longrightarrow\quad\boxed{p_1=\frac{1}{1+e^{-\ell}}}.$$

The source writes the predictor in the form

原始材料将预测量写成如下形式：

$$
\begin{aligned}
\ell={}&\beta_0+b_{\mathrm{batch}}
+\beta_D\ln\frac{D_{\mathrm{abs}}}{D_{\mathrm{ref}}}
+\beta_Q\ln\frac{\dot q'''_{\max}}{\dot q'''_{\mathrm{ref}}}\\
&+\beta_\tau\ln\frac{\tau_L}{\tau_{\mathrm{ref}}}
+f_a(a_d)
+\mathbf z_{\mathrm{form}}^T\boldsymbol\beta_{\mathrm{form}}\\
&+\mathbf z_{\mathrm{det}}^T\boldsymbol\beta_{\mathrm{det}}
+\mathbf z_{\mathrm{hist}}^T\boldsymbol\beta_{\mathrm{hist}}.
\end{aligned}
$$

Here $a_d$ denotes droplet size. The remaining terms account for formulation, batch, detector state, and pulse history. The reference quantities make logarithm arguments dimensionless. **None of these coefficients is calibrated in the supplied theory pages.** [S1, p. 2]

这里的 $a_d$ 表示液滴尺寸。其余各项用于考虑配方、批次、探测器状态和脉冲历史。参考量的作用是使对数中的自变量无量纲化。**所提供的理论页面中，这些系数均尚未标定。** [S1，第2页]

There is a useful algebraic subtlety. For the exact Gaussian pulse model above,

这里有一个值得注意的代数细节。对于前面给出的精确高斯脉冲模型，

$$\ln\dot q'''_{\max}=\ln D_{\mathrm{abs}}-\ln\tau_L+\text{constant}.$$

Therefore dose, peak rate, and pulse width are not three independent predictors within that restricted pulse family. Their separate coefficients require an identifiable parameterization or additional experimental structure. This follows directly from the source equations; it is not a calibrated result.

因此，在这一受限的脉冲族中，剂量、峰值速率和脉宽并不是三个相互独立的预测量。要分别识别它们的系数，需要采用具有可辨识性的参数化方式，或提供额外的实验设计信息。这是由热源方程直接得到的结论，并非标定结果。

Also, because the slide includes detector-state covariates inside the logit, the fitted model should not automatically be interpreted as an intrinsic, detector-independent material law.

此外，由于原始页面将探测器状态协变量直接放入 logit 表达式中，因此不能自动将拟合得到的模型解释为独立于探测器的材料内禀规律。

## 2.2 From one droplet to many droplets / 从单个液滴到液滴群体

Suppose there are $N_{\mathrm{active}}$ available droplets, with independent events and equal probability $p_1$.

假设有 $N_{\mathrm{active}}$ 个可参与激活的液滴，各液滴的事件彼此独立，且事件概率均为 $p_1$。

For one droplet,

对于一个液滴，

$$P(\text{no event})=1-p_1.$$

Independence gives

由独立性可得

$$P(\text{no events among all droplets})=(1-p_1)^{N_{\mathrm{active}}}.$$

Taking the complement,

取其补事件，得到

$$\boxed{P_{\ge1}^{(N)}=1-(1-p_1)^{N_{\mathrm{active}}}}.$$

This is the population transform in the source. [S1, p. 2]

这就是原始材料中的群体概率变换。[S1，第2页]

For example, with $p_1=0.01$,

例如，当 $p_1=0.01$ 时，

$$P_{\ge1}^{(1)}=0.01,$$

but

而

$$P_{\ge1}^{(100)}=1-0.99^{100}\approx0.634.$$

The individual-droplet probability has not changed, yet the probability of observing at least one event has risen from $1\%$ to approximately $63\%$. Consequently, an apparent experimental onset can shift simply because the number of available droplets changes.

单个液滴的概率并没有改变，但观察到至少一次事件的概率却从 $1\%$ 上升到了约 $63\%$。因此，仅仅改变可参与激活的液滴数量，就可能使实验中的表观起始点发生变化。

The inverse relation follows immediately:

其反演关系可以直接得到：

$$1-P_{\ge1}^{(N)}=(1-p_1)^N,$$

so

因此

$$\boxed{p_1=1-\left(1-P_{\ge1}^{(N)}\right)^{1/N}}.$$

This inversion depends on the assumed known count and independent, equal-probability event model.

这一反演依赖于以下假设：液滴数量已知，各事件相互独立，且具有相同的发生概率。

## 2.3 Adding the detector / 加入探测器模型

Now let $q_d$ be the probability that a real single-droplet event is detected, and $f_d$ the false-event probability per observation.

现在，令 $q_d$ 表示真实单液滴事件被探测到的概率，$f_d$ 表示每次观测出现假事件的概率。

For one droplet,

对于一个液滴，

$$P(\text{detected real event})=q_dp_1.$$

The probability that none of the droplets produces a detected real event is

没有任何液滴产生被探测到的真实事件，其概率为

$$(1-q_dp_1)^N.$$

Under the source’s independent false-event model, observing no event also requires no false event:

在原始材料采用的独立假事件模型下，未记录到事件还要求没有假事件发生：

$$P(\text{no recorded event})=(1-f_d)(1-q_dp_1)^N.$$

Therefore,

因此

$$\boxed{P_{\mathrm{det}}=1-(1-f_d)(1-q_dp_1)^N},$$

or equivalently,

等价地，

$$\boxed{P_{\mathrm{det}}=f_d+(1-f_d)\left[1-(1-q_dp_1)^N\right]}.$$

This is why observed onset and underlying event probability are not interchangeable. [S1, p. 2]

这就是为什么观测到的起始点与底层事件概率不能混为一谈。[S1，第2页]

When $q_d>0$, $f_d<1$, and $N$ is known, inversion gives

当 $q_d>0$、$f_d<1$ 且 $N$ 已知时，反演得到

$$\boxed{p_1=\frac{1-\left(\dfrac{1-P_{\mathrm{det}}}{1-f_d}\right)^{1/N}}{q_d}}.$$

The physical bounds $0\le p_1\le1$ imply

由物理取值范围 $0\le p_1\le1$ 可得

$$f_d\le P_{\mathrm{det}}\le f_d+(1-f_d)\left[1-(1-q_d)^N\right].$$

A measured probability outside those bounds would be inconsistent with the chosen count and detector parameters.

如果测得的概率落在上述范围之外，就说明它与所采用的液滴数量及探测器参数不相容。

**The output of Stage 2 is a conditioned event probability—not a universal fluence threshold and not a bubble-radius history.** That is the explicit boundary of the second theory page. [S1, p. 2]

**阶段2的输出是一个条件事件概率，而不是通用的能量面密度阈值，也不是气泡半径历程。** 这正是第二个理论页面明确规定的结论边界。[S1，第2页]

# 3. Bubble dynamics / 气泡动力学

*From a moving radius to a pressure field. Corresponding to Theory 03, source page 3.*

*从变化的半径到压力场。对应 Theory 03，原始材料第3页。*

This is the central mechanics derivation.

这是整套理论中最核心的力学推导。

The spherical model assumes a bubble of radius $R(t)$, approximately uniform internal pressure $p_B(t)$, and an unbounded incompressible surrounding liquid. Let the liquid density and dynamic viscosity be $\rho_l$ and $\mu_l$, and its distant pressure be $p_\infty(t)$. We neglect the correction to interface kinematics caused by mass transfer.

球对称模型假设气泡半径为 $R(t)$，内部压力 $p_B(t)$ 近似均匀，周围为无界、不可压缩液体。液体密度和动力黏度分别记为 $\rho_l$ 和 $\mu_l$，远处液体压力为 $p_\infty(t)$。这里忽略质量传递对界面运动学条件造成的修正。

These are the classical assumptions behind the radial flow and Rayleigh–Plesset framework; they are not assumptions of a fully resolved near-wall bubble. [R1]

这些是径向流动与 Rayleigh–Plesset 框架背后的经典假设，并不等同于对近壁气泡进行完全解析时所采用的模型。[R1]

## 3.1 Continuity determines the liquid velocity / 连续性方程确定液体速度

For a purely radial, incompressible flow,

对于纯径向不可压缩流动，

$$\nabla\cdot\mathbf u=\frac{1}{r^2}\frac{\partial}{\partial r}(r^2u)=0.$$

Thus,

因此

$$r^2u=C(t).$$

At the bubble wall, the liquid follows the interface:

在气泡壁面处，液体跟随界面运动：

$$u(R,t)=\dot R.$$

Therefore,

于是

$$C(t)=R^2\dot R,$$

and

从而

$$\boxed{u(r,t)=\frac{R^2\dot R}{r^2}}.$$

The interpretation is simple: the same instantaneous volume flux passes through every concentric spherical surface,

其物理含义很简单：通过每一个同心球面的瞬时体积流量都相同，即

$$4\pi r^2u=4\pi R^2\dot R.$$

The entire radial velocity field is therefore determined by one coordinate, $R(t)$.

因此，整个径向速度场由单个坐标 $R(t)$ 决定。

## 3.2 The velocity potential gives the pressure field / 由速度势求得压力场

Introduce a velocity potential $\Phi$ such that

引入速度势 $\Phi$，使其满足

$$u=\frac{\partial\Phi}{\partial r}.$$

Choosing $\Phi\to0$ at infinity,

取无穷远处 $\Phi\to0$，则

$$\boxed{\Phi(r,t)=-\frac{R^2\dot R}{r}}.$$

The unsteady Bernoulli relation is

非定常 Bernoulli 关系为

$$\frac{\partial\Phi}{\partial t}+\frac12u^2+\frac{p-p_\infty}{\rho_l}=0.$$

The time derivative is taken at a **fixed spatial location $r$**:

时间偏导数是在**固定空间位置 $r$** 处计算的：

$$\frac{\partial\Phi}{\partial t}=-\frac{R^2\ddot R+2R\dot R^2}{r}.$$

Also,

同时，

$$\frac12u^2=\frac{R^4\dot R^2}{2r^4}.$$

Consequently,

因此

$$\boxed{p'(r,t)\equiv p(r,t)-p_\infty(t)=\rho_l\left[\frac{R^2\ddot R+2R\dot R^2}{r}-\frac{R^4\dot R^2}{2r^4}\right]}.$$

This reconstructs the pressure-mapping equation shown on source page 3. [S1, p. 3]

这就重构了原始材料第3页所示的压力映射方程。[S1，第3页]

Define

定义

$$A(t)=R^2\ddot R+2R\dot R^2,\qquad B(t)=R^4\dot R^2.$$

Then

则

$$p'=\rho_l\left(\frac{A}{r}-\frac{B}{2r^4}\right).$$

The leading term has an especially useful interpretation. Since

主导项具有一个特别有用的物理解释。由于

$$V=\frac{4\pi}{3}R^3,$$

we have

可得

$$\ddot V=4\pi\left(R^2\ddot R+2R\dot R^2\right)=4\pi A.$$

Thus,

因此

$$\frac{\rho_lA}{r}=\frac{\rho_l}{4\pi r}\ddot V.$$

**Pressure is closely connected to bubble-volume acceleration, not merely to bubble size or whether the bubble is growing.**

**压力与气泡体积的二阶时间导数密切相关，而不仅仅取决于气泡尺寸，或气泡是否正在增长。**

That is why an expanding bubble can produce a negative pressure perturbation while its expansion decelerates.

因此，一个正在膨胀的气泡，在膨胀过程减速时，也可能产生负的压力扰动。

## 3.3 Applying the wall condition gives Rayleigh–Plesset / 由壁面条件得到 Rayleigh–Plesset 方程

Evaluate the pressure relation at $r=R$:

在 $r=R$ 处计算上述压力关系：

$$p_l(R,t)-p_\infty=\rho_l\left[R\ddot R+2\dot R^2-\frac12\dot R^2\right].$$

Therefore,

因此

$$\boxed{p_l(R,t)-p_\infty=\rho_l\left(R\ddot R+\frac32\dot R^2\right)}.$$

Here $p_l(R,t)$ is the liquid pressure immediately outside the interface. It differs from the bubble pressure because of surface tension and viscous normal stress.

这里的 $p_l(R,t)$ 是紧邻界面外侧的液体压力。由于表面张力和黏性法向应力的存在，它与气泡内部压力并不相同。

Let $\sigma$ denote surface tension. The normal-stress condition is

以 $\sigma$ 表示表面张力。法向应力条件为

$$p_B-p_l(R)=\frac{2\sigma}{R}+\frac{4\mu_l\dot R}{R}.$$

The $2\sigma/R$ term follows from the force balance on a hemispherical interface. The viscous term follows from

其中，$2\sigma/R$ 项由半球形界面的受力平衡得到。黏性项来自

$$\left.\frac{\partial u}{\partial r}\right|_{r=R}=-\frac{2\dot R}{R}$$

and the Newtonian normal stress $2\mu_l\partial u/\partial r$.

以及牛顿流体的黏性法向应力 $2\mu_l\partial u/\partial r$。

Substituting yields

代入可得

$$\boxed{\rho_l\left(R\ddot R+\frac32\dot R^2\right)=p_B-p_\infty-\frac{2\sigma}{R}-\frac{4\mu_l\dot R}{R}}.$$

This is the Rayleigh–Plesset equation printed in the source. [S1, p. 3]

这就是原始材料给出的 Rayleigh–Plesset 方程。[S1，第3页]

Its structure should look familiar:

它的结构应当十分熟悉：

$$
\underbrace{\rho_l(R\ddot R+\tfrac32\dot R^2)}_{\text{liquid inertia / 液体惯性}}
=
\underbrace{p_B-p_\infty}_{\text{pressure driving / 压力驱动}}
-
\underbrace{2\sigma/R}_{\text{surface tension / 表面张力}}
-
\underbrace{4\mu_l\dot R/R}_{\text{viscous resistance / 黏性阻力}}.
$$

One subtlety is that viscosity can appear in the wall stress even though we used the potential-flow pressure relation: for this incompressible spherical velocity field, the bulk viscous-force term vanishes, while the interfacial viscous stress does not.

一个细节是：虽然采用了势流压力关系，黏性仍然可以出现在壁面应力中。对于这一不可压缩球对称速度场，液体内部的黏性力项为零，但界面处的黏性应力并不为零。

### Why this equation does not yet predict laser-induced growth / 为什么该方程还不能预测激光诱导增长

Rayleigh–Plesset determines $R(t)$ only after the internal pressure is specified consistently.

只有在以自洽方式给定内部压力之后，Rayleigh–Plesset 方程才能确定 $R(t)$。

For a laser-heated, vaporizing droplet, that requires additional thermal and phase-change information. The source does not supply a closed internal-pressure, heat-transfer, and mass-transfer model. Instead, it uses Rayleigh–Plesset **inversely**:

对于受到激光加热并发生汽化的液滴，这需要额外的热学和相变信息。原始材料没有提供闭合的内部压力、传热与传质模型，而是**反向使用** Rayleigh–Plesset 方程：

$$\boxed{p_{B,\mathrm{required}}(t)=p_\infty+\rho_l\left(R\ddot R+\frac32\dot R^2\right)+\frac{2\sigma}{R}+\frac{4\mu_l\dot R}{R}}.$$

Given a prescribed $R(t)$, this asks what internal pressure would be required to support that trajectory. It is a consistency check, not a forward prediction of activation and growth. [S1, p. 3]

在给定人为规定的 $R(t)$ 后，这个式子回答的是：维持该轨迹需要怎样的内部压力？它属于一致性检查，而不是对激活与增长的正向预测。[S1，第3页]

## 3.4 Deriving the Rayleigh collapse time / 推导 Rayleigh 塌缩时间

The collapse-time estimate comes from a simpler limiting problem.

塌缩时间估计来自一个更简单的极限问题。

Assume constant bubble pressure $p_v$, constant external pressure $p_\infty>p_v$, negligible surface tension and viscosity, and an initially stationary bubble of radius $R_{\max}$. Define

假设气泡内部压力恒为 $p_v$，外界压力恒为 $p_\infty>p_v$，表面张力与黏性可忽略，且气泡初始静止、半径为 $R_{\max}$。定义

$$\Delta p=p_\infty-p_v>0.$$

Then

则

$$R\ddot R+\frac32\dot R^2=-\frac{\Delta p}{\rho_l}.$$

Set $v(R)=\dot R^2$. Along the trajectory,

令 $v(R)=\dot R^2$。沿着运动轨迹有

$$\ddot R=\frac12\frac{dv}{dR},$$

so

因此

$$R\frac{dv}{dR}+3v=-\frac{2\Delta p}{\rho_l}.$$

Multiplication by $R^2$ gives

两边乘以 $R^2$，得到

$$\frac{d}{dR}(R^3v)=-\frac{2\Delta p}{\rho_l}R^2.$$

Using $v(R_{\max})=0$,

利用 $v(R_{\max})=0$，得到

$$\boxed{\dot R^2=\frac{2\Delta p}{3\rho_l}\left[\left(\frac{R_{\max}}{R}\right)^3-1\right]}.$$

During collapse, take the negative square root. The time to reach zero radius is

在塌缩阶段，应取负平方根。到达零半径所需的时间为

$$t_R=\int_0^{R_{\max}}\frac{dR}{\sqrt{\dfrac{2\Delta p}{3\rho_l}\left[\left(\dfrac{R_{\max}}{R}\right)^3-1\right]}}.$$

With $x=R/R_{\max}$,

令 $x=R/R_{\max}$，则

$$t_R=R_{\max}\sqrt{\frac{3\rho_l}{2\Delta p}}\int_0^1\frac{x^{3/2}}{\sqrt{1-x^3}}\,dx.$$

Evaluation of the dimensionless integral gives

计算该无量纲积分可得

$$\boxed{t_R\approx0.915R_{\max}\sqrt{\frac{\rho_l}{\Delta p}}}.$$

This is the origin of the coefficient $0.915$, rather than an empirical fitting factor.

这就是系数 $0.915$ 的来源；它不是经验拟合系数。

The source reports $t_R=0.735\ \mu\mathrm s$ for its reference case and uses it only as a timescale check. Its prescribed trajectory does not actually collapse to zero radius. [S1, p. 3]

原始材料给出的参考情景结果为 $t_R=0.735\ \mu\mathrm s$，并仅将其用于时间尺度检查。材料中人为规定的轨迹实际上并不会塌缩到零半径。[S1，第3页]

## 3.5 Deriving the prescribed smooth trajectory / 推导规定的平滑轨迹

The source constructs a smooth radius history instead of solving a forward cavitation problem.

原始材料构造了一条平滑的半径历程，而没有求解正向空化问题。

We want a function $S(\xi)$, $0\le\xi\le1$, satisfying

需要构造函数 $S(\xi)$，其中 $0\le\xi\le1$，并满足

$$S(0)=0,\qquad S(1)=1,$$

and

以及

$$S'(0)=S'(1)=0,\qquad S''(0)=S''(1)=0.$$

These six conditions determine a fifth-degree polynomial:

这六个条件确定了一个五次多项式：

$$\boxed{S(\xi)=10\xi^3-15\xi^4+6\xi^5}.$$

Its derivatives are

其导数为

$$S'(\xi)=30\xi^2(1-\xi)^2,$$

$$S''(\xi)=60\xi(1-\xi)(1-2\xi).$$

Let $\Delta R=R_{\max}-R_0$, with growth time $t_g$ and shrinkage time $t_c$. Then

令 $\Delta R=R_{\max}-R_0$，增长时间为 $t_g$，收缩时间为 $t_c$。则

$$\boxed{R(t)=\begin{cases}R_0+\Delta R\,S(t/t_g),&0\le t\le t_g,\\[4pt]R_{\max}-\Delta R\,S((t-t_g)/t_c),&t_g<t\le t_g+t_c.\end{cases}}$$

The zero endpoint derivatives prevent artificial velocity and acceleration jumps. This is the stated purpose of the prescribed trajectory. [S1, p. 3]

端点处一阶与二阶导数为零，可避免速度和加速度出现人为跳变。这正是原始材料构造该规定轨迹的目的。[S1，第3页]

Because $S'$ has its maximum at $\xi=1/2$,

由于 $S'$ 在 $\xi=1/2$ 处达到最大值，

$$S'_{\max}=\frac{30}{16}=1.875.$$

Therefore,

因此

$$\dot R_{\max,\mathrm{growth}}=1.875\frac{\Delta R}{t_g},\qquad |\dot R|_{\max,\mathrm{collapse}}=1.875\frac{\Delta R}{t_c}.$$

Using the supplied values

代入所提供的数值

$$R_0=1\ \mu\mathrm m,\quad R_{\max}=8\ \mu\mathrm m,\quad t_g=0.7\ \mu\mathrm s,\quad t_c=0.6\ \mu\mathrm s,$$

gives

得到

$$\dot R_{\max,\mathrm{growth}}=18.75\ \mathrm{m\,s^{-1}},$$

$$\boxed{|\dot R|_{\max,\mathrm{collapse}}=21.875\ \mathrm{m\,s^{-1}}}.$$

This exactly reproduces the reported maximum wall speed. It follows from the chosen polynomial and timings—not independently predicted cavitation dynamics. [S1, p. 5]

这精确复现了原始材料报告的最大壁面速度。该数值来自选定的多项式与时间参数，而不是独立预测得到的空化动力学结果。[S1，第5页]

## 3.6 Mapping bubble pressure onto a load disk / 将气泡压力映射至载荷圆盘

Let the bubble centre be a distance $d$ from a plane. Use $s$ for radial distance along that plane. Then the distance from the bubble centre to a point on the plane is

设气泡中心距某平面的距离为 $d$，以 $s$ 表示该平面上的径向距离。则气泡中心到平面上某点的距离为

$$r=\sqrt{d^2+s^2}.$$

Substitution into the spherical pressure field gives

代入球对称压力场，得到

$$p'(s,t)=\rho_l\left[\frac{A(t)}{\sqrt{d^2+s^2}}-\frac{B(t)}{2(d^2+s^2)^2}\right].$$

The average over a disk of radius $L$ is

在半径为 $L$ 的圆盘上的平均压力为

$$\bar p(t)=\frac{1}{\pi L^2}\int_0^L p'(s,t)\,2\pi s\,ds.$$

The required integrals are

所需积分为

$$\int_0^L\frac{s}{\sqrt{d^2+s^2}}\,ds=\sqrt{d^2+L^2}-d,$$

and

以及

$$\int_0^L\frac{s}{(d^2+s^2)^2}\,ds=\frac12\left(\frac1{d^2}-\frac1{d^2+L^2}\right).$$

Hence,

因此

$$\boxed{\begin{aligned}\bar p(t)=\rho_l\bigg[&\frac{2A(t)}{L^2}\left(\sqrt{d^2+L^2}-d\right)\\&-\frac{B(t)}{2L^2}\left(\frac1{d^2}-\frac1{d^2+L^2}\right)\bigg].\end{aligned}}$$

This reconstructs the load-disk average on source page 3. [S1, p. 3]

这就重构了原始材料第3页给出的载荷圆盘平均压力。[S1，第3页]

As a check, letting $L\to0$ recovers the axis value,

作为检查，令 $L\to0$，可以恢复轴线上的压力值：

$$\bar p\to\rho_l\left(\frac{A}{d}-\frac{B}{2d^4}\right).$$

## 3.7 What the signed pressure does—and does not—mean / 带符号压力的含义与局限

The signs follow from the acceleration terms, not simply from the sign of $\dot R$. Growth acceleration, growth deceleration, collapse acceleration, and collapse deceleration can generate different pressure branches.

压力的正负号来自加速度相关项，而不只是由 $\dot R$ 的符号决定。增长加速、增长减速、塌缩加速与塌缩减速可能产生不同的压力分支。

The model consequently produces a time-dependent signed load. Replacing it by a constant positive pressure would change the structural problem. The source specifically emphasizes the relative timing of these branches. [S1, p. 3]

因此，该模型产生的是一个随时间变化、具有正负号的载荷。如果用恒定正压替代它，就会改变结构问题本身。原始材料特别强调这些分支之间的相对时序。[S1，第3页]

However, there are two important limits.

不过，这里存在两项重要限制。

First, the reported stand-off ratio is

第一，原始材料报告的距壁比为

$$\gamma=\frac{d}{R_{\max}}=1.0625.$$

With $R_{\max}=8\ \mu\mathrm m$, this implies $d=8.5\ \mu\mathrm m$. The bubble is close to the boundary, whereas the pressure expression was derived for an unbounded spherical flow. Evaluating it on a plane does not enforce a real wall boundary condition. The source therefore does not claim validated near-wall pressure, jetting, or shock prediction. [S1, p. 3]

当 $R_{\max}=8\ \mu\mathrm m$ 时，可得 $d=8.5\ \mu\mathrm m$。此时气泡非常接近边界，但压力表达式是在无界球对称流动下推导的。仅仅在一个平面上计算该表达式，并不能满足真实壁面的边界条件。因此，原始材料并未声称已经预测出经验证的近壁压力、射流或冲击波。[S1，第3页]

Second,

第二，

$$p_{\mathrm{absolute}}=p_\infty+p'.$$

The source explicitly flags its negative source branch as failing the reference absolute-pressure check. That branch cannot simply be treated as a validated physical load and passed downstream. [S1, p. 5]

原始材料明确指出，其负压源分支未通过参考情景的绝对压力检查。因此，不能直接将该分支视为经验证的物理载荷，并传递给下游模型。[S1，第5页]

This is a limitation of this calculation, not a universal statement that liquids cannot sustain tension: metastable liquids can sustain negative pressure under appropriate conditions. Such behaviour requires its own nucleation and metastability description, which is absent here. [R2]

这是当前计算本身的限制，并不是说液体普遍不能承受拉伸：在适当条件下，亚稳态液体能够承受负压。但描述这种行为需要相应的成核与亚稳态模型，而当前模型中没有这些内容。[R2]

# 4. Structural motion and interfacial release / 结构运动与界面释放

*From pressure to structural motion and interfacial release. Corresponding to Theory 04, source page 4.*

*从压力到结构运动，再到界面释放。对应 Theory 04，原始材料第4页。*

The fourth page contains two complementary mechanical reductions: a flexural mode describing laminate motion, and a first-arrival wave calculation describing through-thickness transmission. Neither, by itself, supplies a resolved cohesive-interface traction history. [S1, p. 4]

第4页包含两种互补的力学简化：用弯曲模态描述层合结构运动，以及用首波计算描述厚度方向的传输。这两种简化中的任何一种，都不能单独给出经过空间解析的黏聚界面牵引历程。[S1，第4页]

## 4.1 Reducing the laminate to one generalized coordinate / 将层合结构简化为一个广义坐标

Approximate the transverse displacement as

将横向位移近似为

$$w(s,t)=\phi(s)q(t),$$

where $\phi(s)$ is an assumed spatial shape and $q(t)$ its amplitude.

其中，$\phi(s)$ 是假定的空间振型，$q(t)$ 是其幅值。

The printed modal coefficients can be reconstructed using the clamped-disk shape

采用以下固支圆盘振型，可以重构原始材料中的模态系数：

$$\boxed{\phi(s)=\left(1-\frac{s^2}{a^2}\right)^2},\qquad 0\le s\le a.$$

It satisfies

它满足

$$\phi(a)=0,\qquad\phi'(a)=0,\qquad\phi(0)=1.$$

Thus the edge is clamped and $q(t)$ is the centre displacement. This is an admissible assumed shape, not a claim that the exact laminate eigenmode has been measured.

因此，边缘为固支条件，$q(t)$ 就是中心位移。这是一个满足边界条件的假定振型，并不意味着已经测得层合结构的精确固有模态。

### Modal mass / 模态质量

Let $m'$ be laminate mass per unit area. The kinetic energy is

以 $m'$ 表示层合结构的单位面积质量。动能为

$$T=\frac12\int_A m'\dot w^2\,dA=\frac12\dot q^2\int_A m'\phi^2\,dA.$$

Therefore,

因此

$$M_q=2\pi m'\int_0^a\phi^2s\,ds.$$

Since

由于

$$\int_0^a\left(1-\frac{s^2}{a^2}\right)^4s\,ds=\frac{a^2}{10},$$

we obtain

可得

$$\boxed{M_q=\frac{\pi m'a^2}{5}}.$$

### Modal stiffness / 模态刚度

For an equivalent isotropic thin-plate reduction with bending rigidity $D$,

对于弯曲刚度为 $D$ 的等效各向同性薄板简化模型，

$$U=\frac{D}{2}\int_A\left(\kappa_r^2+\kappa_\theta^2+2\nu\kappa_r\kappa_\theta\right)dA,$$

where

其中

$$\kappa_r=-q\phi'',\qquad\kappa_\theta=-q\frac{\phi'}s.$$

Matching $U=\tfrac12K_qq^2$ gives

与 $U=\tfrac12K_qq^2$ 对比，得到

$$K_q=2\pi D\int_0^a\left[(\phi'')^2+\left(\frac{\phi'}s\right)^2+2\nu\phi''\frac{\phi'}s\right]s\,ds.$$

For the selected shape,

对于选定的振型，

$$\int_0^a[\cdots]s\,ds=\frac{32}{3a^2},$$

so

所以

$$\boxed{K_q=\frac{64\pi D}{3a^2}}.$$

The actual laminate rigidity $D$ still requires its layer constitutive properties and appropriate laminate assumptions.

实际层合结构的刚度 $D$ 仍需根据各层本构参数与适当的层合理论假设确定。

### Generalized load / 广义载荷

Virtual work is

虚功为

$$\delta W=\int_A p(s,t)\,\delta w\,dA.$$

Since $\delta w=\phi\,\delta q$,

由于 $\delta w=\phi\,\delta q$，

$$\delta W=\left[\int_A p(s,t)\phi(s)\,dA\right]\delta q.$$

Hence,

因此

$$\boxed{Q(t)=2\pi\int_0^a p(s,t)\phi(s)s\,ds}.$$

Here $Q(t)$ is a generalized force, not the optical heating source $Q'''$.

这里的 $Q(t)$ 是广义力，不是光学体热源 $Q'''$。

Lagrange’s equation, with modal damping $C_q$, now gives

考虑模态阻尼 $C_q$，由 Lagrange 方程得到

$$\boxed{M_q\ddot q+C_q\dot q+K_qq=Q(t)}.$$

This is the reduced structural equation in the source. Its load is a spatial projection, not merely the pressure at the centre. [S1, p. 4]

这就是原始材料中的降阶结构方程。其载荷是压力场的空间投影，而不只是中心点的压力。[S1，第4页]

## 4.2 Why load timing matters / 为什么载荷时序很重要

Define

定义

$$\omega_n=\sqrt{\frac{K_q}{M_q}},\qquad\zeta=\frac{C_q}{2\sqrt{M_qK_q}},\qquad\omega_d=\omega_n\sqrt{1-\zeta^2}.$$

For zero initial conditions and an underdamped mode,

在零初始条件及欠阻尼模态下，

$$\boxed{q(t)=\frac{1}{M_q\omega_d}\int_0^t Q(\tau)e^{-\zeta\omega_n(t-\tau)}\sin\!\left[\omega_d(t-\tau)\right]\,d\tau}.$$

This follows by convolving the load with the oscillator’s impulse response.

这是将载荷与振子的脉冲响应进行卷积得到的结果。

The sine factor is the key. The same load increment can increase or decrease the current motion depending on when it arrives. Therefore, two histories with equal net impulse need not produce equal peak displacement. This mathematically explains the phase sensitivity discussed on source page 3. [S1, p. 3]

关键在于正弦因子。同样的载荷增量，根据到达时刻的不同，可能增强当前运动，也可能削弱当前运动。因此，净冲量相同的两条载荷历程，不一定产生相同的峰值位移。这从数学上解释了原始材料第3页讨论的相位敏感性。[S1，第3页]

## 4.3 Why equal total impulse can also fail spatially / 为什么总冲量相同仍可能产生不同的空间响应

Write a separable pressure distribution as

将可分离的压力分布写成

$$p(s,t)=F(t)b(s),\qquad\int_A b(s)\,dA=1.$$

Then $F(t)$ is total force, while

此时 $F(t)$ 为总力，而

$$Q(t)=F(t)\underbrace{\int_A b(s)\phi(s)\,dA}_{\Lambda}.$$

Two distributions can have the same total force history but different modal participation factors $\Lambda$.

两个分布可以具有相同的总力历程，却具有不同的模态参与因子 $\Lambda$。

For example, uniform loading over the entire disk has

例如，整个圆盘上的均匀载荷对应

$$b=\frac1{\pi a^2},$$

giving

因此

$$\Lambda=\frac1{\pi a^2}\int_A\phi\,dA=\frac13.$$

A strongly centre-concentrated load samples $\phi\approx1$, giving a participation factor approaching one.

高度集中于中心附近的载荷作用在 $\phi\approx1$ 的区域，因此其参与因子接近1。

This is an illustrative consequence of the assumed shape, not a numerical reconstruction of the source’s bars. It explains why the top-hat, Gaussian, and raised-cosine distributions in the source produce different centre displacements despite equal total impulse. [S1, p. 4]

这是采用该假定振型后得到的示意性结论，并不是对原始材料中柱状图的数值复现。它解释了为什么原始材料中的顶帽、高斯和升余弦分布，即使总冲量相同，也会产生不同的中心位移。[S1，第4页]

## 4.4 Deriving first-arrival wave transmission / 推导首波传输

For one-dimensional longitudinal motion in an isotropic elastic layer,

对于各向同性弹性层中的一维纵向运动，

$$\rho\frac{\partial^2u}{\partial t^2}=\frac{\partial\sigma_{zz}}{\partial z},\qquad\sigma_{zz}=M_L\frac{\partial u}{\partial z},$$

where the longitudinal modulus is

其中纵向模量为

$$M_L=\frac{E(1-\nu)}{(1+\nu)(1-2\nu)}.$$

Combining gives a wave equation with speed

将两式结合，得到波动方程，其波速为

$$\boxed{c_L=\sqrt{\frac{E(1-\nu)}{\rho(1+\nu)(1-2\nu)}}}.$$

The corresponding impedance is

相应的阻抗为

$$\boxed{Z=\rho c_L}.$$

For a normally incident wave at an ideal bonded interface, let $p_i,p_r,p_t$ denote incident, reflected, and transmitted compressive amplitudes. Continuity of traction and particle velocity gives

对于垂直入射到理想粘结界面的波，以 $p_i,p_r,p_t$ 分别表示入射、反射与透射的压缩波幅值。由牵引连续和质点速度连续条件可得

$$p_i+p_r=p_t,$$

$$\frac{p_i-p_r}{Z_1}=\frac{p_t}{Z_2}.$$

Solving,

求解得到

$$\boxed{R_p=\frac{p_r}{p_i}=\frac{Z_2-Z_1}{Z_2+Z_1}},$$

$$\boxed{T_p=\frac{p_t}{p_i}=\frac{2Z_2}{Z_1+Z_2}}.$$

Because energy flux scales as $p^2/Z$, the energy-transmission coefficient is

由于能流按 $p^2/Z$ 缩放，能量透射系数为

$$\boxed{T_I=T_p^2\frac{Z_1}{Z_2}=\frac{4Z_1Z_2}{(Z_1+Z_2)^2}}.$$

Thus $T_p>1$ does not imply that transmitted energy exceeds incident energy.

因此，$T_p>1$ 并不意味着透射能量超过入射能量。

For a stack,

对于多层堆叠结构，

$$\boxed{t_{\mathrm{transit}}=\sum_i\frac{h_i}{c_{L,i}}}.$$

The source reports a one-way value of $29.9\ \mathrm{ns}$, but its calculation retains only the forward first arrival. Later reflections, attenuation, shear transmission, and the resolved through-thickness field are not included. A short first-arrival time does not make those omitted effects irrelevant. [S1, p. 4]

原始材料报告的单程传播时间为 $29.9\ \mathrm{ns}$，但计算仅保留了首次正向到达的波。后续反射、衰减、剪切传输，以及完整解析的厚度方向场均未包含在内。首波到达时间很短，并不意味着这些被忽略的效应不重要。[S1，第4页]

## 4.5 From transmitted loading to cohesive failure / 从传递载荷到黏聚失效

Interfacial release requires a relation between traction and displacement discontinuity.

界面释放需要通过牵引与位移不连续之间的关系来描述。

The source introduces a cohesive form

原始材料引入了如下黏聚形式：

$$\boxed{\mathbf t=(1-D_c)\mathbf K\boldsymbol\delta},$$

where $\boldsymbol\delta$ contains opening and sliding separations, $\mathbf t$ contains the corresponding tractions, and $D_c$ is a damage variable.

其中，$\boldsymbol\delta$ 包含张开与滑移分离量，$\mathbf t$ 包含相应的牵引分量，$D_c$ 为损伤变量。

Its quadratic mixed-mode initiation condition is

其二次混合模态损伤起始条件为

$$\boxed{\left(\frac{\langle t_n\rangle}{T_{n0}}\right)^2+\left(\frac{t_s}{T_{s0}}\right)^2=1},$$

with $\langle t_n\rangle=\max(t_n,0)$ under a tension-positive convention.

在拉伸为正的符号约定下，$\langle t_n\rangle=\max(t_n,0)$。

This condition identifies the onset of damage in the adopted model. It does **not** by itself specify complete separation. That requires the subsequent traction–separation evolution and fracture energy, schematically

这一条件确定的是所采用模型中的损伤起始，**并不能**单独确定完全分离。要描述完全分离，还需要后续的牵引–分离演化关系与断裂能，其示意表达为

$$G_c=\int_{\text{separation path}}\mathbf t\cdot d\boldsymbol\delta.$$

The distinction is analogous to strength versus toughness: reaching an initiation stress is not the same as supplying the work required to propagate separation.

这种区分类似于强度与韧度的区别：达到损伤起始应力，并不等同于提供了使分离继续扩展所需的功。

The source explicitly identifies missing normal and tangential traction histories, rate-dependent strength, mixed-mode fracture energy, and a resolved cohesive zone. [S1, p. 4]

原始材料明确指出，当前缺少法向与切向牵引历程、速率相关强度、混合模态断裂能，以及经过空间解析的黏聚区。[S1，第4页]

There is also a sign-convention issue: positive fluid pressure is compressive, whereas positive cohesive normal traction usually denotes opening tension. The transmitted pressure curve cannot simply be relabelled as cohesive traction without solving the relevant structural/interface problem.

这里还存在符号约定问题：正的流体压力表示压缩，而正的黏聚法向牵引通常表示张开拉伸。在没有求解相应结构或界面问题之前，不能简单地将透射压力曲线改名为黏聚牵引曲线。

### Cohesive-zone length scale / 黏聚区长度尺度

The source’s scaling

原始材料给出的尺度关系

$$\ell_{\mathrm{cz}}\sim\frac{E'G_c}{T_0^2}$$

can be understood from fracture mechanics. With

可以从断裂力学角度理解。由

$$K_c^2\sim E'G_c$$

and near-tip stress scaling

以及裂纹尖端附近的应力尺度关系

$$\sigma\sim\frac{K_c}{\sqrt r},$$

the distance at which stress reaches cohesive strength $T_0$ is

可得应力达到黏聚强度 $T_0$ 时的距离尺度

$$r\sim\left(\frac{K_c}{T_0}\right)^2.$$

Therefore,

因此

$$\boxed{\ell_{\mathrm{cz}}\sim\frac{E'G_c}{T_0^2}}.$$

The coefficient depends on the cohesive law and geometry; the scaling explains why a cohesive simulation needs a sufficiently fine mesh.

其比例系数取决于黏聚定律和几何条件；这一尺度关系说明了为什么黏聚仿真需要足够精细的网格。

## 4.6 Deriving the impulse and energy availability ratios / 推导冲量与能量可用性比值

Let $J_A$ be the selected pressure impulse per unit area and $m'$ the moving mass per unit area. For an idealized rigid layer initially at rest,

以 $J_A$ 表示所选压力历程的单位面积冲量，以 $m'$ 表示运动部分的单位面积质量。对于初始静止的理想刚性层，

$$m'v=J_A.$$

Its kinetic energy per unit area is then

其单位面积动能为

$$\frac{E}{A}=\frac12m'v^2=\boxed{\frac{J_A^2}{2m'}}.$$

Equating this idealized available energy to $G_c$ defines a nominal impulse scale:

令这一理想化的可用能量等于 $G_c$，可定义名义冲量尺度：

$$\boxed{J_{\mathrm{nominal}}=\sqrt{2m'G_c}}.$$

The source therefore forms

因此，原始材料构造了

$$\boxed{\Pi_J=\frac{J_A}{J_{\mathrm{nominal}}}},$$

and separately,

以及另一个独立比值

$$\boxed{\Pi_E=\frac{E_{\mathrm{mode,max}}}{A_{\mathrm{rel}}G_c}}.$$

The reported values,

原始材料给出的数值为

$$\Pi_J=0.565,\qquad\Pi_E=0.767,$$

are scalar availability comparisons. They are neither release probabilities nor local energy-release rates. They also need not obey $\Pi_E=\Pi_J^2$, because the modal-energy calculation and rigid-layer impulse estimate are different reductions. [S1, p. 4]

它们属于标量可用性比较，既不是释放概率，也不是局部能量释放率。它们也不必满足 $\Pi_E=\Pi_J^2$，因为模态能量计算与刚性层冲量估计采用了不同的简化模型。[S1，第4页]

# 5. Sensitivity and the next measurements / 敏感性与下一步测量

*What the theory tells us to measure next. Corresponding to Theory 05, source page 5.*

*理论告诉我们下一步应测量什么。对应 Theory 05，原始材料第5页。*

The final page uses the calculations to prioritize uncertain inputs rather than to declare a validated transfer threshold. Its reported rankings are calculation-only Spearman correlations. [S1, p. 5]

最后一页利用计算结果对不确定输入进行优先级排序，而不是宣称已经得到经验证的转印阈值。其中报告的排序仅来自计算所得的 Spearman 秩相关。[S1，第5页]

## 5.1 What a Spearman ranking measures / Spearman 排序衡量什么

For sampled inputs $X$ and outputs $Y$,

对于抽样得到的输入 $X$ 和输出 $Y$，

$$\boxed{\rho_s=\operatorname{Corr}\bigl(\operatorname{rank}X,\operatorname{rank}Y\bigr)}.$$

It measures whether larger input values tend to accompany larger or smaller outputs. It is not a governing equation, and its magnitude depends on the sampled ranges and assumptions.

它衡量的是：较大的输入值是否倾向于对应较大或较小的输出值。它不是控制方程，其数值大小取决于抽样范围与相关假设。

The directions of several reported relationships can nevertheless be understood from the equations we derived.

不过，原始材料报告的若干关系，其正负方向可以通过已经推导出的方程来理解。

## 5.2 Optical sensitivity follows directly from the temperature scale / 光学敏感性直接来自温升尺度

From

由

$$\Delta T_{\mathrm{ad},0}=\frac{\eta_{\mathrm{abs}}F_0}{\rho_{\mathrm{abs}}c_p\delta_{\mathrm{abs}}},$$

take logarithms:

两边取对数：

$$\ln\Delta T_{\mathrm{ad},0}=\ln\eta_{\mathrm{abs}}+\ln F_0-\ln\delta_{\mathrm{abs}}-\ln(\rho_{\mathrm{abs}}c_p).$$

Holding the other quantities fixed,

保持其他量不变，可得

$$\frac{\partial\ln\Delta T}{\partial\ln F_0}=1,\qquad\frac{\partial\ln\Delta T}{\partial\ln\eta_{\mathrm{abs}}}=1,\qquad\frac{\partial\ln\Delta T}{\partial\ln\delta_{\mathrm{abs}}}=-1.$$

This explains the positive fluence/absorption dependence and negative absorption-depth dependence in the source’s ranking. It does not reconstruct the numerical rank coefficients without the original uncertainty samples. [S1, p. 5]

这解释了原始材料排序中，温升与能量面密度、吸收比例的正相关，以及与吸收深度的负相关。但如果没有原始不确定性样本，就不能据此复现具体的秩相关系数。[S1，第5页]

## 5.3 Bubble-load sensitivity follows from acceleration scaling / 气泡载荷敏感性来自加速度尺度

For comparable dimensionless trajectories with characteristic radius $R_b$ and time $t_b$,

对于无量纲形状相近、特征半径为 $R_b$、特征时间为 $t_b$ 的轨迹，

$$\dot R\sim\frac{R_b}{t_b},\qquad\ddot R\sim\frac{R_b}{t_b^2}.$$

Consequently,

因此

$$A=R^2\ddot R+2R\dot R^2\sim\frac{R_b^3}{t_b^2}.$$

At fixed observation distance $d$, the leading pressure scale is

在观测距离 $d$ 固定时，主导压力尺度为

$$p'\sim\frac{\rho_lR_b^3}{dt_b^2},$$

and a corresponding impulse scale is

相应的冲量尺度为

$$\boxed{J_A\sim\frac{\rho_lR_b^3}{dt_b}}.$$

If stand-off ratio is held fixed instead, so $d=\gamma R_b$,

如果保持不变的是距壁比，即 $d=\gamma R_b$，则

$$J_A\sim\frac{\rho_lR_b^2}{\gamma t_b}.$$

These are explanatory scalings, not substitutes for the disk-average calculation. They show why larger bubbles and shorter motion times tend to increase loading, while also showing that “sensitivity to radius” depends on which geometric quantities are held fixed.

这些属于解释性的尺度关系，不能替代圆盘平均压力计算。它们说明了为什么更大的气泡和更短的运动时间往往会增大载荷，同时也表明，“对半径的敏感性”取决于哪些几何量被保持不变。

The source’s calculated ranking identifies $R_{\max}$ and boundary gain as strong positive influences on growth impulse, and growth time as a negative influence. [S1, p. 5]

原始材料的计算排序表明，$R_{\max}$ 和边界增益对增长阶段冲量具有较强的正向影响，而增长时间具有负向影响。[S1，第5页]

## 5.4 Interface toughness enters the availability ratios explicitly / 界面韧度显式进入可用性比值

For fixed impulse and mass,

当冲量与质量固定时，

$$\Pi_J=\frac{J_A}{\sqrt{2m'G_c}}\propto G_c^{-1/2}.$$

For fixed modal energy and release area,

当模态能量与释放面积固定时，

$$\Pi_E\propto G_c^{-1}.$$

Thus a larger nominal fracture energy decreases both availability ratios. This is consistent with the negative toughness ranking reported for the release surrogate, while remaining conditional on the particular screening calculation. [S1, p. 5]

因此，更大的名义断裂能会使两个可用性比值都减小。这与原始材料中释放替代量对韧度呈负相关的排序一致，但仍然以具体筛查计算的假设为条件。[S1，第5页]

## 5.5 Why the measurement order matters / 为什么测量顺序很重要

The source proposes the following order:

原始材料提出了如下顺序：

$$\begin{gathered}
\text{Optical deposition / 光学沉积}\\\downarrow\\
R(t)\ \text{and bubble geometry / 气泡历程与几何}\\\downarrow\\
\text{Boundary pressure and shear / 边界压力与剪切}\\\downarrow\\
\text{Rate-dependent mixed-mode interface properties}\\
\text{速率相关的混合模态界面性质}
\end{gathered}$$

This order follows the direction of the model dependencies. [S1, p. 5]

这一顺序遵循模型之间的依赖方向。[S1，第5页]

For example, fitting interface toughness while the incident pressure is unknown allows the toughness parameter to compensate for an incorrect loading amplitude. A successful displacement fit would then not identify the true interface property.

例如，在入射压力未知的情况下拟合界面韧度，就可能使韧度参数去补偿错误的载荷幅值。这样一来，即使成功拟合了位移，也不能说明识别出了真实的界面性质。

Likewise, obtaining the correct absorbed energy does not identify activation coefficients, and choosing an $8\ \mu\mathrm m$ bubble does not establish that the laser will generate one. The source explicitly warns against using downstream parameters to compensate for unknown upstream inputs. [S1, p. 5]

同样，得到正确的吸收能量并不意味着识别出了激活系数；选取一个 $8\ \mu\mathrm m$ 的气泡，也不能证明激光会产生这样的气泡。原始材料明确提醒，不应利用下游参数去补偿未知的上游输入。[S1，第5页]

# The complete picture / 完整图景

You can now read the theory as a sequence of different questions:

现在可以将这套理论理解为一系列彼此不同、逐级衔接的问题：

$$\begin{aligned}
&F(r),\ g(t),\ \mu_a\\
&\qquad\longrightarrow Q'''(\mathbf x,t),\ D_{\mathrm{abs}},\ E_{\mathrm{abs}}\\[6pt]
&D_{\mathrm{abs}},\ \dot q'''_{\max},\ \text{droplet state / 液滴状态}\\
&\qquad\longrightarrow p_1,\ P_{\ge1},\ P_{\mathrm{det}}\\[6pt]
&R(t),\ \dot R(t),\ \ddot R(t)\\
&\qquad\longrightarrow p'(\mathbf x,t)\\[6pt]
&p'(\mathbf x,t),\ \text{structural properties / 结构性质}\\
&\qquad\longrightarrow q(t),\ \text{transmitted stress field / 传递应力场}\\[6pt]
&\text{interface tractions and separations / 界面牵引与分离量}\\
&\qquad\longrightarrow\text{damage and possible release / 损伤与可能的释放}.
\end{aligned}$$

The key missing connection in the present source is that **activation and laser heating do not yet generate $R(t)$ through a closed forward model**. The radius history is prescribed. Likewise, the resulting pressure screen does not yet provide validated near-wall loading or resolved cohesive tractions. Those are stated limitations of the supplied theory, not steps that can be filled by algebra alone. [S1, pp. 3–4]

当前原始材料中缺失的关键连接是：**激活与激光加热尚未通过一个闭合的正向模型生成 $R(t)$**。半径历程是人为规定的。同样，由此得到的压力筛查也尚未提供经验证的近壁载荷，或经过空间解析的黏聚牵引。这些都是所提供理论明确说明的限制，而不是仅靠代数运算就能补齐的步骤。[S1，第3–4页]

The most important conceptual separation is:

最重要的概念区分是：

**Energy accounting tells you what is available. Activation statistics tell you whether an event occurs. Bubble mechanics tells you how liquid is accelerated. Structural dynamics tells you how that loading moves the film. Fracture mechanics tells you whether the interface actually separates.**

**能量核算告诉你有多少资源可用；激活统计告诉你事件是否发生；气泡力学告诉你液体如何被加速；结构动力学告诉你这些载荷如何使薄膜运动；断裂力学告诉你界面是否真正发生分离。**

Keeping those questions distinct is what turns a collection of equations into a defensible cavitation-transfer theory.

只有始终区分这些问题，才能把一组方程转化为一套依据清晰、边界明确的空化转印理论。

# Source notes / 来源说明

**[S1] Primary supplied source.** *Laser_Triggered_Cavitation_Theories_20260925.pdf*, five pages, Theory 01–05 (slides 07–11 of the original 17-slide sequence). The pages bear the footer “Laser-Triggered Cavitation Transfer — Detailed bilingual visual notes” and the date 19 September 2026. The filename date and the printed footer date are retained as supplied. The five pages are included unchanged in Appendix A.

**[S1] 用户提供的主要材料。** *Laser_Triggered_Cavitation_Theories_20260925.pdf*，共五页，内容为 Theory 01–05（原17页幻灯片序列中的第07–11页）。各页页脚标为“Laser-Triggered Cavitation Transfer — Detailed bilingual visual notes”，日期为2026年9月19日。文件名日期与页脚日期均按原样保留。五页原文在附录 A 中原样收录。

**[R1] Supplementary link carried over from the preceding explanation.** Spherical radial-flow assumptions and the Rayleigh–Plesset framework; publisher page in *The Journal of the Acoustical Society of America*. No new bibliographic verification or literature expansion was performed for this translation.

**[R1] 沿用前文讲解中的补充链接。** 用于球对称径向流动假设与 Rayleigh–Plesset 框架；链接指向 *The Journal of the Acoustical Society of America* 的出版页面。本次翻译未另外进行书目信息核验或文献扩展。

<https://pubs.aip.org/asa/jasa/article/155/2/1593/3266983/A-unifying-Rayleigh-Plesset-type-equation-for>

**[R2] Supplementary link carried over from the preceding explanation.** The qualification concerning negative pressure and metastable liquids; arXiv record 2410.17626. This preserves the reference already attached to that qualification in the preceding explanation.

**[R2] 沿用前文讲解中的补充链接。** 用于关于负压与亚稳态液体的限定说明；arXiv 记录号为2410.17626。此处保留了前文该项说明所附的参考链接。

<https://arxiv.org/abs/2410.17626>

# Appendix A. Original theory pages / 附录 A：原始理论页面

The next five pages reproduce the supplied PDF without changing its text, equations, charts, or original landscape layout. They provide the original visual context for source references [S1, pp. 1–5].

接下来的五页原样收录用户提供的 PDF，不修改其中的文字、公式、图表或原始横向版式。它们为文中 [S1，第1–5页] 的来源引用提供原始视觉上下文。

The editable Markdown companion contains the full bilingual derivation above. The original graphical pages are preserved in the PDF appendix rather than re-created as Markdown diagrams.

可编辑的 Markdown 配套文件包含上面的完整双语推导。原始图文页面保留于 PDF 附录中，不重新绘制为 Markdown 图形。
