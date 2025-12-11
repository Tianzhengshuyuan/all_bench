Dear Reviewer MRzL, thank you very much for your careful reading of our submission and for providing such detailed and constructive feedback. We sincerely appreciate your recognition of the originality of our work, especially our definition of 10 important dimensions for evaluation settings to make evaluation more systematic, as well as your positive comments on the quality of our experimental study, the clarity of the presentation, and the importance of going beyond single-setting evaluations.

At the same time, we are grateful for your thoughtful critiques. In particular, your request for more concrete details on workload augmentation, your concern that our use of ANOVA may not fully justify the paper’s claimed contribution to "causal methods", and your questions about specific design choices are all very valuable and will help us clarify and strengthen the paper. Below, we respond to your comments and concerns point by point, and we will incorporate the corresponding clarifications and additional details in the revised version.

# Response to Weakness 1: Limited details on the implementation of workload augmentation

Due to space limitations, we only briefly outlined the A-MES part in the submission. Below, we provide a more detailed description of this implementation and will incorporate these clarifications and examples into the revised version.

In our implementation, A‑MES is instantiated as five systematically defined, script‑driven transformation pipelines—three analogical (distractor insertion, numeric substitution, conditional recomposition) and two novel (recent‑source adaptation and conceptual synthesis). For each pipeline, we fix general prompts and scaffolding, and then run the entire process automatically through LLM API calls (e.g., GPT‑5), lightweight verification scripts and other auxiliary tooling. This setup scales to large workloads and produces diverse variants, without any per‑item manual rewriting or hand‑crafting of individual problems. Moreover, we are actively exploring additional automated AIME‑style transformation pipelines to further enrich A‑MES.

Overall, these five transformation pipelines realize seven concrete augmentation mechanisms for each workload item:
1. Distractor Insertion
   - Context‑irrelevant distractor insertion
   - Context‑relevant explanatory distractor insertion
   - Context‑relevant misleading distractor insertion
2. Numeric substitutions
3. Conditional recomposition
4. Recent‑source adaptation
5. Conceptual synthesis

These mechanisms show that A‑MES is not a collection of ad‑hoc, hand‑edited examples, but a unified, automatable framework that systematically augments existing benchmarks to more comprehensively evaluate model capabilities. In practice, for a given benchmark we first use all seven mechanisms to construct a full augmented version of the original workload, producing multiple transformed variants per source item. Among these, numeric substitutions and conditional recomposition may fail for a specific problem (e.g., if no stable solver can be found). During evaluation, for each original workload item we randomly select one of the seven augmentation mechanisms. If the chosen mechanism fails, that specific transformation is simply omitted and the item is evaluated only in its other augmented or original forms. This design keeps the augmentation process both systematic and robust, while avoiding invalid transformed questions. For several major benchmarks, we have already constructed the corresponding augmentation spaces and plan to release them publicly in future work. We next provide concrete descriptions of each of the seven mechanisms.


## 1. Analogical‑1: distractor insertion with three well-defined categories

For distractor insertion, we do not rely on ad‑hoc, one‑off edits. Instead, we define three explicit, controllable categories of redundancy and implement all instances via LLM prompting.

We compare several candidate LLMs and select the one that most reliably follows our definitions (GPT‑5). For each target problem to be transformed, we invoke this LLM via API; with our carefully designed prompts, it automatically generates and inserts the corresponding redundant segments. The prompts are specified as follows.

- **Context‑irrelevant redundancy**  
  - Provide the LLM with an example containing an original problem and a version with added context‑irrelevant redundancy.  
  - Instruct the LLM to insert one or more sentences at a random position that are completely unrelated to the target problem.

- **Context‑relevant, explanatory redundancy**  
  - Provide the LLM with an example of an original problem and a version with added explanatory redundancy.  
  - Instruct the LLM to insert a redundant sentence at a random position in each target problem that explains a concept already appearing in the target problem.

