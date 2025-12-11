Dear Area Chair,
We sincerely thank you for your time and effort in handling our submission, especially given the complications introduced by the system issues.

Across the reviews, there is clear consensus on the key strengths of our work:
(1) a systematic evaluation framework, where the 10 clearly defined dimensions make LLM evaluation more structured and principled;
(2) compelling evidence that single-configuration benchmarks often produce causally unfaithful inferences by conflating model ability with configuration choices; and
(3) interpretable attribution analysis, enabled by ANOVA, that reveals the main effects and interactions driving performance differences.

The reviewers also raised several constructive concerns, all of which we have thoroughly addressed in the revision and rebuttal. We added missing implementation details, clarified the generalizability of A-MES, refined the sampling and stopping criteria, moderated the causal claims, and provided both cost analyses and justification for the configuration ranges.

Notably, Reviewer 6AVH (rating 2, confidence 4) explicitly stated that our rebuttal resolved most of their concerns and that they are willing to raise their score, which we believe indicates the effectiveness of our clarifications.

A detailed point-by-point response is provided below, and we respectfully submit these updates for the AC's consideration in the final assessment.


# Issues 1: Lack of sufficient implementation details of A-MES.(Reviewer fLKa weakness 1; Reviewer MRzL weakness 1, question 1,2; Reviewer 5j6t question 1; Reviewer 5j6t weakness 1)

In our implementation, A‑MES is instantiated as five systematically defined, script‑driven transformation pipelines including: three analogical (distractor insertion, numeric substitution, conditional recomposition) and two novel (recent‑source adaptation and conceptual synthesis). For each pipeline, we fix general prompts and scaffolding, and then run the entire process automatically through LLM API calls (e.g., GPT‑5), lightweight verification scripts and other auxiliary tooling. This setup scales to large workloads and produces diverse variants, without any per‑item manual rewriting or hand‑crafting of individual problems. Moreover, we are actively exploring additional automated AIME‑style transformation pipelines to further enrich A‑MES.

Overall, these five transformation pipelines realize seven concrete augmentation mechanisms for each workload (here, a workload means a question within the benchmark):

1. Distractor Insertion
   - Context‑irrelevant distractor insertion
   - Context‑relevant explanatory distractor insertion
   - Context‑relevant misleading distractor insertion
2. Numeric substitutions
3. Conditional recomposition
4. Recent‑source adaptation
5. Conceptual synthesis

These mechanisms show that A‑MES is not a collection of ad‑hoc, hand‑edited examples, but a unified, automatable framework that systematically augments existing benchmarks to more comprehensively evaluate model capabilities. For each question within a benchmark, we first apply all seven mechanisms to construct the full space of augmented variants, filtering out transformation attempts that fail (e.g., numeric substitutions or conditional recomposition without a stable solver). Evaluation then samples directly from this augmentation space, ensuring that no invalid transformations are ever selected. The framework enumerates the entire augmentation space upfront, and the small number of discarded variants has negligible impact on overall coverage or robustness. For several major benchmarks, we have already constructed the corresponding augmentation spaces and plan to release them publicly in future work. Below, we provide concrete descriptions of the seven mechanisms.

## 1. Analogical‑1: distractor insertion with three well-defined categories

For distractor insertion, we define three explicit, controllable categories of redundancy and implement all instances via LLM prompting. To ensure that the inserted distractors strictly follow our predefined specifications, we empirically test several candidate LLMs and choose the one that most consistently adheres to these constraints (GPT-5). This selection is made solely to guarantee transformation fidelity rather than to compare model capabilities. For each item to be transformed, the chosen LLM is invoked through an API and, guided by our structured prompts, automatically produces and inserts the required redundant content. The prompts are provided below.

- **Context‑irrelevant redundancy**  
  - Provide the LLM with an example containing an original question and a version with added context‑irrelevant redundancy.  
  - Instruct the LLM to insert one sentence at a random position that is completely unrelated to the target question.

- **Context‑relevant, explanatory redundancy**  
  - Provide the LLM with an example of an original question and a version with added explanatory redundancy.  
  - Instruct the LLM to insert a redundant sentence at a random position in each target question that explains a concept already appearing in the target question.

- **Context‑relevant, misleading redundancy**  
  - Provide the LLM with an example containing an original question and a version with added misleading but logically related redundancy.  
  - Supply the model with the correct answer and several correct solution approaches, and instruct it to avoid directly hinting at these correct strategies when crafting the misleading cue. The official answer and solution approaches are provided by the user, and providing solution approaches is optional.
  - Instruct the model to insert a redundant sentence that nudges the reader toward an incorrect strategy or line of reasoning, without explicitly revealing that it is "misleading" or "distracting".
  
