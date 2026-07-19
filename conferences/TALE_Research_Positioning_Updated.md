# Research Positioning for IEEE TALE 2026

## Overall Research Vision

This research does **not** aim to develop a new machine learning
algorithm or achieve the highest prediction accuracy. Instead, it
proposes a **trustworthy learning analytics framework** that helps
universities understand:

1.  **When** GPA predictions become sufficiently trustworthy to support
    educational decisions.
2.  **Why** prediction reliability evolves throughout a student's
    academic journey.
3.  **How** educational institutions should use predictions of different
    confidence levels to support responsible interventions.

A transparent Ridge Regression model is deliberately adopted because the
contribution lies in the **evaluation framework and educational
interpretation**, rather than algorithmic optimisation.

------------------------------------------------------------------------

# Problem Statement

Early warning systems are widely used in higher education to identify
students who may require academic support. However, most existing
studies concentrate on improving prediction accuracy or comparing
machine learning algorithms.

A critical question remains unanswered:

> **When are student performance predictions sufficiently trustworthy to
> support educational action?**

Most studies evaluate models using a single performance metric while
overlooking:

-   prediction stability,
-   systematic bias,
-   differences across student performance groups, and
-   how prediction confidence should influence educational decisions.

Consequently, universities may deploy prediction systems that appear
accurate overall but remain unreliable for the very students most in
need of support.

------------------------------------------------------------------------

# Research Gap

Current research predominantly asks:

> **Which model predicts student performance most accurately?**

This research instead asks:

> **When can predictions be trusted, why do they become trustworthy, and
> how should educators act on predictions with different levels of
> confidence?**

The focus therefore shifts from model optimisation towards **trustworthy
deployment of learning analytics**.

------------------------------------------------------------------------

# Overall Research Framework

Rather than viewing RQ1 and RQ2 as independent studies, they form one
integrated framework.

## Part I --- Trustworthy Prediction (RQ1)

### Purpose

Determine **when** final GPA predictions become reliably actionable.

### Dataset

-   Pre-academic factors
-   Demographic variables
-   Semester GPA

No module-level information is included because the objective is to
evaluate prediction reliability using information routinely available to
universities.

### Research Question

At what semester do predictions become sufficiently trustworthy after
jointly considering:

-   Accuracy
-   Prediction Stability
-   Group-level Directional Bias

The outcome is a reliability framework indicating the confidence
institutions should place in GPA predictions over time.

------------------------------------------------------------------------

## Part II --- Understanding Prediction Reliability (RQ2)

### Purpose

Explain **why** prediction reliability evolves throughout the programme.

Rather than improving prediction accuracy, RQ2 opens the "black box" by
investigating the educational factors responsible for prediction
behaviour.

### Dataset

RQ2 uses all information available up to each semester:

-   Pre-academic factors
-   Demographics
-   Semester GPAs
-   Module grades completed up to that semester

Future information is never included.

Module-level information is introduced **only to explain prediction
behaviour**, not to improve the prediction framework developed in RQ1.

### Research Question

How does the explanatory importance of:

-   pre-academic characteristics,
-   semester GPAs,
-   module performance,
-   demographic factors,

change throughout the degree programme, and what early academic signals
indicate potential underperformance?

------------------------------------------------------------------------

# Relationship Between RQ1 and RQ2

RQ1 and RQ2 answer different but complementary questions.

  -----------------------------------------------------------------------
  RQ1                                 RQ2
  ----------------------------------- -----------------------------------
  When are predictions trustworthy?   Why do they become trustworthy?

  Reliability evaluation              Educational explanation

  Uses semester GPA                   Opens semester GPA using
                                      module-level information

  Institutional perspective           Learning perspective
  -----------------------------------------------------------------------

RQ2 does **not** replace RQ1. Instead, it provides the educational
explanation behind the reliability patterns identified in RQ1.

------------------------------------------------------------------------

# Proposed Solution

The complete framework contains two complementary components.

## Component 1 --- Reliability Framework

Prediction reliability is evaluated using:

1.  Prediction Accuracy (RMSE)
2.  Prediction Stability (SD of RMSE across repeated cross-validation)
3.  Group-level Directional Bias

The framework determines how much confidence universities should place
in predictions at different stages of a student's academic journey.

------------------------------------------------------------------------

## Component 2 --- Temporal Explainability

RQ2 investigates how predictive information evolves over time using
SHAP.

The focus is on:

-   evolution of semester GPA importance,
-   module-level contributions,
-   persistence of pre-academic characteristics,
-   emergence of early academic risk signals.

The objective is to explain why prediction reliability changes rather
than simply reporting feature rankings.

------------------------------------------------------------------------

# Educational Interpretation

The framework does **not** recommend delaying support until predictions
become highly reliable.

Instead, prediction confidence determines the **type of educational
action**.

  -----------------------------------------------------------------------
  Prediction Reliability            Suggested Educational Use
  --------------------------------- -------------------------------------
  Low                               Screening signal, advisor awareness,
                                    monitoring, gather additional
                                    evidence

  Moderate                          Advisor review, mentoring, targeted
                                    academic support

  High                              Individualised intervention planning
                                    and higher-confidence decision
                                    support
  -----------------------------------------------------------------------

Predictions therefore evolve from **screening tools** into
**decision-support tools**.

------------------------------------------------------------------------

# Expected Contributions

The integrated framework contributes by providing:

-   A group-aware reliability framework integrating accuracy, stability
    and bias.
-   A temporal explainability framework describing how academic
    predictors evolve.
-   A decision-support perspective linking prediction confidence with
    educational action.
-   A transparent and transferable methodology suitable for institutions
    without requiring complex black-box models.

------------------------------------------------------------------------

# Core Message

The central contribution of this research is **not**:

> "We can predict GPA earlier."

Instead, it is:

> **We provide a trustworthy learning analytics framework that helps
> universities understand when GPA predictions become trustworthy, why
> they become trustworthy, and how prediction confidence should guide
> responsible educational decision-making.**

This positions the research within Learning Analytics, explainable AI,
trustworthy AI, and evidence-based educational decision support,
aligning well with IEEE TALE.
