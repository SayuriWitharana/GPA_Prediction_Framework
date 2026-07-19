# Research Positioning for IEEE TALE 2026

## Working Research Vision

This research is **not** intended to develop a new machine learning
model or achieve the highest prediction accuracy. Instead, it proposes a
**decision-support framework** that helps universities determine **when
student GPA predictions become sufficiently trustworthy to support
educational decisions**.

A simple and interpretable Ridge Regression model is deliberately used
because the contribution lies in the **evaluation framework**, rather
than algorithmic optimisation.

------------------------------------------------------------------------

# Problem Statement

Early warning systems have become a major component of Learning
Analytics. Most existing studies focus on improving prediction accuracy
or comparing machine learning models.

However, an important question remains largely unanswered:

> **At what point are GPA predictions sufficiently reliable to support
> educational action?**

Most studies report a single accuracy metric while overlooking
prediction stability across different training samples and systematic
directional bias affecting different student performance groups.

Consequently, universities may deploy models that appear accurate
overall but remain unreliable for specific groups, particularly
academically underperforming students.

------------------------------------------------------------------------

# Research Gap

Most existing work asks:

> Which model predicts best?

This research instead asks:

> When can predictions be trusted enough to responsibly inform
> educational decisions?

The focus therefore shifts from model optimisation toward trustworthy
deployment of learning analytics.

------------------------------------------------------------------------

# Research Objectives

## RQ1

Determine the earliest semester at which final GPA predictions become
reliably actionable by jointly evaluating:

-   Prediction accuracy
-   Prediction stability
-   Group-level directional bias

## RQ2

Explain why prediction reliability changes over time by analysing:

-   Temporal feature importance
-   Module-level importance
-   Semester GPA evolution
-   Early indicators of academic underperformance

RQ2 complements RQ1 by explaining why reliability emerges.

------------------------------------------------------------------------

# Proposed Solution

The framework contains two complementary components.

## 1. Reliability Framework

Predictions are evaluated using:

1.  RMSE (accuracy)
2.  RMSE stability across repeated cross-validation
3.  Group-level directional bias

The framework determines how much confidence institutions should place
in predictions at each stage of a student's academic journey.

## 2. Temporal Explainability

RQ2 investigates why reliability improves by examining changing feature
importance using SHAP and related analyses.

------------------------------------------------------------------------

# Educational Interpretation

The framework does **not** recommend waiting until predictions become
highly reliable before supporting students.

Instead, prediction confidence determines the type of educational
action.

  -----------------------------------------------------------------------
  Reliability                         Educational Use
  ----------------------------------- -----------------------------------
  Low                                 Screening, monitoring, advisor
                                      awareness, gather additional
                                      evidence

  Moderate                            Advisor review, mentoring, targeted
                                      academic support

  High                                Individualised intervention
                                      planning and higher-confidence
                                      decision support
  -----------------------------------------------------------------------

Predictions therefore evolve from screening signals into trustworthy
decision-support tools.

------------------------------------------------------------------------

# Expected Contributions

-   A group-aware reliability framework integrating accuracy, stability
    and bias.
-   Temporal explainability showing how predictive factors evolve.
-   A decision-support perspective linking prediction confidence with
    educational action.
-   A transferable methodology based on transparent regression rather
    than complex black-box models.

------------------------------------------------------------------------

# Core Message

This research is **not** about producing the most accurate prediction
model.

It is about helping universities understand:

1.  **When** GPA predictions become trustworthy.
2.  **Why** they become trustworthy.
3.  **How** prediction confidence should guide responsible educational
    interventions.

This positions the work within Learning Analytics, trustworthy AI, and
evidence-based educational decision support, aligning well with IEEE
TALE.