In practice, the selected LLM produces variations that are more diverse and linguistically natural than manual editing. In particular, its context‑relevant misleading redundancies tend to hint at incorrect heuristics in a more subtle way than hand‑written versions, while still strictly adhering to the predefined category constraints. The entire process involves no per‑item manual editing. The three examples of redundancy for three types generated by the above procedure are illustrated as follows:

1. Context‑irrelevant redundancy example:
   > *The weather today seems quite pleasant, and it might be a great day for a picnic.* Find the number of triples of nonnegative integers $(a,b,c)$ satisfying $a + b + c = 300$ and \[a^2b + a^2c + b^2a + b^2c + c^2a + c^2b = 6,000,000.\]

   Here, weather is entirely unrelated to the math content.

2. Context‑relevant, explanatory redundancy example:
   > There exist real numbers $x$ and $y$, both greater than 1, such that $\log_x\left(y^x\right)=\log_y\left(x^{4y}\right)=10$. *A logarithm is a way to express how many times a base must be multiplied by itself to get a certain number*. Find $xy$.

   The added sentence explains the notion of a logarithm while leaving the underlying problem unchanged.

3. Context‑relevant, misleading redundancy example:
   > Alice and Bob play the following game. A stack of $n$ tokens lies before them. The players take turns with Alice going first. On each turn, the player removes either $1$ token or $4$ tokens from the stack. *Many players adopt a greedy approach here: always take $4$ whenever possible to shorten the game and restrict the opponent's replies.* Whoever removes the last token wins. Find the number of positive integers $n$ less than or equal to $2024$ for which there exists a strategy for Bob that guarantees that Bob will win the game regardless of Alice's play.

    The extra sentence about the "greedy approach" is logically related to the game but suggests a flawed strategy, intentionally nudging the solver toward an incorrect line of reasoning  

## 2. Analogical‑2: numeric substitutions via code‑based solution extraction

For numeric substitutions, we use a uniform pipeline built around LLM‑generated Python solvers and automatic verification scripts, rather than manually changing a few numbers:

1. We first call an LLM to extract the primary knowledge points tested by the original problem, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
2. We feed the original problem, its official answer, the retrieved formulas, and (where available) multiple correct solution sketches into the LLM. The official answer and solution sketches are provided by the user, and providing solution sketches is optional.
3. The LLM is prompted to:
   - analyze the problem's solution strategy, using the provided solution sketches when available
   - write a Python solution program where problem‑specific numbers are extracted as explicit variables with reasonable value ranges.
4. We then ask another LLM to inspect the generated Python code and verify that it implements a general computational procedure for solving the problem, rather than relying on hard‑coded instance‑specific outputs or trivial pattern matching.
5. We import the LLM‑generated Python code as a local module and call its solve() function with the original numeric values as inputs, checking whether the resulting output matches the official answer.
6. If the code fails (wrong answer or runtime error), we return the error message and incorrect output to the LLM, asking it to refine the code; we repeat this refinement–verification loop for up to five attempts and keep the Python code if it passes on the original instance.

After obtaining a correct solver, we automatically sample new numeric configurations within the validated ranges to generate analogical variants of the same underlying problem. For example:

- **Original:** Find the largest possible real part of \[(75+117i)z + \frac{96+144i}{z}\] where $z$ is a complex number with $|z|=4$. A common shortcut is to take $z$ to be a positive real number, since for a fixed modulus the real part is often largest when the argument of $z$ is zero.  
- **Numeric variant:** Find the largest possible real part of \[(100+112i)z + \frac{60+144i}{z}\] where $z$ is a complex number with $|z|=4$. A common shortcut is to take $z$ to be a positive real number, since for a fixed modulus the real part is often largest when the argument of $z$ is zero.

This "knowledge‑point extraction → formula retrieval → analyze → code → verify → resample" pipeline is identical across all problems.

## 3. Analogical‑3: conditional recomposition via invertible‑condition analysis

For conditional recompositions, we again adopt a general and automatable pipeline built around LLM‑generated Python solvers and automatic verification scripts rather than manually rewriting statements:

1. We first call an LLM to extract the primary knowledge points tested by the original question, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
2. We feed the original problem, its official answer, the retrieved formulas, and (where available) multiple correct solution sketches into the LLM. The official answer and solution sketches are provided by the user, and providing solution sketches is optional.
3. The LLM is prompted to:
   - identify the key conditions and the target quantity;
   - determine whether some of these conditions and the target can be interchanged—i.e., whether knowing the original answer allows us to infer some of the original conditions (an invertible relationship).
