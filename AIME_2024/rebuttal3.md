Dear Reviewer 5j6t, thank you very much for your careful review of our submission and for the thoughtful comments. We are grateful for your recognition of our problem framing, namely that current evaluations often conflate model ability with configuration, for highlighting the novelty of the MES/A-MES framework as a structured way to specify and vary evaluation conditions, and for your appreciation of our ANOVA-based factor attribution.

We also sincerely appreciate your constructive critiques. Your concerns about the method being more conceptual than algorithmic, the uncertainty about generalization beyond academic reasoning benchmarks, the potential complexity and practical burden for practitioners, the limited human evaluation, and the possibility that our causal language is overstated are all very valuable and will help us clarify and strengthen our work. Below, we respond to your comments and questions point by point, and we will incorporate the corresponding clarifications and additional details in the revised version.

# Response to Weakness 1: "method is conceptual rather than algorithmic"

Due to space limitations, we did not fully explain some aspects of LLM evaluatology in the paper, especially the details of A‑MES. This omission may have made our approach appear more conceptual than algorithmic.

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
  - Instruct the LLM to insert one or more sentences at a random position that are completely unrelated to the target problem.

  Algorithm 1: Context‑Irrelevant Redundancy Insertion

  ```pseudo
  FUNCTION InsertContextIrrelevantDistractor(problem_text):
    EXAMPLE_PAIR ← (orig_example, example_with_irrelevant_context)
    PROMPT ← BuildPromptIrrelevant(EXAMPLE_PAIR, problem_text)
    RESPONSE ← LLM_CALL(PROMPT)
    transformed_text ← ParseTransformedProblem(RESPONSE)
    IF NOT BasicSanityCheck(problem_text, transformed_text):
      RETURN FAILURE
    RETURN transformed_text
  ```

- **Context‑relevant, explanatory redundancy**  
  - Provide the LLM with an example of an original problem and a version with added explanatory redundancy.  
  - Instruct the LLM to insert a redundant sentence at a random position in each target problem that explains a concept already appearing in the target problem.

  Algorithm 2: Context‑relevant Explanatory Redundancy Insertion
   
  ```pseudo
  FUNCTION InsertExplanatoryDistractor(problem_text):
    EXAMPLE_PAIR ← (orig_example, example_with_explanatory_sentence)
    PROMPT ← BuildPromptExplanatory(EXAMPLE_PAIR, problem_text)
    RESPONSE ← LLM_CALL(PROMPT)
    transformed_text ← ParseTransformedProblem(RESPONSE)
    IF NOT BasicSanityCheck(problem_text, transformed_text):
      RETURN FAILURE
    RETURN transformed_text
  ```

- **Context‑relevant, misleading redundancy**  
  - Provide the LLM with an example containing an original problem and a version with added misleading but logically related redundancy.  
  - Supply the model with the correct answer and several correct solution approaches that are automatically retrieved at run time from online resources (this step is optional; if no such solution approaches can be found, only the correct answer is provided), and instruct it to avoid directly hinting at these correct strategies when crafting the misleading cue.  
  - Instruct the model to insert a redundant sentence that nudges the reader toward an incorrect strategy or line of reasoning, without explicitly revealing that it is "misleading" or "distracting".  

  Algorithm 3: Context‑relevant Misleading Redundancy Insertion

  ```pseudo
  FUNCTION InsertMisleadingDistractor(problem_text, answer_gold, solution_sketches):
    EXAMPLE_PAIR ← (orig_example, example_with_misleading_sentence)
    PROMPT ← BuildPromptMisleading(
                example_pair      = EXAMPLE_PAIR,
                target_problem    = problem_text,
                answer_gold       = answer_gold,
                solution_sketches = solution_sketches
               )
    RESPONSE ← LLM_CALL(PROMPT)
    transformed_text ← ParseTransformedProblem(RESPONSE)
    IF NOT BasicSanityCheck(problem_text, transformed_text):
      RETURN FAILURE
    RETURN transformed_text
  ```

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

