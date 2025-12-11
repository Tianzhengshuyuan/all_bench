Dear Reviewer 6AVH, thank you very much for your careful and detailed review of our submission. We are grateful that you found the core motivation interesting and important, namely that benchmark scores are not inherent properties of a model but outcomes of a specific evaluation system, and that you see value in our attempt to formalize such systems through the MES/A-MES framework in order to support more systematic, reproducible, and fair comparisons between models.

At the same time, we sincerely appreciate your candid and substantive critiques. Your concerns about our experimental design choices, your reservations about our definitions of analogical and out-of-distribution workloads, and your comments on the clarity of the presentation are all very valuable. Your questions about how we should interpret the "ground truth" baseline and whether evaluation under a single or optimized configuration is preferable to averaging over configurations go to the heart of our conceptual framework, and they will help us refine both the methodology and its justification. Below, we respond to your comments and questions point by point, and we will incorporate the corresponding clarifications and additional details in the revised version.

# Response to Weakness 1: Selection of component value ranges and realism of MES configurations

Thank you very much for this careful and constructive comment. We fully agree that unrealistic evaluation settings can easily distort conclusions, so we take this concern seriously. Below we clarify our design choices and the corresponding validation we have performed.

## 1. Parameter Range Selection

In our actual experiments, we first explored temperature with more fine-grained values between 0 and 1, but when constructing the final MES configuration space we deliberately coarsened this dimension to the three values reported in the paper. The reason is combinatorial: with 10 variables, each additional level per variable multiplies the total number of configurations, quickly making systematic exploration intractable. We therefore treated {0.0, 1.0, 2.0} as a compressed parametrization of a richer underlying search, and verified on the finer-grained runs that the qualitative trends we report are consistent with those obtained at higher resolution. The value ranges of the other parameters were similarly compressed for the same reason.

## 2. `max_tokens = 10` does not truncate answers in our setup

Your concern notes that `max_tokens = 10` could truncate answers in typical conversational settings. However, in our non‑CoT evaluation setup, we ask the LLM to use a very compact answer format:

- For multiple-choice questions:  
  `####A####`
- For numeric fill-in-the-blank:  
  `####342####`

Here, `####` is used as a special delimiter and corresponds to *one token* in our tokenizer; thus a complete answer like `####A####` typically consumes only a **small handful of tokens** (about 3 tokens).

Under this constrained format:
- `max_tokens = 10` is more than sufficient to generate complete answers for both multiple-choice and fill-in-the-blank questions.
- In our logs, we do not observe systematic truncation of answers at `max_tokens = 10` for these tasks.


## 3. Temperature = 2.0 does not universally cause "random" outputs

We agree that for some models, pushing temperature to 2.0 can lead to unstable behavior. However, this is model-dependent and not universally true. For example, consider the following configuration for DeepSeek:

```text
{
  'Language': 'yy',
  'Question Format': 0,
  'Question Paraphrase': 0,
  'Shot': 1,
  'COT': 0,
  'Multi Turn': 0,
  'temperature': 2.0,
  'top_p': 0.6,
  'presence_penalty': 0.5,
  'max_tokens': 100
}
```

Under this configuration, the observed accuracy is 56.67%, which is clearly far above random guessing for AIME problems. This indicates that including temperature = 2.0 in the evaluation space is not equivalent to injecting invalid runs. Rather, temperature = 2.0 is challenging but not pathological for the model, and it provides useful information about robustness under aggressive decoding settings.

## 4. Realistic deployment scenarios for `max_tokens = 10` and temperature = 2.0

`max_tokens = 10` does have practical use cases in real deployments, especially when users only need very short responses from the model. By constraining `max_tokens`, applications can cap output length to save time (avoiding long generations when only a brief signal is required) and reduce cost (since pricing is typically proportional to the number of output tokens). Consequently, although `max_tokens = 10` may appear "extreme" from the perspective of open-ended chat, it is a realistic and meaningful setting for short-answer tasks like ours, as well as for many production scenarios that prioritize brevity and efficiency.