4. When such an invertible relationship exists, the LLM is asked to write a Python solution program for the recomposed problem, where the original target now appears as an input condition and (a subset of) the original conditions become the new target.
5. We then ask another LLM to inspect the generated Python code and verify that it implements a general computational procedure for solving the problem, rather than relying on hard‑coded instance‑specific outputs or trivial pattern matching.
6. We import the LLM‑generated Python code as a local module and call its solve() function, plugging the original answer value into the new "condition" slot and checking whether the returned output correctly recovers the original condition values.
7. Any discrepancy or runtime error is fed back to the LLM for iterative refinement, just as in the numeric substitutions pipeline. we repeat this refinement–verification loop for up to five attempts and keep the Python code if it passes on the instance.

Once a correct solver for the recomposed version is obtained, we can further vary the new input variables within reasonable ranges to generate additional condition‑recomposed variants.

- **Original:** 
> Rectangles $ABCD$ and $EFGH$ are drawn such that $D,E,C,F$ are collinear. Also, $A,D,H,G$ all lie on a circle. If $BC=16$,$AB=107$,$FG=17$, and $EF=184$, what is the length of $CE$? 
- **Conditional recomposition:**
> Rectangles $ABCD$ and $EFGH$ are drawn such that $D,E,C,F$ are collinear. Also, $A,D,H,G$ all lie on a circle. If $BC=16$,$AB=107$,$CE=104$, and $EF=184$, what is the length of $FG$?

These conditional recompositions are therefore produced by a uniform "knowledge‑point extraction → formula retrieval → analyze → code → verify → resample" pipeline, not by hand‑crafting each rephrased problem.

## 4. Novel‑1: recent‑source adaptation via structured retrieval and paraphrasing

In the "novel" branch, the first mechanism is recent‑source adaptation, which is also fully scriptable:

1. We first use an LLM to extract the primary knowledge points tested by a given source problem.
2. We query open‑access repositories of centralized exam questions that index items by region, year, subject, and knowledge point, and crawl the most recent 2025 exam problems matching the extracted knowledge points.
3. The retrieved problems are paraphrased by the LLM and can be further transformed using the three analogical methods (redundancy insertion, numeric substitution, and conditional recomposition).

This yields a set of new, recent‑source problems that are structurally aligned at the knowledge level but clearly distinct in surface form and provenance. The entire workflow is driven by scripts and general prompts, without hand‑curating individual items.

## 5. Novel‑2: textbook‑based conceptual synthesis via a parsed knowledge base

The second "novel" mechanism is conceptual synthesis from authoritative textbooks. We first crawl a large collection of authoritative textbooks across different subjects from the web, and then use the LLM API's built‑in functionality for parsing local PDF files to extract their content. Based on the extracted content, we build a structured knowledge base in which each concept is associated with definitions, properties, theorems, phenomena, and canonical examples extracted from the textbooks.

1. Given a problem to be augmented, we use an LLM to identify its main knowledge points, and then retrieve the corresponding entries from the structured knowledge base. If the subject‑specific knowledge base is missing, we trigger the textbook crawling and parsing step to expand the knowledge base, and then retrieve the corresponding entries from it.
2. Conditioned on these entries, the LLM is prompted to generate new conceptual questions targeting the underlying knowledge points, rather than copying any existing problem.

For example, one generated question associated with the concept of *logarithms* is: 
> What kind of mathematical idea/method turns exponentiation and multiplication into multiplication and addition?

This pipeline turns textbook content into fresh conceptual questions that align with the original topic but are novel in form and focus.

# Issue 2: Unclear whether the method can generalize. (Reviewer fLKa weakness 4; Reviewer 5j6t weakness 2)

Our methodology is not limited to public academic benchmarks and naturally extends to non‑benchmark settings. As long as there exists a seed workload—such as an enterprise’s internal question bank, a school or institutional exam repository, or other custom task collections—our MES/A‑MES pipeline can be instantiated on top of it without any conceptual change. In this view, the internal or proprietary workload simply serves as the workload component in our framework; our tooling then automatically constructs the corresponding configuration space, performs workload augmentation, and runs the same sampling and attribution procedures. This enables organizations to obtain causally interpretable, system‑level evaluations tailored to their own private or domain‑specific tasks, rather than being restricted to public academic reasoning benchmarks.

Furthermore, our method is in fact fully generalizable. Specifically, we would like to clarify that our LLM evaluatology framework is task‑agnostic: once we define the set of evaluation variables (C1–C10) and their value ranges, the MES configuration space and the corresponding A‑MES workflows are automatically generated by our tooling. The procedures for random sampling, convergence‑based stopping, and ANOVA remain unchanged regardless of whether the benchmark is reasoning(AIME), knowledge (MMLU), science (GPQA), coding, or multi‑turn, and in our current experiments we apply this pipeline to AIME, MMLU, and GPQA with no benchmark‑specific adaptation or custom engineering, demonstrating that the framework already works out‑of‑the‑box across three different benchmarks. We are actively extending the framework to additional benchmarks, including coding, tool‑use, long‑context, and more complex multi‑turn interactions, following exactly the same methodology.