Algorithm 4: Numeric Substitutions

```pseudo
FUNCTION BuildNumericSolver(problem_text, answer_gold, solution_sketches, max_iter=5, max_refine=5):
  knowledge_points ← LLM_ExtractKnowledgePoints(problem_text)
  retrieved_formulas ← RETRIEVE_FORMULAS(knowledge_points)
  history ← EMPTY_LIST
  FOR iter IN 1..max_iter:
    PROMPT ← BuildPromptCodeGen(problem_text, answer_gold, solution_sketches, retrieved_formulas)
    history.APPEND((PROMPT, None))
    (CODE, value_ranges) ← LLM_CALL(PROMPT)
    is_hard_code ← LLM_HARD_CODE_CHECK(CODE)
    IF is_hard_code:
      CONTINUE
    FOR refine_step IN 0..max_refine:
      (output, error) ← RUN_PYTHON(
                            CODE,
                            input = OriginalNumericInputs(problem_text)
                          )
      history.APPEND((CODE, (output, error)))
      IF error == NONE AND VERIFY(output, answer_gold):
        RETURN (CODE, value_ranges)  
      IF refine_step == max_refine:
        BREAK 
      PROMPT_refine ← BuildPromptCodeRefine(
                              problem_text = problem_text,
                              answer_gold  = answer_gold,
                              history      = history
                        )
      (CODE, value_ranges) ← LLM_CALL(PROMPT_refine)
  RETURN FAILURE

FUNCTION GenerateNumericVariants(problem_text, answer_gold, solution_sketches, K):
  (solver_code, param_ranges) ← BuildNumericSolver(problem_text, answer_gold, solution_sketches)
  IF solver_code == FAILURE:
    RETURN EMPTY_SET
  variants     ← EMPTY_SET
  WHILE |variants| < K:
    new_param ← SAMPLE(param_ranges)
    new_problem_text ← InstantiateNumericProblemText(problem_text, new_param)
    (output, error) ← RUN_PYTHON(solver_code, input = new_params)
    IF error != NONE:
      CONTINUE  
    new_answer_gold ← output
    RETURN (new_problem_text, new_answer_gold)
```

## 3. Analogical‑3: conditional recomposition via invertible‑condition analysis

For conditional recompositions, we again adopt a general and automatable pipeline built around LLM‑generated Python solvers and automatic verification scripts rather than manually rewriting statements:

1. We first call an LLM to extract the primary knowledge points tested by the original problem, and query a pre‑constructed formula library indexed by knowledge point to retrieve potentially relevant formulas.
2. We feed the original problem, its official answer, the retrieved formulas, and (where available) multiple correct solution sketches into the LLM.
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

Algorithm 5: Conditional Recomposition