Similarly, temperature = 2.0 is not purely an academic extreme. It is used in creative-generation scenarios such as poetry, fiction, and brainstorming, where diversity and novelty are prioritized. It is also employed for generating unusual phrasing or surprising ideas in exploratory ideation tools, where users explicitly trade reliability for creativity. In such applications, practitioners intentionally set a high temperature to push the model away from generic responses. Therefore, we view temperature = 2.0 as a realistic configuration for specific use cases, even if it is not ideal for strict QA-type benchmarks. We include such settings to study how sensitive model performance is to decoding extremes, since real deployments often explore a wide range of temperatures across tasks.

## 5. Why near-zero accuracies are not pathological on AIME’24

AIME problems are extremely difficult, even for human experts. In our author group:
- With strong mathematical backgrounds, we could solve only about one third of the problems without looking at the official solutions.
- Even after carefully studying the solution strategies, we still found about 10% of the problems for which we could not fully understand the solution idea.

Given this difficulty, the concentration of mass near zero in the violin plots (Figure 4(a)) primarily reflects the intrinsic hardness of AIME’24, rather than the use of extreme decoding settings.


## 6. Direct test: removing all `max_tokens = 10` and `temperature = 2.0` runs

To address your concern more directly, we ran an explicit ablation in which we removed all evaluation points with `max_tokens = 10` and all points with `temperature = 2.0`, and then recomputed and replotted the violin plots corresponding to Figure 4(a). The new plots are qualitatively very similar to the originals: the density near zero accuracy is slightly reduced, but the overall shape remains, still with substantial mass close to 0. This indicates that the mass near zero is not primarily caused by these "extreme" settings. Instead, it arises from a combination of the intrinsic difficulty of AIME’24, non‑CoT configurations, less favorable prompts and languages, as well as other factors.

Therefore, excluding max_tokens = 10 and temperature = 2.0 does not materially change our main conclusions or the qualitative distributions of accuracies.

---

In summary, we acknowledge the importance of using realistic and interpretable configurations, and have therefore (i) compressed parameter ranges only after initially exploring finer-grained settings, (ii) carefully designed the answer format so that `max_tokens = 10` is sufficient and non-pathological, (iii) empirically verified that temperature = 2.0 can yield non-random performance across models, (iv) motivated both `max_tokens = 10` and temperature = 2.0 with real deployment scenarios, and (v) confirmed via ablation that removing these "extreme" settings leaves the qualitative accuracy distributions essentially unchanged. Together, these analyses support that our MES configuration space, while intentionally broad, does not artificially inflate variance or undermine the reliability of the reported evaluation results.

# Response to Weakness 2: Motivation and construction of A‑MES and definition of out‑of‑distribution workloads

## 1. On "distractor insertion": robustness vs. analogical generalization

You are absolutely right that our current example (adding an irrelevant sentence) reads like a robustness or adversarial‑style perturbation. Our intention, however, was not to claim that this alone constitutes analogical reasoning; rather, A‑MES is designed to cover a broader family of workload shifts, including robustness to realistic "noise" in user queries.

In real‑world usage, users rarely submit clean, minimal prompts; they often add story background, opinions, meta‑commentary, or partially incorrect intuitions. Users still expect the model to solve the core task correctly despite such "perturbations". From this perspective, introducing redundant or misleading sentences is not artificial but faithfully reflects actual deployment conditions. Evaluating robustness to these perturbations is therefore an essential part of "causally faithful" evaluation.

More importantly, our redundancy insertion is not a single ad‑hoc edit; it is implemented via three explicit, controllable categories, and all instances are generated systematically via LLM prompting:

1. Context‑irrelevant redundancy: sentences completely unrelated to the problem.  
   *Example:* 
   > *The weather today seems quite pleasant, and it might be a great day for a picnic.* Find the number of triples of nonnegative integers $(a,b,c)$ satisfying $a + b + c = 300$ and \[a^2b + a^2c + b^2a + b^2c + c^2a + c^2b = 6,000,000.\] *Also, there are some beautiful flowers blooming in the nearby park.*

   Here, the weather and flowers are entirely unrelated to the math content.