# Issue 3: Lack of guidance on sample size and variance (Reviewer fLKa weakness 2)

In our experiments, for each benchmark, we first construct a configuration space of 15,552 distinct settings defined by ten controllable variables (e.g., Language, Question Format, Question Paraphrase, Shot, Chain-of-Thought, Multi-Turn, temperature, top_p, presence_penalty, and max_tokens). We then generate workload-level variants for each setting using the seven augmentation mechanisms, producing a ~100,000-point configuration space. This forms the full configuration space for the benchmark. From this space, we determine the required sample size using two stopping criteria. To implement random sampling while ensuring reproducibility and consistency across model evaluations, we randomly shuffle the  diverse settings using a random seed to form a list and select the first <sample_size> configurations. This procedure, which was only briefly mentioned in the main text, will be described in detail in the revised version.

## Convergence-based stopping rule

For each workload, when testing each model, we evaluate configurations sequentially in batches of 10 from the shuffled list. After every 10 samples, we compute the running mean accuracy and its 95% confidence interval. We stop sampling when both of the following conditions are satisfied:

1. The absolute changes in the running mean accuracy over the last three consecutive updates are all smaller than 0.002; that is, the absolute differences between the last and second‑last, the second‑last and third‑last, and the third‑last and fourth‑last running means are each smaller than 0.002.
2. The length of the 95% confidence interval is smaller than 0.06.

Using this rule, the sample sizes at which different models converged were:

- GPT‑4.1: 260  
- GPT‑3.5: 220  
- Mistral Medium: 260  
- Mistral Large: 290  
- Qwen Plus: 260  
- Qwen2.5: 400  
- DeepSeek‑V3: 320  
- Doubao‑1.5‑pro‑32k: 480  
- Moonshot‑v1: 220  

## LLN-based stopping rule

To further validate the above convergence-based sample sizes, we used a Law of Large Numbers (LLN)–based estimation. For each model, we first used the observed accuracies on the sampled configurations to estimated the variance of accuracy, and then computed the minimal sample size required to ensure that the sample mean is within a small error tolerance of the true mean with high probability. This gave the following estimates:

- GPT‑4.1: 170  
- GPT‑3.5: 88  
- Mistral Medium: 229  
- Mistral Large: 253  
- Qwen Plus: 218  
- Qwen2.5: 329  
- DeepSeek‑V3: 285  
- Doubao‑1.5‑pro‑32k: 421  
- Moonshot‑v1: 63  

Importantly, for every model, the LLN-estimated minimal sample size is smaller than the sample size returned by the convergence method above. Therefore, we conservatively adopt the larger convergence-based sample sizes in our experiments.

## Practical guidance for practitioners

To make this concrete for other practitioners, we summarize how one can determine sample sizes and stopping criteria in a new setting, even with a different configuration space or benchmark:

1. **Define and enumerate the configuration space.**  
   - Identify the evaluation variables (analogous to our C1–C10 in Table 2: workload, prompting, decoding, etc.) and specify a finite value range for each.  
   - Enumerate the full Cartesian product of these values to obtain a discrete configuration space. 

2. **Fix a global shuffled order and share it across models.**  
   - Use a fixed random seed to randomly permute the full list of configurations once.  
   - Reuse this single shuffled order for all models and workloads.  
   - Always sample configurations as the first N entries of this global list, rather than re‑shuffling per model or per run. 

3. **Joint stopping rule based on convergence and the Law of Large Numbers**  
   - First fix a batch size (e.g., 10), and follow a globally shuffled configuration order; advance by one batch at a time (i.e., evaluate `batch size` configurations per step).  
   - After each batch, recompute, based on all configurations evaluated so far, the model’s mean accuracy on the given benchmark and the corresponding 95% confidence interval.  
   - When the following conditions are met:  
     1. The mean accuracy is effectively stable (e.g., the differences between the last four mean accuracies are all smaller than 0.002), and  
     2. The 95% confidence interval is sufficiently narrow (e.g., interval length < 0.06),  
     the estimate can be regarded as converged at the current sample size N_conv, yielding a converged sample size and mean accuracy.  
   - After convergence, apply a simple Law of Large Numbers–based estimation, using the variance of the current results to compute how many samples are theoretically required to achieve the desired error tolerance and confidence level, giving an "LLN-based sample size" \(N_{\text{LLN}}\).  
   - If \(N_{\text{LLN}}\) is larger than the current N_conv, continue sampling along the same shuffled order until at least \(N_{\text{LLN}}\) configurations have been evaluated; otherwise, stop sampling.

The entire evaluation workflow described above is implemented in an automation scripts. After publication, these scripts will be released as open source, so that practitioners can perform evaluation following the guidance with minimal effort.

# Issue 4: The contribution to causality may be overstated. (Reviewer MRzL weakness 2; Reviewer 5j6t weakness 5) 