```pseudo
FUNCTION BuildRecomposedSolver(problem_text, answer_gold, solution_sketches, max_iter=5, max_refine=5):
  knowledge_points ← LLM_ExtractKnowledgePoints(problem_text)
  retrieved_formulas ← RETRIEVE_FORMULAS(knowledge_points)
  history ← EMPTY_LIST
  ANALYSIS_PROMPT ← BuildPromptInvertibleAnalysis(
                           problem_text,
                           answer_gold,
                           solution_sketches,
                           retrieved_formulas
                      )
  ANALYSIS_RESPONSE ← LLM_CALL(ANALYSIS_PROMPT)
  (invertible, cond_as_unknown, target_as_given, recomposed_problem_text) ← ParseInvertibleStructure(ANALYSIS_RESPONSE)
  IF NOT invertible:
    RETURN FAILURE
  FOR iter IN 1..max_iter:
    PROMPT ← BuildPromptRecomposedCodeGen(
                      origin_problem_text = problem_text
                      new_problem_text = recomposed_problem_text,
                      origin_answer_gold = answer_gold,
                      new_answer_gold = cond_as_unknown.original_values,
                      solution_sketches = solution_sketches,
                      retrieved_formulas = retrieved_formulas
                )
    history.APPEND((PROMPT, None))
    (CODE, value_ranges)   ← LLM_CALL(PROMPT)
    is_hard_code ← LLM_HARD_CODE_CHECK(CODE)
    IF is_hard_code:
      CONTINUE
    FOR refine_step IN 0..max_refine:
      (output, error) ← RUN_PYTHON(
                            CODE,
                            input = { target_as_given: answer_gold }
                          )
      history.APPEND((CODE, (output, error)))
      IF error == NONE AND VERIFY(output, cond_as_unknown.original_values):
        RETURN (CODE, cond_as_unknown, target_as_given, value_ranges, recomposed_problem_text)
      IF refine_step == max_refine:
        BREAK
      PROMPT ← BuildPromptRecomposedCodeRefine(
                           problem_text = problem_text,
                           answer_gold  = cond_as_unknown.original_values,
                           history      = history
                        )
      (CODE, value_ranges) ← LLM_CALL(PROMPT)
  RETURN FAILURE

FUNCTION GenerateRecomposedVariants(problem_text, answer_gold, solution_sketches, K):
  (solver_code, cond_as_unknown, target_as_given, value_ranges, recomposed_problem_text) ← BuildRecomposedSolver(problem_text, answer_gold, solution_sketches)
  IF solver_code == FAILURE:
    RETURN EMPTY_SET
  variants ← EMPTY_SET
  WHILE |variants| < K:
    new_param ← SAMPLE(value_ranges)
    new_problem_text ← InstantiateRecomposedProblemText(recomposed_problem_text, new_param)
    (output, error) ← RUN_PYTHON(solver_code, input = { target_as_given: new_param })
    IF error != NONE:
      CONTINUE
    new_answer_gold ← output
    RETURN (new_problem_text, new_answer_gold)
```

## 4. Novel‑1: recent‑source adaptation via structured retrieval and paraphrasing

In the "novel" branch, the first mechanism is recent‑source adaptation, which is also fully scriptable:

1. We first use an LLM to extract the primary knowledge points tested by a given source problem.
2. We query open‑access repositories of centralized exam questions that index items by region, year, subject, and knowledge point, and crawl the most recent 2025 exam problems matching the extracted knowledge points.
3. The retrieved problems are paraphrased by the LLM and can be further transformed using the three analogical methods (redundancy insertion, numeric substitution, and conditional recomposition).

This yields a set of new, recent‑source problems that are structurally aligned at the knowledge level but clearly distinct in surface form and provenance. The entire workflow is driven by scripts and general prompts, without hand‑curating individual items.

Algorithm 6: Recent‑Source Adaptation

```pseudo
FUNCTION RecentSourceAdaptation(problem_text, metadata, K):
  KP_PROMPT   ← BuildPromptExtractKnowledgePoints(problem_text, metadata)
  KP_RESPONSE ← LLM_CALL(KP_PROMPT)
  KPs         ← ParseKnowledgePoints(KP_RESPONSE)
  IF KPs == EMPTY:
    RETURN EMPTY_SET
  year_range ← {2025}
  candidate_item ← RETRIEVE_EXAMS(
                           knowledge_points = KPs,
                           year_range       = year_range,
                           subject          = metadata.subject
                       )
  IF candidate_items == NONE:
    RETURN EMPTY_SET
  adapted_set ← EMPTY_SET
  PARA_PROMPT ← BuildPromptParaphrase(
                           source_text   = candidate_item.text,
                           answer_gold   = candidate_item.answer_gold,
                           preserve_KPs  = KPs
                         )
  PARA_RESPONSE    ← LLM_CALL(PARA_PROMPT)
  paraphrased_item ← ParseParaphrasedProblem(PARA_RESPONSE)
  adapted_item = {
            text : paraphrased_item.text,
            answer : candidate_item.answer_gold,
            KPs : KPs,
            provenance : {
                source_exam :candidate_item.metadata,
                transform   : "paraphrase"
            }
          }
  RETURN adapted_item
```

