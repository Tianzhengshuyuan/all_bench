Dear Reviewer fLKa, thank you very much for taking the time to carefully review our submission and for your thoughtful and constructive feedback. We are grateful for your recognition that rigorous evaluation of LLMs is important to the community, and for highlighting our analysis of factor attributions as strengths.

At the same time, we very much appreciate your candid comments on the current limitations of our work, including your concerns that the proposed solutions may appear trivial or hand-crafted, the need for more concrete guidance on sampling and variance across seeds, the issues with typos in tables, and the request for broader coverage beyond AIME. These are all valuable points that help us better position and improve our work. Below, we respond to your comments and concerns point by point, and we will incorporate the corresponding clarifications and additional details in the revised version.

# Weakness 1: "The proposed solution seems trivial and handcrafted."

Thank you for raising this concern. Due to space constraints, the main text focused on the high‑level design of A‑MES and may have made the concrete pipeline appear more "handcrafted" than it actually is. 

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

These mechanisms show that A‑MES is not a collection of ad‑hoc, hand‑edited examples, but a unified, automatable framework that systematically augments existing benchmarks to more comprehensively evaluate model capabilities. In practice, for a given benchmark we first use all seven mechanisms to construct a full augmented version of the original workload, producing multiple transformed variants per source item. Among these, numeric substitutions and conditional recomposition may fail for a specific problem (e.g., if no stable solver can be found). During evaluation, for each original workload item we randomly select one of the seven augmentation mechanisms. If the chosen mechanism fails, that specific transformation is simply omitted and the item is evaluated only in its other augmented or original forms. This design keeps the augmentation process both systematic and robust, while avoiding invalid transformed questions. For several major benchmarks, we have already constructed the corresponding augmentation spaces and plan to release them publicly in future work. Below, we provide concrete descriptions of each of the seven mechanisms.


## 1. Analogical‑1: distractor insertion with three well-defined categories

For distractor insertion, we do not rely on ad‑hoc, one‑off edits. Instead, we define three explicit, controllable categories of redundancy and implement all instances via LLM prompting.

We compare several candidate LLMs and select the one that most reliably follows our definitions (GPT‑5). For each target problem to be transformed, we invoke this LLM via API; with our carefully designed prompts, it automatically generates and inserts the corresponding redundant segments. The prompts are specified as follows.

- **Context‑irrelevant redundancy**  
  - Provide the LLM with an example containing an original problem and a version with added context‑irrelevant redundancy.  
  - Instruct the LLM to insert one sentence at a random position that is completely unrelated to the target problem.

- **Context‑relevant, explanatory redundancy**  
  - Provide the LLM with an example of an original problem and a version with added explanatory redundancy.  
  - Instruct the LLM to insert a redundant sentence at a random position in each target problem that explains a concept already appearing in the target problem.

- **Context‑relevant, misleading redundancy**  
  - Provide the LLM with an example containing an original problem and a version with added misleading but logically related redundancy.  
  - Supply the model with the correct answer and several correct solution approaches that are automatically retrieved at run time from online resources (this step is optional; if no such solution approaches can be found, only the correct answer is provided), and instruct it to avoid directly hinting at these correct strategies when crafting the misleading cue.  
  - Instruct the model to insert a redundant sentence that nudges the reader toward an incorrect strategy or line of reasoning, without explicitly revealing that it is "misleading" or "distracting".
  
In practice, the selected LLM produces variations that are more diverse and linguistically natural than manual editing. In particular, its context‑relevant misleading redundancies tend to hint at incorrect heuristics in a more subtle way than hand‑written versions, while still strictly adhering to the predefined category constraints. The entire process involves no per‑item manual editing. The three types of redundancy generated by the above procedure are illustrated as follows:

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

1. We first call an LLM to extract the primary knowledge points tested by the original problem, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
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


# Weakness 2: "More guidance on sample sizes per workload/model and variance across random seeds."

We greatly appreciate this suggestion and agree that practitioners need concrete guidance. In our experiments, we first construct a fixed configuration space with shared randomization across models, and then determine sample sizes using two stopping rules. This procedure was not fully described in the main text and will be elaborated in the revision.

The 10 variables (Language, Question Format, Question Paraphrase, Shot, COT, Multi Turn, temperature, top_p, presence_penalty, max_tokens) define a complete configuration space of size 15,552. We designed a script that enumerates this full 15,552-point space, randomly shuffles the entire set once using a fixed random seed, and then has all models test configurations in exactly the same shuffled order starting from the beginning. This design controls for randomness across models and makes performance comparable.

## Convergence-based stopping rule

For each workload, when testing each model, we evaluate configurations sequentially in batches of 10 from the fixed shuffled list. After every 10 samples, we compute the running mean accuracy and its 95% confidence interval. We stop sampling when both of the following conditions are satisfied:

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

## Variance across random seeds

Because we use a single fixed random seed to generate the global shuffle of the 15,552 configurations and share this ordering across all models, there is no variance arising from different random seeds in our model comparison. This design also makes the experimental results fully reproducible.

In the revised version, we will describe this procedure and the concrete numbers above in more detail.

## Practical guidance for practitioners

To make this concrete for other practitioners, we summarize how one can determine sample sizes and stopping criteria in a new setting, even with a different configuration space or benchmark:

1. **Define and enumerate the configuration space.**  
   - Identify the evaluation variables (analogous to our C1–C10 in Table 2: workload, prompting, decoding, etc.) and specify a finite value range for each.  
   - Enumerate the full Cartesian product of these values to obtain a discrete configuration space. In our case, this yields 15,552 configurations

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
   - After convergence, apply a simple Law of Large Numbers–based estimation, using the variance of the current results to compute how many samples are theoretically required to achieve the desired error tolerance and confidence level, giving an "LLN-based sample size" N_LLN.  
   - If N_LLN is larger than the current N_conv, continue sampling along the same shuffled order until at least N_LLN configurations have been evaluated; otherwise, stop sampling.

The entire evaluation workflow described above is implemented in an automation scripts. After publication, these scripts will be released as open source, so that practitioners can perform evaluation following the guidance with minimal effort.


# Weakness 3: "GPT‑3.5 accuracy appears as 1.10 in Table 3 (typo)."

Thank you for carefully catching this typo; we agree that such inconsistencies can harm the credibility of the results. The correct value for GPT‑3.5's accuracy in Table 3 is 0.1, not 1.10. In addition, we have re-checked all other reported numerical results in the paper and confirmed that there are no further inconsistencies. We will fix this typo in the revised manuscript and also perform a thorough proofread to eliminate similar issues.


# Weakness 4: "The main narrative leans heavily on AIME; more in-depth code/long-context/multi-turn settings would strengthen generality."

We fully agree that including more task types would make the empirical section stronger. At the same time, we would like to clarify that our LLM evaluatology framework is task-agnostic: once we define the set of evaluation variables (C1–C10) and their value ranges, the MES configuration space and the corresponding A‑MES workflows are automatically generated by our tooling. The procedures for random sampling, convergence-based stopping, and ANOVA remain unchanged regardless of whether the benchmark is math (AIME), knowledge (MMLU), science (GPQA), coding, or multi-turn, and in our current experiments we apply this pipeline to AIME, MMLU, and GPQA with no benchmark-specific adaptation or custom engineering, demonstrating that the framework already works out-of-the-box across three different benchmarks. We are actively extending the framework to additional benchmarks, including coding, tool-use, long-context, and more complex multi-turn interactions, following exactly the same methodology. The full automation tooling will be released as open source upon publication.