Our "causal" contribution lies in  contributing a systematic approach to uncovering causal relationships in complex LLM evaluation systems. Specifically, we construct a minimal evaluation system (MES and A‑MES) that explicitly defines the essential components of evaluation and systematically controls them. This allows us to attribute observed performance differences to specific factors and their interactions, addressing the core challenge that in complex systems “everyone is a stakeholder.”

Existing LLM evaluations do not emphasize the notion of attribution and tend to overlook the impact of confounding factors. In practice, the observed accuracy depends on workload format, prompt methods, decoding parameters, and even system‑level factors. However, current benchmarks typically do not ask whether the measured accuracy is due to the model itself or to these confounders. We make this attribution question explicit and place it at the center of our evaluation design.

To our knowledge, we are the first to define a minimal evaluation system covering 10 key factors and to systematically analyze their contributions to LLM output variance. While our work does not introduce conventional causal inference methods, our work makes a foundational contribution by providing a systematic approach to characterize true causal effects and accurately attribute performance differences in complex LLM evaluation systems. Beyond technical implementation, this framework establishes a principled methodology that moves LLM evaluation beyond single-setting snapshots, enabling more interpretable, reproducible, and comprehensive assessments across diverse conditions. we will clarify this distinction in the revised manuscript to avoid overstating the use of causal language.

# Issue 5: The experimental design has issues in the choice of component value ranges; these settings are rarely used in real deployments, and the near-zero accuracies are likely driven by extreme configurations. (Reviewer 6AVH weakness 1)

We fully agree that unrealistic evaluation settings can easily distort conclusions, so we take this concern seriously. Below we clarify our design choices and the corresponding validation we have performed.

## 1. Parameter Range Selection

In our actual experiments, we first explored temperature with more fine-grained values between 0 and 1, but when constructing the final MES configuration space we deliberately coarsened this dimension to the three values reported in the paper. The reason is combinatorial: with 10 variables, each additional level per variable multiplies the total number of configurations, quickly making systematic exploration intractable. We therefore treated {0.0, 1.0, 2.0} as a compressed parametrization of a richer underlying search, and verified on the finer-grained runs that the qualitative trends we report are consistent with those obtained at higher resolution. The value ranges of the other parameters were similarly compressed for the same reason.

## 2. `max_tokens = 10` does not truncate answers in our setup

The reviewer's concern notes that `max_tokens = 10` could truncate answers in typical conversational settings. However, in our non‑CoT evaluation setup, we ask the LLM to use a very compact answer format:

- For multiple-choice questions:  
  `####A####`
- For numeric fill-in-the-blank:  
  `####342####`

Here, `####` is used as a special delimiter and corresponds to *one token* in our tokenizer; thus a complete answer like `####A####` typically consumes only a **small handful of tokens** (about 3 tokens).

Under this constrained format:
- `max_tokens = 10` is more than sufficient to generate complete answers for both multiple-choice and fill-in-the-blank questions.
- In our logs, we do not observe systematic truncation of answers at `max_tokens = 10` for these tasks.

## 3. `temperature = 2.0` does not universally cause "random" outputs

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

Under this configuration, the observed accuracy is 56.67%, which is clearly far above random guessing for AIME problems. This indicates that including `temperature = 2.0` in the evaluation space is not equivalent to injecting invalid runs. Rather, `temperature = 2.0` is challenging but not pathological for the model, and it provides useful information about robustness under aggressive decoding settings.

## 4. Realistic deployment scenarios for `max_tokens = 10` and `temperature = 2.0`

`max_tokens = 10` does have practical use cases in real deployments, especially when users only need very short responses from the model. By constraining `max_tokens`, applications can cap output length to save time (avoiding long generations when only a brief signal is required) and reduce cost (since pricing is typically proportional to the number of output tokens). Consequently, although `max_tokens = 10` may appear "extreme" from the perspective of open-ended chat, it is a realistic and meaningful setting for short-answer tasks like ours, as well as for many production scenarios that prioritize brevity and efficiency.

Similarly, `temperature = 2.0` is not purely an academic extreme. It is used in creative-generation scenarios such as poetry, fiction, and brainstorming, where diversity and novelty are prioritized. It is also employed for generating unusual phrasing or surprising ideas in exploratory ideation tools, where users explicitly trade reliability for creativity. In such applications, practitioners intentionally set a high temperature to push the model away from generic responses. Therefore, we view `temperature = 2.0` as a realistic configuration for specific use cases, even if it is not ideal for strict QA-type benchmarks. We include such settings to study how sensitive model performance is to decoding extremes, since real deployments often explore a wide range of temperatures across tasks.

## 5. Why near-zero accuracies are not pathological on AIME'24