- **Context‑relevant, misleading redundancy**  
  - Provide the LLM with an example containing an original problem and a version with added misleading but logically related redundancy.  
  - Supply the model with the correct answer and several correct solution approaches that are automatically retrieved at run time from online resources (this step is optional; if no such solution approaches can be found, only the correct answer is provided), and instruct it to avoid directly hinting at these correct strategies when crafting the misleading cue.  
  - Instruct the model to insert a redundant sentence that nudges the reader toward an incorrect strategy or line of reasoning, without explicitly revealing that it is "misleading" or "distracting".
  
In practice, the selected LLM produces variations that are more diverse and linguistically natural than manual editing. In particular, its context‑relevant misleading redundancies tend to hint at incorrect heuristics in a more subtle way than hand‑written versions, while still strictly adhering to the predefined category constraints. The entire process involves no per‑item manual editing. The three types of redundancy generated by the above procedure are illustrated as follows:

1. Context‑irrelevant redundancy example:
   > *The weather today seems quite pleasant, and it might be a great day for a picnic.* Find the number of triples of nonnegative integers $(a,b,c)$ satisfying $a + b + c = 300$ and \[a^2b + a^2c + b^2a + b^2c + c^2a + c^2b = 6,000,000.\] *Also, there are some beautiful flowers blooming in the nearby park.*

   Here, weather and flowers are entirely unrelated to the math content.

2. Context‑relevant, explanatory redundancy example:
   > There exist real numbers $x$ and $y$, both greater than 1, such that $\log_x\left(y^x\right)=\log_y\left(x^{4y}\right)=10$. *A logarithm is a way to express how many times a base must be multiplied by itself to get a certain number*. Find $xy$.

   The added sentence explains the notion of a logarithm while leaving the underlying problem unchanged.

3. Context‑relevant, misleading redundancy example:
   > Alice and Bob play the following game. A stack of $n$ tokens lies before them. The players take turns with Alice going first. On each turn, the player removes either $1$ token or $4$ tokens from the stack. *Many players adopt a greedy approach here: always take $4$ whenever possible to shorten the game and restrict the opponent's replies.* Whoever removes the last token wins. Find the number of positive integers $n$ less than or equal to $2024$ for which there exists a strategy for Bob that guarantees that Bob will win the game regardless of Alice's play.

    The extra sentence about the "greedy approach" is logically related to the game but suggests a flawed strategy, intentionally nudging the solver toward an incorrect line of reasoning  


## 2. Analogical‑2: numeric substitutions via code‑based solution extraction

For numeric substitutions, we use a uniform pipeline built around LLM‑generated Python solvers and automatic verification scripts, rather than manually changing a few numbers:

1. We first call an LLM to extract the primary knowledge points tested by the original problem, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
2. We feed the original problem, its official answer, the retrieved formulas, and (where available) multiple correct solution sketches into the LLM.
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

1. We first call an LLM to extract the primary knowledge points tested by the original problem, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
2. m, its official answer, the retrieved formulas, and (where available) multiple correct solution sketches into the LLM.
3. The LLM is prompted to:
   - identify the key conditions and the target quantity;
   - determine whether some of these conditions and the target can be interchanged—i.e., whether knowing the original answer allows us to infer some of the original conditions (an invertible relationship).
4. When such an invertible relationship exists, the LLM is asked to write a Python solution program for the recomposed problem, where the original target now appears as an input condition and (a subset of) the original conditions become the new target.
5. We then ask another LLM to inspect the generated Python code and verify that it implements a general computational procedure for solving the problem, rather than relying on hard‑coded instance‑specific outputs or trivial pattern matching.
6. We import the LLM‑generated Python code as a local module and call its solve() function, plugging the original answer value into the new "condition" slot and checking whether the returned output correctly recovers the original condition values.
7. Any discrepancy or runtime error is fed back to the LLM for iterative refinement, just as in the numeric substitutions pipeline.

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

The second "novel" mechanism is conceptual synthesis from authoritative textbooks. We parse digital versions of standard textbooks across different subjects to build a structured knowledge base, where each concept is associated with definitions, properties, theorems, phenomena, and canonical examples extracted from the text.