## 5. Novel‑2: textbook‑based conceptual synthesis via a parsed knowledge base

The second "novel" mechanism is conceptual synthesis from authoritative textbooks. We first crawl a large collection of authoritative textbooks across different subjects from the web, and then use the LLM API's built‑in functionality for parsing local PDF files to extract their content. Based on the extracted content, we build a structured knowledge base in which each concept is associated with definitions, properties, theorems, phenomena, and canonical examples extracted from the textbooks.

1. Given a problem to be augmented, we use an LLM to identify its main knowledge points, and then retrieve the corresponding entries from the structured knowledge base. If the subject‑specific knowledge base is missing, we trigger the textbook crawling and parsing step to expand the knowledge base, and then retrieve the corresponding entries from it.
2. Conditioned on these entries, the LLM is prompted to generate new conceptual questions targeting the underlying knowledge points, rather than copying any existing problem.

For example, one generated question associated with the concept of *logarithms* is: 
> What kind of mathematical idea/method turns exponentiation and multiplication into multiplication and addition?

This pipeline turns textbook content into fresh conceptual questions that align with the original topic but are novel in form and focus.

Algorithm 7: Conceptual Synthesis

```pseudo
FUNCTION ConceptualSynthesis(problem_text, metadata):
  KP_PROMPT   ← BuildPromptExtractKnowledgePoints(problem_text, metadata)
  KP_RESPONSE ← LLM_CALL(KP_PROMPT)
  KPs         ← ParseKnowledgePoints(KP_RESPONSE)
  IF KPs == EMPTY:
    RETURN EMPTY_SET
  kb_entries ← RETRIEVE_KB_ENTRIES(
                 knowkedge_points = KPs
                 subject          = metadata.subject,
               )
  IF kb_entries == EMPTY:
    CRAWL_AND_PARSE_TEXTBOOKS(subject = metadata.subject)
    kb_entries ← RETRIEVE_KB_ENTRIES(
                   knowkedge_points = KPs
                   subject          = metadata.subject,
                 )
    IF kb_entries == EMPTY:
      RETURN EMPTY_SET
  GEN_PROMPT   ← BuildPromptConceptualQuestionGeneration(
                      kb_entries = kb_entries,
                      KPs        = KPs,
                 )
  GEN_RESPONSE ← LLM_CALL(GEN_PROMPT)
  raw_item     ← ParseGeneratedConceptualQuestions(GEN_RESPONSE)
  conceptual_item = {
            text       : raw_item.text,
            answer     : raw_item.answer,
            KPs        : KPs
          }
  RETURN conceptual_item
```

--- 

Taken together, we effectively have seven concrete augmentation mechanisms for each workload item:

1. Context‑irrelevant distractor insertion
2. Context‑relevant explanatory distractor insertion
3. Context‑relevant misleading distractor insertion
4. Numeric substitutions
5. Conditional recomposition
6. Recent‑source adaptation
7. Conceptual synthesis

These mechanisms show that our method is not merely a high‑level conceptual proposal. A‑MES is realized as a concrete, fully automated workflow with fixed prompts, scripted control logic, programmatic verification, and data‑driven retrieval and synthesis. 

Among these, numeric substitutions and conditional recomposition may fail for a specific problem (e.g., if no stable solver can be found). In constructing A‑MES, for each original workload item we randomly select one of the seven augmentation strategies. If the chosen strategy fails, we simply do not apply that strategy to this item and instead keep the item only in its other augmented or original forms. This design keeps the augmentation process both systematic and robust, while avoiding invalid transformed questions.