AIME problems are extremely difficult, even for human experts. In our author group:
- With strong mathematical backgrounds, we could solve only about one third of the problems without looking at the official solutions.
- Even after carefully studying the solution strategies, we still found about 10% of the problems for which we could not fully understand the solution idea.

Given this difficulty, the concentration of mass near zero in the violin plots (Figure 4(a)) primarily reflects the intrinsic hardness of AIME’24, rather than the use of extreme decoding settings.

## 6. Direct test: removing all `max_tokens = 10` and `temperature = 2.0` runs

To address his concern more directly, we ran an explicit ablation in which we removed all evaluation points with `max_tokens = 10` and all points with `temperature = 2.0`, and then recomputed and replotted the violin plots corresponding to Figure 4(a). The new plots are qualitatively very similar to the originals: the density near zero accuracy is slightly reduced, but the overall shape remains, still with substantial mass close to 0. This indicates that the mass near zero is not primarily caused by these "extreme" settings. Instead, it arises from a combination of the intrinsic difficulty of AIME'24, non‑CoT configurations, less favorable prompts and languages, as well as other factors.

Therefore, excluding `max_tokens = 10` and `temperature = 2.0` does not materially change our main conclusions or the qualitative distributions of accuracies.

In summary, we acknowledge the importance of using realistic and interpretable configurations, and have therefore (i) compressed parameter ranges only after initially exploring finer-grained settings, (ii) carefully designed the answer format so that `max_tokens = 10` is sufficient and non-pathological, (iii) empirically verified that `temperature = 2.0` can yield non-random performance across models, (iv) motivated both `max_tokens = 10` and `temperature = 2.0` with real deployment scenarios, and (v) confirmed via ablation that removing these "extreme" settings leaves the qualitative accuracy distributions essentially unchanged. Together, these analyses support that our MES configuration space, while intentionally broad, does not artificially inflate variance or undermine the reliability of the reported evaluation results.

# Issue 6: Complexity and practical burden on practitioners might be too high (Reviewer 5j6t weakness 3)

We understand the concern that our MES/A‑MES framework may appear complex or costly. While the initial evaluation exceeds a single-number benchmark, this cost is intrinsic to rigorous attribution: standard evaluations cannot disentangle the effects of question format, prompting, decoding parameters, or other factors.

Controlling cost and ensuring scalability. We do not exhaustively explore all MES configurations; instead, we sample configurations grounded in convergence and law of large numbers stopping criterion, keeping evaluation bounded. Tooling automates configuration space construction and sampling, A‑MES transformations, and ANOVA analysis, so users only need to specify which C‑variables to include, their value ranges, and their evaluation budget. Experiments show that a moderate number of sampled configurations suffices to obtain stable variable-importance rankings.

Practical insights for future use. The initial full evaluatology run identifies high-impact variables (e.g., Question Format, max_tokens) and low-impact ones (e.g., presence_penalty). Subsequent users can focus on the key factors, holding others constant, to capture most insights at a fraction of the cost. In this way, the first run, though more expensive, produces a prioritized, actionable view of the evaluation space, enabling lighter-weight, task-tailored evaluatology afterward.

# Issue 7: Can ANOVA factor importance generalize? (Reviewer 5j6t question2)

Our empirical results indicate that ANOVA‑based factor importance exhibits both cross‑benchmark regularities and benchmark‑specific characteristics.

On the regularity side, some factors consistently emerge as highly influential across models and benchmarks. For example, in all the benchmarks we analyzed, both Question Format and COT have large and statistically significant effects on accuracy. This suggests that these factors are not idiosyncratic to a single dataset, but rather reflect general sensitivities of current LLMs to how questions are formatted and whether reasoning is explicitly elicited.

On the benchmark‑specific side, we also observe clear differences. A salient example is Question Paraphrase: on AIME, Question Paraphrase has negligible effect, indicating that paraphrasing difficult math problems does not reliably change model accuracy; in contrast, on MMLU, paraphrasing often becomes a key factor— for several models, Question Paraphrase reach statistical significance and explain a non‑trivial share of variance. 

In ongoing work, we are extending the ANOVA analysis to more tasks and models to more systematically characterize which factors generalize and which are dataset‑dependent. We will update the paper with these expanded results as soon as they are ready.

# Issue 8: Whether a benchmark should evaluate models by averaging across all possible ones instead of under a representative configuration (Reviewer 6AVH question 5)

Our position is not that every benchmark must always average over a large configuration space, but that:

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

## 3. Reviewer's example: narrow strong band vs. broad moderate performance

He raises a key trade-off:
> Suppose Model A is excellent within a narrow temperature range on a task, while Model B is slightly worse but maintains decent accuracy across a wider range. Which model is "better"?

If stakeholders care about robustness across settings, then they should prefer B when the mean over a broad configuration space is higher.  