2. Context‑relevant, explanatory redundancy: additional sentences that explain concepts already present in the question (semantics and solution unchanged).  
   *Example:*
   > There exist real numbers $x$ and $y$, both greater than 1, such that $\log_x\left(y^x\right)=\log_y\left(x^{4y}\right)=10$. *A logarithm is a way to express how many times a base must be multiplied by itself to get a certain number*. Find $xy$.

   The added sentence explains the notion of a logarithm while leaving the underlying problem unchanged.

3. Context‑relevant, misleading redundancy: sentences that are thematically related but subtly promote an incorrect heuristic.  
   *Example:* 
   > Alice and Bob play the following game. A stack of $n$ tokens lies before them. The players take turns with Alice going first. On each turn, the player removes either $1$ token or $4$ tokens from the stack. *Many players adopt a greedy approach here: always take $4$ whenever possible to shorten the game and restrict the opponent's replies.* Whoever removes the last token wins. Find the number of positive integers $n$ less than or equal to $2024$ for which there exists a strategy for Bob that guarantees that Bob will win the game regardless of Alice's play.

    The extra sentence about the "greedy approach" is logically related to the game but suggests a flawed strategy, intentionally nudging the solver toward an incorrect line of reasoning  

We also analyzed these categories separately and observed an interesting pattern: context‑irrelevant redundancy tends to cause the largest drop in model accuracy, whereas even deliberately misleading context‑relevant redundancy has a smaller impact on accuracy than context‑irrelevant noise.

Distractor insertion is only one type of analogical transformation we use (with an emphasis on robustness). In addition, we include:

- **Numeric substitution:** we systematically change the numerical constants in the problem while keeping the solution method and underlying structure intact.  
    *Example:*
    - **Original:** Find the largest possible real part of \[(75+117i)z + \frac{96+144i}{z}\] where $z$ is a complex number with $|z|=4$. A common shortcut is to take $z$ to be a positive real number, since for a fixed modulus the real part is often largest when the argument of $z$ is zero.  
    - **Numeric variant:** Find the largest possible real part of \[(100+112i)z + \frac{60+144i}{z}\] where $z$ is a complex number with $|z|=4$. A common shortcut is to take $z$ to be a positive real number, since for a fixed modulus the real part is often largest when the argument of $z$ is zero.

- **Conditional recomposition:** we change which quantity is treated as the "target" and which appears as a given condition, while preserving the same geometric or algebraic relationships.  
    *Example:*
    - **Original:** 
    > Rectangles $ABCD$ and $EFGH$ are drawn such that $D,E,C,F$ are collinear. Also, $A,D,H,G$ all lie on a circle. If $BC=16$,$AB=107$,$FG=17$, and $EF=184$, what is the length of $CE$? 
    - **Conditional recomposition:**
    > Rectangles $ABCD$ and $EFGH$ are drawn such that $D,E,C,F$ are collinear. Also, $A,D,H,G$ all lie on a circle. If $BC=16$,$AB=107$,$CE=104$, and $EF=184$, what is the length of $FG$?

To summarize, in our framework "analogical transformations" are intended to capture a class of reasoning‑preserving modifications: they may change the numerical values or which variable is queried, and may introduce realistic redundancy, but they keep the underlying solution strategy essentially unchanged. This is exactly what we aim to probe—whether the model has internalized the reasoning pattern rather than merely memorized a specific benchmark instance. If the term analogical suggests a narrower notion to you and has contributed to this confusion, we would be happy to adopt a more precise term in the revised version.

## 2. On the use of "out‑of‑distribution" (OOD)

We apologize for the confusion caused by our terminology. Our intention was not to redefine OOD in a way that conflicts with its standard usage in the ML literature. In our setting, we conceptually distinguish three categories of workloads:

1. Seen / potentially memorized: tasks that may have been present (or nearly present) in training.  
2. Unseen but structurally similar: tasks not memorized verbatim, but solvable by applying previously learned patterns or transformations.  
3. Completely novel: tasks that are unlikely to appear in the training corpus and thus probe more genuine generalization.

In the paper, we loosely referred to category (3) as "out‑of‑distribution". Thanks to your comment, we now see that calling this "OOD" can be misleading, since OOD in the general literature often refers to a well‑characterized distributional shift (e.g., different domain, style, or covariates), rather than simply "unseen exam problems". We will adopt a more precise term for this category in the revised version.

# Response to Weakness 3: Lack of a clear definition for the term "LLM workload"

Thank you for pointing out the potential confusion around our use of the term workload and for noting that it may appear to be borrowed from CPU benchmarking. Our intention in using workload is indeed inspired by evaluatology work in computer architecture, but we agree that in the LLM community this term is not yet standard and that our current presentation can be clearer. In our setting, we deliberately distinguish:

- **Task**: an abstract capability or objective (e.g., solving high‑school competition math problems, answering graduate‑level physics questions, writing secure code patches).
- **Workload**: the concrete collection of input instances and their organization used to exercise those tasks under evaluation (e.g., the specific set of AIME'24 problems presented in a particular language, question format, and paraphrase; or MMLU questions instantiated in multiple languages).

We acknowledge that this terminology and its connection to CPU benchmarking are not explained early enough in the current draft, which can indeed cause confusion, especially since we later make a careful distinction between task and workload. To address this, in the revised version we will:

1. **Add an explicit definition of "LLM workload" in the Introduction**, immediately when we first use the term, including:
   - the distinction between *task* and *workload* as described above, and  
   - a brief note that the term is borrowed and adapted from evaluatology in computer systems, but specialized here for LLM evaluation.

2. **Adjust wording in a few places** where we currently alternate between "dataset" and "workload", to ensure consistency:  
   - we will use *task* for capability (e.g., "math reasoning task"),  
   - *workload* for the concrete instantiated set of problems

We hope these clarifications and revisions will make our intent around "LLM workload" more transparent and reduce the cognitive burden on readers unfamiliar with evaluatology terminology.

# Response to Question 1: Redundant reported-accuracy line in figure 4(a)

Thank you for carefully checking Figure 4(a) and for pointing out the issue with the legend.

You are absolutely right: in Figure 4(a) there should not be a separate legend entry for a "reported accuracy line". That item in the legend is a plotting mistake on our side and does not correspond to an actual curve that should be interpreted by the reader.

In the revised version, we will remove the incorrect legend entry from Figure 4(a)

# Response to Question 2: Zero values in Table 3 and Figure 5(a)

Thank you for pointing out the potential confusion regarding the 0 accuracies in Table 3 and Figure 5(a). We realize that similar confusion may also occur for other readers, and we would like to clarify the following:

The 0 accuracies are not placeholders for missing data. For all models listed in Table 3 and Figure 5(a), whenever a model shows 0 accuracy, it means that on our evaluated configuration, the model did not solve any of the AIME'24 problems correctly, not that we lacked data or simply treated "not reported" as zero. 

In fact, under some evaluation settings, 0% accuracy on AIME'24 is not only possible but even expected. AIME is an extremely challenging U.S. mathematics invitational competition: among the authors, even with strong mathematical backgrounds, we can correctly solve only about one third of the problems unaided, and even after carefully studying official solutions there remains roughly 10% of the problems whose step‑by‑step reasoning is still difficult to follow. Given this intrinsic difficulty, it is therefore not surprising that for some models and some configurations—especially those without chain‑of‑thought or suitable prompting—the measured accuracy is 0%, as our experiments indeed show that such configurations often lead to systematic failure on these items.

To avoid misleading readers, in the revision we will explicitly state that a 0 accuracy value means that no problems are solved correctly under the evaluated configurations, rather than indicating missing data. We will also clarify that, given the intrinsic difficulty of AIME and the absence of chain‑of‑thought in some configurations, a 0% accuracy is in fact a realistic and interpretable outcome for certain models and settings.

# Response to Question 3: Interpretation of the "ground truth" baseline in Figure 5(a)

Thank you for raising this – our earlier wording was not precise enough and indeed made it easy to misunderstand how the "ground truth" in Figure 5(a) is constructed. The key point is that the restricted space we exhaustively evaluate is not a subset of the configuration space used for random sampling, and therefore the agreement between the two is not a trivial consequence of variance reduction.

More concretely, for the ANOVA and the "ground truth" in Figure 5(a), we construct a factorial subspace over the 10 components (Language, Question Format, Question Paraphrase, Shot, COT, Multi Turn, temperature, top_p, presence_penalty, max_tokens). For each component, we partition its original value range into a "low" and a "high" level by selecting representative low‑ and high‑value settings, and then take the full factorial combination of these two levels across all 10 components. This yields a 2¹⁰ = 1024-point design that is balanced across all 10 factors.  
     
From this 1024‑point design we run ANOVA and then select the 5 most influential components (e.g., Question Format, COT, max tokens, Shot, Multi Turn for a given model). For these 5 components we then take all of their original value ranges (as listed in Table 2), and for the remaining 5 components we keep them at fixed values. The Cartesian product of "all values of the 5 important components × fixed values of the other 5" defines a new configuration space, on which we perform exhaustive evaluation and average the accuracy. This average is what we call the "restricted‑space ground truth".

In contrast, the random sampling used to construct the confidence intervals in Figure 5(a) is performed over the full 10‑dimensional configuration space defined in Table 2, whose size is 15,552. 
     
We sample configurations uniformly from this full space, evaluate them, and continue sampling until both the sample mean and its confidence interval have converged within the predefined thresholds. 

Importantly, many of the configurations in the restricted space do not appear in the randomly sampled configurations, and vice versa. The restricted space is therefore not a subset of the randomly sampled configuration set.

Consequently, the fact that the confidence intervals derived from random sampling over the full 15,552‑point space consistently cover the mean obtained from exhaustive testing on the separate restricted space is not guaranteed by construction. It is an empirical check of consistency between two different approximations of the "global" performance.

# Response to Question 4: The actual experimental configuration

Thank you for raising this point — it helped us realize that the distinction between Table 1 and Table 2 is not yet sufficiently explicit in the current draft.

In Section 3 we wrote:

> "To make this issue concrete, we systematically reviewed major benchmarks and compiled a taxonomy of which components are explicitly defined and which are left open (Table 1)."

This means that Table 1 is only used to summarize and compare how existing benchmarks and model technical reports typically set (or leave unspecified) the 10 key components. It serves to illustrate the current evaluation practice and its lack of control over many indispensable variables, thereby motivating our methodology. Concretely:

- The rows of Table 1 are different benchmarks (e.g., MMLU, AIME, GPQA, etc.);  
- The columns are the 10 key components (Language, Question Format, Shot, COT, temperature, etc.);  
- The values come from official benchmark documentation and model technical reports and are used to show:
  - which components are explicitly fixed,  
  - which are left open/underspecified or have multiple possible choices,  
  - and how different models are often evaluated on the same benchmark under different configurations.

Thus, Table 1 is a "status-quo taxonomy" of how others evaluate models; it is not the configuration we used in our experiments.

By contrast, Table 2 appears in Section 4 when we introduce our LLM evaluatology methodology and define the Minimal Evaluation System (MES). Table 2 specifies the evaluation conditions (EC) that we actively control and on which our experiments are actually run.

For the MES experiments, we sample configurations from the space defined by Table 2 (Section 5.1: "we conducted 500 random samplings without replacement from the MES configuration space described in Section 4.1. The specific components and their corresponding value ranges are summarized in Table 2.").  

For the A-MES experiments, we augment only the workload part W, while keeping the prompting methods P and decoding parameters D the same as in Table 2 (Section 4.2). The experiments are still run over the EC space defined by Table 2.

So your current assumption is correct: all of our MES and A-MES experiments (including the results in Figure 4, Table 3, and the ANOVA analysis) are conducted under the configuration space specified in Table 2, not Table 1.

In the revised version, we will clarify more explicitly under which configurations our experiments are conducted. 

# Response to Question 5: Appropriate metric for comparing models

Thank you for this thoughtful question; it touches exactly the core design choice behind our methodology. Our position is not that every benchmark must always average over a large configuration space, but that:

1. Different stakeholders have very different, sometimes conflicting, configuration needs, and  
2. If we only report performance under a single (even "optimized") configuration, we systematically bias the benchmark toward some users and against others, and we make causal attribution to the model itself unreliable.

## 1. Why a single "representative" configuration is problematic

In practice, users do not share a single fixed configuration, even for something as simple as temperature:

- Creative writing / brainstorming / ideation.  
  Users typically prefer *higher* temperature (e.g., 0.8–1.0 or even above) to obtain diverse, exploratory outputs.

- Safety‑critical or correctness‑critical use cases (e.g., medical triage support, compliance checks, financial calculations, math competitions).  
  Users usually choose *low* temperature (e.g., 0.0–0.2) and often strict decoding to minimize randomness and hallucinations.

LLMs are deployed to a broad, heterogeneous user base across many domains, not to a homogeneous user who always uses exactly one temperature. If a benchmark fixes the temperature at a single "representative" choice, it implicitly represents some subset of applications at the expense of others. Any single fixed configuration is, unavoidably, a choice of whose use case "counts" as the benchmark.

## 2. Why averaging over a configuration space is useful and what it means

Our method does not claim that "the true user setting is the uniform distribution over all configurations". Instead, we do two things:

1. We explicitly define an evaluation condition space EC (Table 2) over indispensable components (Language, Question Format, Shot, COT, temperature, top‑p, etc.), and  
2. We estimate the expected accuracy under that space by controlled sampling (with convergence checks on the mean and confidence intervals).

This has several motivations:

- Fairness across users.  
    By averaging over multiple plausible configurations, we approximate how a model behaves across a spectrum of realistic use patterns, rather than privileging a single usage style. 

- Causal attributions to the model itself.  
    When different models are evaluated under different, partially specified configurations, observed performance differences can conflate intrinsic model quality with arbitrary choices of prompts and decoding hyperparameters. By defining a shared EC space and averaging over it in a controlled manner, we reduce this confounding and obtain measurements that better reflect the effect of the model itself. In addition, by combining this with ANOVA over the EC space, we can quantitatively decompose variance into contributions from the model and from specific components (e.g., Question Format, COT, max tokens), making the causal structure of the evaluation more transparent.   

Conceptually, our average is a model of an "evaluation user population": instead of assuming a single fixed user behavior, we define an explicit configuration distribution and report the expected performance under that distribution.

## 3. Your example: narrow strong band vs. broad moderate performance

You raise a key trade-off:
> Suppose Model A is excellent within a narrow temperature range on a task, while Model B is slightly worse but maintains decent accuracy across a wider range. Which model is "better"?

If stakeholders care about robustness across settings, then they should prefer B when the mean over a broad configuration space is higher.  

If they care about peak performance under a tightly controlled configuration, they might prefer A — provided they are willing and able to enforce that precise configuration in deployment.

In other words, there is no universally correct answer to "which is better?"; the evaluation outcome depends on individual preferences, and our methodology is compatible with this fact:

- In our experiments, we use relatively broad ranges for each component in EC. However, in the MES framework and the accompanying tooling we propose, the value ranges of all components in EC are user‑configurable rather than fixed.  
- If a user cares about a **narrow** operating regime (e.g., a tight temperature band, fixed language, fixed format), they can set correspondingly narrow ranges and evaluate models under that restricted EC.  
- If a user instead cares about **broader** behavior across diverse configurations, they can define wider ranges for the same components.  

In both cases, the same evaluatology pipeline is applied within the user‑specified EC space, yielding results tailored to their particular preferences.