In the revised version, we will add a concise algorithmic overview summarizing this implementation, so that the algorithmic nature and reproducibility of LLM evaluatology are made explicit.

# Response to Weakness 2: "unclear if this generalizes beyond academic reasoning benchmarks"

Our methodology is not limited to public academic benchmarks and naturally extends to non‑benchmark settings. As long as there exists a seed workload—such as an enterprise’s internal question bank, a school or institutional exam repository, or other custom task collections—our MES/A‑MES pipeline can be instantiated on top of it without any conceptual change. In this view, the internal or proprietary workload simply serves as the workload component in our framework; our tooling then automatically constructs the corresponding configuration space, performs workload augmentation, and runs the same sampling and attribution procedures. This enables organizations to obtain causally interpretable, system‑level evaluations tailored to their own private or domain‑specific tasks, rather than being restricted to public academic reasoning benchmarks.

Existing reasoning benchmarks are typically defined as a fixed workload (a set of questions) plus scoring rules, with many indispensable components left underspecified, such as prompting, decoding, and system configuration.  In contrast, our LLM evaluatology explicitly treats a benchmark not as "a dataset with a number", but as a full evaluation system: we jointly consider (i) the evaluation object (an LLM or an LLM-based service), and (ii) a bundle of evaluation conditions, including the workload, the prompting method, and the decoding parameters. From this perspective, an academic reasoning benchmark like AIME, under a single default configuration, is just one point in a much larger configuration space (EC). Our contribution is to make this space explicit and controlled, systematically augment it in a semantically meaningful way, and attribute performance differences to specific components, rather than reporting a single score. Thus, our proposal is not "one more reasoning benchmark", but a general recipe for turning LLM evaluation into a causally interpretable system-level benchmark. 

Furthermore, our method is in fact fully generalizable. Specifically, we would like to clarify that our LLM evaluatology framework is task‑agnostic: once we define the set of evaluation variables (C1–C10) and their value ranges, the MES configuration space and the corresponding A‑MES workflows are automatically generated by our tooling. The procedures for random sampling, convergence‑based stopping, and ANOVA remain unchanged regardless of whether the benchmark is reasoning(AIME), knowledge (MMLU), science (GPQA), coding, or multi‑turn, and in our current experiments we apply this pipeline to AIME, MMLU, and GPQA with no benchmark‑specific adaptation or custom engineering, demonstrating that the framework already works out‑of‑the‑box across three different benchmarks. We are actively extending the framework to additional benchmarks, including coding, tool‑use, long‑context, and more complex multi‑turn interactions, following exactly the same methodology.

# Response to Weakness 3: "complexity and practical burden on practitioners might be too high; unclear scalability"

We understand the concern that our evaluatology framework may appear complex and potentially burdensome for practitioners. Our view is that:

1. The cost is higher than a single‑number leaderboard evaluation, but this is intrinsic to doing serious attribution, not an artifact of our specific design;  
2. We explicitly control and reduce this cost via sampling;
3. The resulting insights further lower the cost of future runs.

## 1. Why some additional cost is unavoidable but justified

Existing practice typically measures a small set of metrics under a single, fixed evaluation configuration. This is cheap, but provides almost no attribution: it is impossible to tell whether performance changes come from question format, prompting methods, decoding parameters or other factors. 

Our MES/A‑MES framework makes this attribution explicit: we define C1–C10 as a set of interpretable evaluation dimensions, generate controlled variants, and apply ANOVA to quantify effect sizes. This incurs additional evaluation cost compared to a normal benchmark run, but it is precisely what enables the insights that standard evaluations cannot provide (e.g., which variables dominate performance, where robustness breaks, how different models differ in sensitivity).

## 2. How we control cost in practice