If they care about peak performance under a tightly controlled configuration, they might prefer A — provided they are willing and able to enforce that precise configuration in deployment.

In other words, there is no universally correct answer to "which is better?"; the evaluation outcome depends on individual preferences, and our methodology is compatible with this fact:

- In our experiments, we use relatively broad ranges for each component in EC. However, in the MES framework and the accompanying tooling we propose, the value ranges of all components in EC are user‑configurable rather than fixed.  
- If a user cares about a **narrow** operating regime (e.g., a tight temperature band, fixed language, fixed format), they can set correspondingly narrow ranges and evaluate models under that restricted EC.  
- If a user instead cares about **broader** behavior across diverse configurations, they can define wider ranges for the same components.  

In both cases, the same evaluatology pipeline is applied within the user‑specified EC space, yielding results tailored to their particular preferences.

# Issue 9: What is the single evaluation score after MES/A-MES exploration? (Reviewer 5j6t question 3)

This is a very valuable question, and we acknowledge that this part was not fully explicit in the paper. Ultimately, practitioners need a single evaluation score per model. In our framework, this is addressed statistically and guided by the intended evaluation goals.

First, the selection of a representative score can be aligned with the stakeholders’ priorities—for example, focusing on specific evaluation dimensions or practical usage scenarios that matter most.

Second, the A‑MES sampling space naturally subsumes the MES space, as each original MES instance is included as one of the possible augmentations. By sampling from the broader A‑MES space, we effectively cover a wider range of configurations and potential use cases, while still maintaining a non-zero probability of evaluating the original MES settings.

The final reported evaluation score for each model is then the mean performance over the sampled instances, together with 95% and 99% confidence intervals, providing a stable summary metric that balances comprehensiveness with practical efficiency.

# Issue 10: Why question paraphrase in Table 2 is binary (Reviewer MRzL question 3)

The "Question Paraphrase" column in Table 2 is binary by design, which does not imply that there is only a single way to paraphrase a question. The binary flag distinguishes two regimes:

- No (original): the original question text is used, which may appear in a model's training data.
- Yes (paraphrased): the question is restated in different wording while preserving all underlying semantics, answers, numerical values, and natural language constraints, avoiding potential data‑contamination issues.

To construct paraphrases, we first compare several candidate LLMs on a small validation set and select the one that reliably follows these constraints. This model is then instructed to restate each question, ensuring semantic equivalence while changing surface wording. The purpose of this binary indicator is to diagnose memorization and data‑contamination effects: comparing model performance on original versus paraphrased items reveals whether behavior is robust to rewording or overly tied to specific training instances. The specific paraphrasing strategy or number of rewrites is irrelevant for this goal.

Within MES, all workload transformations—including Question Paraphrase—preserve intrinsic semantics, providing alternative surface realizations of the same task. By contrast, A‑MES analogical transformations (distractor insertion, numeric substitution, condition recomposition) alter problem structure while maintaining core reasoning patterns, producing a family of structurally varied, more challenging variants.Therefore, keeping Question Paraphrase as a binary indicator cleanly separates same‑semantics rewording from the structural, changed‑semantics regime in A‑MES, aligning the design with our evaluation objectives.

# Issue 11: Motivation and construction of A‑MES and definition of out‑of‑distribution workloads (Reviewer 6AVH weakness 2)

The reviewer was absolutely right that our current example (adding an irrelevant sentence) reads like a robustness or adversarial‑style perturbation. Our intention, however, was not to claim that this alone constitutes analogical reasoning; rather, A‑MES is designed to cover a broader family of workload shifts, including robustness to realistic "noise" in user queries.

In real‑world usage, users rarely submit clean, minimal prompts; they often add story background, opinions, meta‑commentary, or partially incorrect intuitions. Users still expect the model to solve the core task correctly despite such "perturbations". From this perspective, introducing redundant or misleading sentences is not artificial but faithfully reflects actual deployment conditions. Evaluating robustness to these perturbations is therefore an essential part of "causally faithful" evaluation.

More importantly, our redundancy insertion is not a single ad‑hoc edit; it is implemented via three explicit, controllable categories, and all instances are generated systematically via LLM prompting:

1. Context‑irrelevant redundancy: sentences completely unrelated to the problem.  
   *Example:* 
   > *The weather today seems quite pleasant, and it might be a great day for a picnic.* Find the number of triples of nonnegative integers $(a,b,c)$ satisfying $a + b + c = 300$ and \[a^2b + a^2c + b^2a + b^2c + c^2a + c^2b = 6,000,000.\] 

   Here, the weather is entirely unrelated to the math content.

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

To summarize, in our framework "analogical transformations" are intended to capture a class of reasoning‑preserving modifications: they may change the numerical values or which variable is queried, and may introduce realistic redundancy, but they keep the underlying solution strategy essentially unchanged. This is exactly what we aim to probe—whether the model has internalized the reasoning pattern rather than merely memorized a specific benchmark instance. 