1. Given a problem to be augmented, we use an LLM to identify its main knowledge points, and then retrieve the corresponding entries from the structured knowledge base. If the subject‑specific knowledge base is missing, we trigger the textbook crawling and parsing step to expand the knowledge base, and then retrieve the corresponding entries from it.
2. Conditioned on these entries, the LLM is prompted to generate new conceptual questions targeting the underlying knowledge points, rather than copying any existing problem.

For example, one generated question associated with the concept of *logarithms* is: 
> What kind of mathematical idea/method turns exponentiation and multiplication into multiplication and addition?

This pipeline turns textbook content into fresh conceptual questions that align with the original topic but are novel in form and focus.


# Response to Weakness 2: Use of the term "causal" for our attribution method

Thank you for raising this point. Our "causal" contribution lies in how we structure and use the evaluation system: we build MES and A‑MES, explicitly model key evaluation components as controllable conditions, and then apply ANOVA over systematically sampled configurations to attribute observed performance differences to specific factors.

Existing LLM evaluations do not emphasize the notion of attribution and tend to overlook the impact of confounding factors. In practice, the observed accuracy depends on workload format, prompt methods, decoding parameters, and even system‑level factors. However, current benchmarks typically do not ask whether the measured accuracy is due to the model itself or to these confounders. We make this attribution question explicit and place it at the center of our evaluation design.

To the best of our knowledge, existing work considers at most three factors that affect LLM output accuracy (e.g., output format, prompt style, knowledge domain). In contrast, we are the first to explicitly define a minimal evaluation system that covers factors at different levels (10 in total), and to sample and test within the resulting configuration space, quantifying how much variance each factor and their interactions explain. We will also treat the exploration of richer causal methodologies as future work, and clearly position this as an open direction rather than a completed contribution.

Existing LLM evaluations do not emphasize the notion of attribution and tend to overlook the impact of confounding factors. In practice, the observed accuracy depends on workload format, prompt methods, decoding parameters, and even system‑level factors. However, current benchmarks typically do not ask whether the measured accuracy is due to the model itself or to these confounders. We make this attribution question explicit and place it at the center of our evaluation design.

To the best of our knowledge, existing work considers at most three factors that affect LLM output accuracy (e.g., output format, prompt style, knowledge domain). In contrast, we are the first to explicitly define a minimal evaluation system that covers factors at different levels (10 in total), and to sample and test within the resulting configuration space, quantifying how much variance each factor and their interactions explain. We will also treat the exploration of richer causal methodologies as future work, and clearly position this as an open direction rather than a completed contribution.

# Response to Question 1: Implementation of analogical transformations in A‑MES

Thank you for this detailed question. We do use a systematic and scalable procedure to construct analogical (Transformed) workloads, rather than ad‑hoc editing. As outlined in our response to Weakness 1, all transformed workloads are generated by script‑driven pipelines, so that the process scales to large benchmarks without per‑item manual rewriting.

Actually, we separately examined context‑relevant and context‑irrelevant redundancy and found an interesting pattern: context‑irrelevant redundancy tends to cause the largest drop in model accuracy, whereas even deliberately misleading context‑relevant redundancy has a smaller impact on accuracy than context‑irrelevant noise.

Regarding "swapping problem statements and conditions", we agree with your concern: naively swapping the question and a condition can easily render a math problem invalid or ill‑posed. As we noted when describing the construction of A‑MES, we effectively have seven concrete augmentation mechanisms for each workload item:

1. Context‑irrelevant distractor insertion
2. Context‑relevant explanatory distractor insertion
3. Context‑relevant misleading distractor insertion
4. Numeric substitutions
5. Conditional recomposition
6. Recent‑source adaptation
7. Conceptual synthesis

Among these, numeric substitutions and conditional recomposition may fail for a specific problem (e.g., if no stable solver can be found). In constructing A‑MES, for each original workload item we randomly select one of the seven augmentation strategies. If the chosen strategy fails, we simply do not apply that strategy to this item and instead keep the item only in its other augmented or original forms. This design keeps the augmentation process both systematic and robust, while avoiding invalid transformed questions.