Importantly, the framework is not a combinatorial grid search over all possible MES configurations; instead, we randomly sample configurations from the MES space and use a stopping criterion grounded in convergence and law of large numbers to decide when we have enough data, so the total number of evaluated configurations (and thus cost) is explicitly bounded and controllable. In practice, our experiments show that a moderate number of sampled configurations suffices to obtain stable variable‑importance rankings, i.e., we do not need to exhaustively explore the full Cartesian product of all C‑variables.

## 3. Our empirical results provide actionable cost‑reduction for future users

Crucially, the evaluatology analysis itself tells practitioners which variables matter most, which directly lowers the practical burden in subsequent use. We find that Question Format and max\_tokens have the largest effect sizes, while several other dimensions (e.g., presence_penalty) have comparatively minor impact on performance. This implies that, for many practical purposes, users who only need coarse evaluatology can fix or omit low‑impact variables and focus evaluation budget on the small subset of high‑impact factors.

Concretely, a practitioner could vary question format and max\_tokens across a few sampled configurations, hold other low‑impact C‑variables at default values, and still obtain the majority of the insight at a fraction of the full experimental cost. In other words, the first full evaluatology run is more expensive, but it yields a compressed, prioritized view of the evaluation space that can be used to design lighter‑weight, task‑tailored evaluatology protocols afterward.

## 4. Scalability and tooling for practitioners

Finally, the complexity is largely centralized in our tooling, not in per‑user engineering: once the evaluation variables and their ranges are specified, MES configurations are sampled automatically, A‑MES transformations are script‑driven, and ANOVA is applied by standard statistical libraries, so practitioners do not need to hand‑craft transformations or write custom code for each benchmark instance; they only choose (i) which C‑variables to include and what value ranges to use for them, and (ii) how much evaluation budget they are willing to spend.


# Response to Weakness 4: "limited human evaluations --> maybe human ablation could be added"

Our current experiments focus on tasks with objective ground-truth answers (e.g., AIME, MMLU, GPQA). Even after A‑MES transformations, we explicitly ensure that each item still has a well-defined, automatically checkable correct answer. Under this setting, human judgments are, in principle, expected to align closely with the ground truth, so large‑scale human evaluation or human ablation would add relatively little information beyond what is already captured by automatic grading scripts.

We fully agree that human ablation studies are very valuable, especially for open‑ended or subjective tasks, where human evaluation is essential for assessing output quality, error types, and nuanced behavior that cannot be reduced to a single correct answer. In ongoing follow‑up work on open‑ended question evaluation, we are planning to adopt exactly this strategy: sampling outputs under different MES/A‑MES configurations and having human annotators (experts or crowd workers) provide detailed judgments, then comparing these with automatic metrics and ANOVA‑based importance analyses.

# Response to Weakness 5: "causal language might be overstated"

Thank you for raising this point. Our "causal" contribution lies in how we structure and use the evaluation system: we build MES and A‑MES, explicitly model key evaluation components as controllable conditions, and then apply ANOVA over systematically sampled configurations to attribute observed performance differences to specific factors.

Existing LLM evaluations do not emphasize the notion of attribution and tend to overlook the impact of confounding factors. In practice, the observed accuracy depends on workload format, prompt methods, decoding parameters, and even system‑level factors. However, current benchmarks typically do not ask whether the measured accuracy is due to the model itself or to these confounders. We make this attribution question explicit and place it at the center of our evaluation design.

To the best of our knowledge, existing work considers at most three factors that affect LLM output accuracy (e.g., output format, prompt style, knowledge domain). In contrast, we are the first to explicitly define a minimal evaluation system that covers factors at different levels (10 in total), and to sample and test within the resulting configuration space, quantifying how much variance each factor and their interactions explain. We will also treat the exploration of richer causal methodologies as future work, and clearly position this as an open direction rather than a completed contribution.

If we have correctly understood your concern in the review, we will make our position on "causal" contributions more precise in the revised version. Looking forward to your feedback.

# Response to Question 1: "Which parts of A-MES generation are automated and which require expert authoring? How would scalability be possible?"

