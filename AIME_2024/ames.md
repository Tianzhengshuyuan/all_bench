In our implementation, A‑MES is instantiated as five systematically defined, script‑driven transformation pipelines including: three analogical (distractor insertion, numeric substitution, conditional recomposition) and two novel (recent‑source adaptation and conceptual synthesis). For each pipeline, we fix general prompts and scaffolding, and then run the entire process automatically through LLM API calls (e.g., GPT‑5), lightweight verification scripts and other auxiliary tooling. This setup scales to large workloads and produces diverse variants, without any per‑item manual rewriting or hand‑crafting of individual problems. Moreover, we are actively exploring additional automated AIME‑style transformation pipelines to further enrich A‑MES.

Overall, these five transformation pipelines realize seven concrete augmentation mechanisms for each workload (here, a workload means a question within the benchmark):
1-3. Distractor Insertion
   - Context‑irrelevant distractor insertion
   - Context‑relevant explanatory distractor insertion
   - Context‑relevant misleading distractor insertion
4. Numeric substitutions
5. Conditional recomposition
6. Recent‑source adaptation
7. Conceptual synthesis

These mechanisms show that A‑MES is not a collection of ad‑hoc, hand‑edited examples, but a unified, automatable framework that systematically augments existing benchmarks to more comprehensively evaluate model capabilities. For each question within a benchmark, we first apply all seven mechanisms to construct the full space of augmented variants, filtering out transformation attempts that fail (e.g., numeric substitutions without a stable solver). Evaluation then samples directly from this augmentation space, ensuring that no invalid transformations are ever selected. The framework enumerates the entire augmentation space upfront, and the small number of discarded variants has negligible impact on overall coverage or robustness. For several major benchmarks, we have already constructed the corresponding augmentation spaces and plan to release them publicly in future work. Below, we provide concrete descriptions of the seven mechanisms.

## 1. Analogical‑1: distractor insertion with three well-defined categories

For distractor insertion, we define three explicit, controllable categories of redundancy and implement all instances via LLM prompting. To ensure that the inserted distractors strictly follow our predefined specifications, we empirically test several candidate LLMs and choose the one that most consistently adheres to these constraints (GPT-5). This selection is made solely to guarantee transformation fidelity rather than to compare model capabilities. For each item to be transformed, the chosen LLM is invoked through an API and, guided by our structured prompts, automatically produces and inserts the required redundant content. The prompts are provided below.

- **Context‑irrelevant redundancy**  
  - Provide the LLM with an example containing an original question and a version with added context‑irrelevant redundancy.  
  - Instruct the LLM to insert one sentence at a random position that is completely unrelated to the target question.

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
  - Provide the LLM with an example of an original question and a version with added explanatory redundancy.  
  - Instruct the LLM to insert a redundant sentence at a random position in each target question that explains a concept already appearing in the target question.

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
  - Provide the LLM with an example containing an original question and a version with added misleading but logically related redundancy.  
  - Supply the model with the correct answer and several correct solution approaches that are automatically retrieved at run time from online resources (this step is optional; if no such solution approaches can be found, only the correct answer is provided), and instruct it to avoid directly hinting at these correct strategies when crafting the misleading cue.  
  - Instruct the model to insert a redundant sentence that nudges the reader toward an incorrect strategy or line of reasoning, without explicitly revealing that it is "misleading" or "distracting."
  
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

Algorithm 4: Numeric Substitutions

```pseudo
FUNCTION BuildNumericSolver(problem_text, answer_gold, solution_sketches, max_iter=5, max_refine=5):
  knowledge_points ← LLM_ExtractKnowledgePoints(problem_text)
  retrieved_formulas ← RETRIEVE_FORMULAS(knowledge_points)
  history ← EMPTY_LIST
  FOR iter IN 1..max_iter:
    PROMPT ← BuildPromptCodeGen(problem_text, answer_gold, solution_sketches, retrieved_formulas)
    history.APPEND((PROMPT, None))
    (CODE, value_ranges)   ← LLM_CALL(PROMPT)
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
    history.APPEND((PROMPT, None)
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