# Response to Question 2: Implementation of novel workloads in A‑MES

Thank you for this question. The concrete procedures for both recent‑source adaptation and conceptual synthesis are detailed in our response to Weakness 1, where we describe how they fit into the broader A‑MES construction pipeline.

Regarding your concerns about recent‑source adaptation, we clarify as follows. First, recent‑source adaptation is only one branch of our augmentation design; it is complemented by conceptual synthesis and the analogical transformations. Together, these seven mechanisms form a systematic augmentation methodology. In addition, the MES framework itself also provides a rich configuration space. This structured design goes beyond simply refreshing items over time, and is not present in existing dynamic benchmarks such as LiveCodeBench.

Second, for recent‑source adaptation, our goal is not only to "harvest new questions", but to systematically align them to specific knowledge points of our base workloads, and then optionally apply the analogical pipelines on top. This gives us knowledge‑controlled novelty, rather than a generic continuously updated pool.

Regarding conceptual synthesis, we do not ask the LLM to generate arbitrary new questions and answers. Instead, the generation process is grounded in authoritative textbooks: we parse standard textbooks into a structured knowledge base, retrieve the relevant entries for a given workload item, and strictly constrain the LLM's generation to these vetted materials when producing conceptual questions. This grounding in authoritative sources significantly improves the reliability of the generated (question, answer) pairs compared with unconstrained LLM generation. In other words, our conceptual synthesis is not free‑form generation "out of thin air", but a controlled transformation of trusted textbook content, which is precisely how we ensure that the resulting questions are well‑posed and their answers correct.


# Response to Question 3: Binary coding of "Question Paraphrase" in Table 2

In Table 2, the "Question Paraphrase" column is indeed binary by design, but this does not mean we assume there is only a single way to paraphrase a question. Our intention there is to distinguish two regimes:

- No (non‑paraphrased): the original question text is used. This version may plausibly appear in a model's training data.
- Yes (paraphrased): the surface form of the question has been rewritten while preserving exactly the same underlying semantics, so that we can effectively avoid data‑contamination issues associated with reusing the original wording.

Concretely, to construct paraphrased questions, we first compare several candidate LLMs on a small validation set and select the model that most reliably follows our paraphrasing constraints. We then instruct this model to restate each question in different wording while keeping the problem’s meaning, answer, numerical values, and natural language strictly unchanged. This ensures that the paraphrased and original items are semantically equivalent, differing only in surface form.

The purpose of this binary flag is to diagnose data‑contamination and memorization effects: by comparing performance on original versus paraphrased versions of the same item, we can assess whether a model's behavior is robust to rewording or overly tied to specific training instances, and for this goal we only need to know whether paraphrasing has been applied, not which specific paraphrasing strategy or how many alternative rewrites exist.

Within MES, the three transformation types in the workload (including Question Paraphrase) are all designed so that the intrinsic semantics of the problem remain unchanged—they provide different surface realizations of the same underlying task. By contrast, in A‑MES, the analogical transformations perform a deeper reworking of the original problem structure through distractor insertion, numeric substitutions, and condition recomposition. These operations preserve the core reasoning pattern but turn each original item into a family of more challenging, structurally varied variants rather than mere paraphrases.

Therefore, we keep "Question Paraphrase" as a binary indicator that marks whether we are in the same‑semantics, different‑wording regime used to probe contamination and robustness, as opposed to the changed‑semantics regime of analogical augmentations in A‑MES, which is analyzed separately.

# Response to Question 4: Sufficiency of 500 random samples

Our full configuration space contains 15,552 combinations, and we sample 500 configurations from this space. This sample size choice is not arbitrary: we first determine per‑model sample sizes using an explicit convergence procedure, and then additionally validate them with an LLN‑based calculation. The final "500" threshold is thus a conservative upper cap backed by two independent criteria rather than a heuristic guess.

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