Regarding "Which parts of A‑MES generation are automated and which require expert authoring? How would scalability be possible?", the detailed automation pipeline of A‑MES has already been described in our response to Weakness 1, and its scalability is discussed in our response to Weakness 2.

In brief:

- Automation

  As detailed under Weakness 1, A‑MES is instantiated as a set of script‑driven pipelines (three analogical and two novel branches), all of which are executed automatically via:
  - fixed, reusable prompts and scaffolding,
  - LLM API calls,
  - programmatic verification,
  - and retrieval from external repositories or parsed textbooks.
  There is no per‑item manual authoring or hand‑crafting of individual problems. Once the original workload is given, the augmentation is "one‑click": the scripts generate all A‑MES instances end‑to‑end.

- Scalability

  As described under Weakness 2, the framework is fully generalizable in the sense that:
  - The MES variables (C1–C10) and their ranges are defined once, and the MES/A‑MES configuration space is generated automatically.
  - The sampling, convergence‑based stopping rule, and ANOVA‑based analysis are identical across benchmarks.
  - In our experiments, the same implementation runs unchanged on AIME (math reasoning), MMLU (broad knowledge), and GPQA (scientific reasoning), without any benchmark‑specific engineering.  
  We are currently extending the same pipelines to coding, tool‑use, multi-turn and long‑context settings, again without changing the core methodology.


# Response to Question 2: "DO you expect ANOVA factor importance to generalize across models and tasks, or is it benchmark-specific?"

Our empirical results indicate that ANOVA‑based factor importance exhibits both cross‑benchmark regularities and benchmark‑specific characteristics.

On the regularity side, some factors consistently emerge as highly influential across models and benchmarks. For example, in all the benchmarks we analyzed, both Question Format and COT have large and statistically significant effects on accuracy. This suggests that these factors are not idiosyncratic to a single dataset, but rather reflect general sensitivities of current LLMs to how questions are formatted and whether reasoning is explicitly elicited.

On the benchmark‑specific side, we also observe clear differences. A salient example is Question Paraphrase: on AIME, Question Paraphrase has negligible effect, indicating that paraphrasing difficult math problems does not reliably change model accuracy; in contrast, on MMLU, paraphrasing often becomes a key factor— for several models, Question Paraphrase reach statistical significance and explain a non‑trivial share of variance. 

In ongoing work, we are extending the ANOVA analysis to more tasks and models to more systematically characterize which factors generalize and which are dataset‑dependent. We will update the paper with these expanded results as soon as they are ready.

# Response to Question 3: "How should practitioners choose a single evaluations core after MES/A-MES exploration? What is the summary statistic?"

This is a very valuable question, and we realize we did not make this part sufficiently explicit in the paper. After exploring MES and A‑MES, practitioners will ultimately need a single evaluation score per model. In our framework this is handled in a statistical way.

For MES, the 10 variables together define a finite configuration space of size 15,552. We enumerate this full space once, apply a single random shuffle with a fixed seed, and then let all models evaluate configurations in exactly the same shuffled order. 

In A‑MES, for each workload item we randomly sample exactly one augmentation method from our pool of augmentation strategies. Since this sampling space also includes the original MES formulation, the sampled instance for a given item may still be the original MES problem.

To obtain a stable single score per model without evaluating all configurations and augmented variants, we use a convergence‑based sampling procedure. For each workload and each model, we test configurations sequentially in batches of 10 from this shuffled list. After each batch, we recompute the running mean accuracy and its 95% confidence interval, and stop when (i) the differences between the last four mean accuracies are all smaller than 0.002, and (ii) the 95% confidence interval length is below 0.06. The resulting sample sizes are further checked by a simple Law of Large Numbers (LLN)–based calculation. 

Based on this, the single evaluation score we report for each model on A‑MES is the mean performance over all sampled instances, together with its 95% and 99% confidence intervals.