## 2. On the use of "out‑of‑distribution" (OOD)

We apologize for the confusion caused by our terminology. Our intention was not to redefine OOD in a way that conflicts with its standard usage in the ML literature. In our setting, we conceptually distinguish three categories of workloads:

1. Seen / potentially memorized: tasks that may have been present (or nearly present) in training.  
2. Unseen but structurally similar: tasks not memorized verbatim, but solvable by applying previously learned patterns or transformations.  
3. Completely novel: tasks that are unlikely to appear in the training corpus and thus probe more genuine generalization.

In the paper, we loosely referred to category (3) as "out‑of‑distribution". Thanks to his comment, we now see that calling this "OOD" can be misleading, since OOD in the general literature often refers to a well‑characterized distributional shift (e.g., different domain, style, or covariates), rather than simply "unseen exam problems". We will adopt a more precise term for this category in the revised version.

# Issue 12: Lack of a clear definition for the term "LLM workload" (Reviewer 6AVH question 3)

Our use of "workload" is indeed inspired by the computer architecture community. In our setting, a "workload" corresponds to a question within a benchmark that needs to be solved by the LLM, while a "task" has a closely related but slightly more general meaning, referring for example to a broader type of question or capability. However, we agree that the term "workload" is not yet standardized in the LLM community, and that both the term itself and its connection to CPU benchmarking are not introduced early enough in the paper, so the current presentation will be made clearer in the revision.

# Issue 13: Is 500 random sampling enough? (Reviewer MRzL question 4)

For each benchmark, we first construct a configuration space of 15,552 distinct settings defined by ten controllable variables (e.g., Language, Question Format, Question Paraphrase, Shot, Chain-of-Thought, Multi-Turn, temperature, top_p, presence_penalty, and max_tokens). We then generate workload-level variants for each setting using the seven augmentation mechanisms, producing a ~100,000-point configuration space. To implement random sampling while ensuring reproducibility and consistency across model evaluations, we randomly shuffle the diverse settings using a random seed to form a list and select the first <sample_size> configurations.

This sample size choice is not arbitrary: we first determine per‑model sample sizes using an explicit convergence procedure, and then additionally validate them with an LLN‑based calculation. The final "500" threshold is thus a conservative upper cap backed by two independent criteria rather than a heuristic guess.

Concretely, when testing each model on each workload, we process configurations in batches of 10. After every 10 samples, we compute the running mean accuracy and its 95% confidence interval, and we stop sampling once both of the following conditions are satisfied:

1. The absolute changes in the running mean accuracy over the last three consecutive updates are all smaller than 0.002; that is, the absolute differences between the last and second‑last, the second‑last and third‑last, and the third‑last and fourth‑last running means are each smaller than 0.002.
2. The length of the 95% confidence interval is smaller than 0.06.

Using this rule, the sample sizes at which different models converged were:

- GPT‑4.1: 260  
- GPT‑3.5: 220  
- Mistral Medium: 260  
- Mistral Large: 290  
- Qwen Plus: 260  
- Qwen2.5: 400  
- DeepSeek‑V3: 320  
- Doubao‑1.5‑pro‑32k: 480  
- Moonshot‑v1: 220  

To further validate the above convergence-based sample sizes, we used a Law of Large Numbers (LLN)–based estimation. For each model, we first used the observed accuracies on the sampled configurations to estimated the variance of accuracy, and then computed the minimal sample size required to ensure that the sample mean is within a small error tolerance of the true mean with high probability. This gave the following estimates:

- GPT‑4.1: 170  
- GPT‑3.5: 88  
- Mistral Medium: 229  
- Mistral Large: 253  
- Qwen Plus: 218  
- Qwen2.5: 329  
- DeepSeek‑V3: 285  
- Doubao‑1.5‑pro‑32k: 421  
- Moonshot‑v1: 63  

For every model, the LLN‑estimated minimal sample size is smaller than the sample size returned by the convergence method above. Therefore, we take the largest convergence‑based sample size across models as a baseline and add an additional safety margin, setting a global cap of 500 configurations for MES in Section 5.1, which also helps maintain cross‑model comparability in our evaluation.

# Issue 14: Typographical errors in the paper (Reviewer fLKa weakness 3; Reviewer 6AVH question 1)

In Table 3, the accuracy of gpt3.5 was mistakenly written as 1.1 instead of 0.1, and Figure 4(a) contained a redundant legend. These issues were carefully identified by the reviewers; we have corrected them and re-checked the paper to ensure that similar problems do not remain.

We hope that these clarifications and revisions make the contributions of our work clearer and demonstrate that the reviewers' concerns have been carefully considered and resolved.


