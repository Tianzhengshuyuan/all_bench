Dear Reviewer MRzL, thank you for carefully reviewing our submission and providing detailed, constructive feedback. We appreciate your recognition of our work’s originality, particularly our definition of ten evaluation dimensions, as well as your positive comments on our experiments, presentation, and the importance of moving beyond single-setting evaluations. We also value your critiques, including requests for more details on workload augmentation, concerns about the use of ANOVA in supporting causal claims, and questions on specific design choices. We address each point below and will incorporate the corresponding clarifications in the revised version.

# Response to Weakness 1: Limited details on the implementation of workload augmentation

Due to space limitations, we only briefly outlined the A-MES part in the submission. Below, we provide a more detailed description of this implementation and will incorporate these clarifications and examples into the revised version.

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

These mechanisms show that A‑MES is not a collection of ad‑hoc, hand‑edited examples, but a unified, automatable framework that systematically augments existing benchmarks to more comprehensively evaluate model capabilities. For each question within a benchmark, we first apply all seven mechanisms to construct the full space of augmented variants, filtering out transformation attempts that fail (e.g., numeric substitutions without a stable solver). Evaluation then samples directly from this augmentation space, ensuring that no invalid transformations are ever selected. The framework enumerates the entire augmentation space upfront, and the small number of discarded variants has negligible impact on overall coverage or robustness. For several major benchmarks, we have already constructed the corresponding augmentation spaces and plan to release them publicly in future work. Below, we provide concrete descriptions of the seven mechanisms.

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


# Response to Weakness 2: Use of the term "causal" for our attribution method

Thank you for raising this point. While our paper does not introduce new causal inference methods, it contributes a systematic approach to uncovering causal relationships in complex LLM evaluation systems. Specifically, we construct a minimal evaluation system (MES and A‑MES) that explicitly defines the essential components of evaluation and systematically controls them. This allows us to attribute observed performance differences to specific factors and their interactions, addressing the core challenge that in complex systems “everyone is a stakeholder.”

Existing LLM evaluations rarely focus on attribution and often overlook confounding factors such as workload format, prompt design, decoding parameters, or system-level effects. By explicitly incorporating these factors and systematically sampling the resulting configuration space, our approach quantifies how much variance each factor explains, making the attribution question central to the evaluation.

To our knowledge, we are the first to define a minimal evaluation system covering 10 key factors and to systematically analyze their contributions to LLM output variance. While the development of new causal inference methods remains an important direction, our work makes a foundational contribution by providing a systematic approach to characterize true causal effects and accurately attribute performance differences in complex LLM evaluation systems. Beyond technical implementation, this framework establishes a principled methodology that moves LLM evaluation beyond single-setting snapshots, enabling more interpretable, reproducible, and comprehensive assessments across diverse conditions.


# Response to Question 1: Implementation of analogical transformations in A‑MES

Thank you for this detailed question. We provided a detailed description of the implementation of the analogical transformation workloads in our response to Weakness 1. We use a systematic and scalable procedure to construct analogical transformation workloads, rather than ad‑hoc editing. All transformed workloads are generated by script‑driven pipelines, so that the process scales to large benchmarks without per‑item manual rewriting.

Actually, we separately examined context‑relevant and context‑irrelevant redundancy and found an interesting pattern: context‑irrelevant redundancy tends to cause the largest drop in model accuracy, whereas even deliberately misleading context‑relevant redundancy has a smaller impact on accuracy than context‑irrelevant noise.

Regarding "swapping problem statements and conditions", we agree with your concern: naively swapping the question and a condition can render a math problem invalid or ill‑posed. As we noted when describing the construction of A‑MES, we effectively have seven concrete augmentation mechanisms for each workload item:

1. Distractor InsertionContext‑irrelevant distractor insertion
  - Context‑irrelevant distractor insertion
  - Context‑relevant explanatory distractor insertion
  - Context‑relevant misleading distractor insertion
2. Numeric substitutions
3. Conditional recomposition
4. Recent‑source adaptation
5. Conceptual synthesis

For each question within a benchmark, we first apply all seven mechanisms to construct the full space of augmented variants, filtering out transformation attempts that fail. Evaluation then samples directly from this augmentation space, ensuring that no invalid transformations are ever selected. Therefore, the small number of discarded invalid variants (e.g., certain conditional recompositions) has negligible impact on overall coverage or robustness.

# Response to Question 2: Implementation of novel workloads in A‑MES

Thank you for this question. The concrete procedures for both recent‑source adaptation and conceptual synthesis are detailed in our response to Weakness 1, where we describe how they fit into the broader A‑MES construction pipeline.

Regarding your concerns about recent‑source adaptation, we clarify as follows. First, recent‑source adaptation is only one branch of our augmentation design; it is complemented by conceptual synthesis and the analogical transformations. Together, these seven mechanisms form a systematic augmentation methodology. In addition, the MES framework itself also provides a rich configuration space. This structured design goes beyond simply refreshing items over time, and is not present in existing dynamic benchmarks such as LiveCodeBench.

Second, for recent‑source adaptation, our goal is not only to "harvest new questions", but to systematically align them to specific knowledge points of our base workloads, and then optionally apply the analogical pipelines on top. This gives us knowledge‑controlled novelty, rather than a generic continuously updated pool.

Regarding conceptual synthesis, we do not ask the LLM to generate arbitrary new questions and answers. Instead, the generation process is grounded in authoritative textbooks: we parse standard textbooks into a structured knowledge base, retrieve the relevant entries for a knowledge points corresponding to a given workload item, and strictly constrain the LLM's generation to these vetted materials when producing conceptual questions. This grounding in authoritative sources significantly improves the reliability of the generated (question, answer) pairs compared with unconstrained LLM generation. In other words, our conceptual synthesis is not free‑form generation "out of thin air", but a controlled transformation of trusted textbook content, which is precisely how we ensure that the resulting questions are well‑posed and their answers correct.


# Response to Question 3: Binary coding of "Question Paraphrase" in Table 2

The "Question Paraphrase" column in Table 2 is binary by design, which does not imply that there is only a single way to paraphrase a question. The binary flag distinguishes two regimes:

- No (original): the original question text is used, which may appear in a model's training data.
- Yes (paraphrased): the question is restated in different wording while preserving all underlying semantics, answers, numerical values, and natural language constraints, avoiding potential data‑contamination issues.

To construct paraphrases, we first compare several candidate LLMs on a small validation set and select the one that reliably follows these constraints. This model is then instructed to restate each question, ensuring semantic equivalence while changing surface wording. The purpose of this binary indicator is to diagnose memorization and data‑contamination effects: comparing model performance on original versus paraphrased items reveals whether behavior is robust to rewording or overly tied to specific training instances. The specific paraphrasing strategy or number of rewrites is irrelevant for this goal.

Within MES, all workload transformations—including Question Paraphrase—preserve intrinsic semantics, providing alternative surface realizations of the same task. By contrast, A‑MES analogical transformations (distractor insertion, numeric substitution, condition recomposition) alter problem structure while maintaining core reasoning patterns, producing a family of structurally varied, more challenging variants.Therefore, keeping Question Paraphrase as a binary indicator cleanly separates same‑semantics rewording from the structural, changed‑semantics regime in A‑MES, aligning the design with our evaluation objectives.


# Response to Question 4: Sufficiency of 500 random samples

Thank you for raising this concern. For each benchmark, we first construct a configuration space of 15,552 distinct settings defined by ten controllable variables (e.g., Language, Question Format, Question Paraphrase, Shot, Chain-of-Thought, Multi-Turn, temperature, top_p, presence_penalty, and max_tokens). We then generate workload-level variants for each setting using the seven augmentation mechanisms, producing a ~100,000-point configuration space. To implement random sampling while ensuring reproducibility and consistency across model evaluations, we randomly shuffle the diverse settings using a random seed to form a list and select the first <sample_size> configurations.

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

