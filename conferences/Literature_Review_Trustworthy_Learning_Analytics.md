**Comprehensive Literature Review**

Early Student Performance Prediction and Trustworthy Learning Analytics

_Prepared in support of the Trustworthy Learning Analytics Group-aware Framework for Responsible Early Academic Intervention_

**Search strategy:** Structured search across IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect/Elsevier, Wiley, Taylor & Francis, EDM, LAK, IEEE TALE, Computers & Education, IEEE Access and other reputable academic sources, executed via live web search on 19 July 2026.

**Coverage:** 24 papers across six research themes, each documented with full bibliographic detail, methodological summary, and relevance assessment.

_Note: entries marked with a ⚠ verification flag have incomplete author metadata in the retrieved search snippets. These should be cross-checked against the original publisher record before inclusion in the final dissertation reference list. No citation in this document has been invented - where detail could not be confirmed, this is stated explicitly rather than filled in._

# Table of Contents

# 1\. Search Methodology

This review followed the structured search prompt defined in the project's Research Strategy & Design Document (Part C, Section 9). Searches were executed as live web queries on 19 July 2026, targeting the specified academic sources (IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect/Elsevier, Wiley, Taylor & Francis, Educational Data Mining, Learning Analytics and Knowledge, IEEE TALE, Computers & Education, IEEE Access, and related venues) plus open-access aggregators (arXiv, PLOS ONE, MDPI, PMC) where these hosted directly relevant peer-reviewed or pre-print work.

Twenty-four papers were selected - four per research theme - prioritising recency (2019-2026), direct relevance to student performance prediction, explainability, fairness, or temporal analysis, and diversity of venue. Where full author metadata could not be confirmed from the retrieved search snippets, this is flagged explicitly rather than inferred, in line with the instruction to avoid inventing citations.

This review should be treated as a strong first pass rather than an exhaustive systematic review: a full PRISMA-style systematic review (database-by-database, with formal inclusion/exclusion screening) would be needed to support a journal-length related-work section, and is recommended as a next step once the dissertation's scope is finalised.

# Theme 1 - Learning Analytics and Educational Data Mining

This theme establishes the conceptual foundation for the review: the historical development, definitions, and relationship between Learning Analytics (LA) and Educational Data Mining (EDM), the two overlapping fields from which this research draws its methods and vocabulary.

### \[1\] Romero, C., & Ventura, S (2020)

**APA citation:** Romero, C., & Ventura, S. (2020). Educational data mining and learning analytics: An updated survey. WIREs Data Mining and Knowledge Discovery, 10(3), e1355.

**IEEE citation:** C. Romero and S. Ventura, "Educational data mining and learning analytics: An updated survey," WIREs Data Min. Knowl. Discov., vol. 10, no. 3, e1355, 2020.

**DOI / Link:** <https://doi.org/10.1002/widm.1355>

**Year:** 2020

**Venue:** WIREs Data Mining and Knowledge Discovery

**Research objective:** Provide an updated, comprehensive survey of EDM/LA methods, tools, and applications following on from the authors' earlier 2013 survey.

**Dataset characteristics:** Survey paper - synthesises findings across hundreds of primary EDM/LA studies rather than a single dataset.

**Features used:** Not applicable (survey); catalogues commonly used feature types across the field (academic, demographic, behavioural, LMS log data).

**Prediction model(s):** Reviews classification, regression, clustering, association rule mining, and recommender-system techniques as applied across EDM/LA.

**Explainability technique:** Notes the growing but still limited attention to interpretability in EDM/LA research as of 2020.

**Evaluation metrics:** Surveys accuracy, RMSE, and other metrics as reported across reviewed studies (not a primary evaluation).

**Key findings:** Confirms continued growth of prediction-of-performance as the dominant EDM/LA task and identifies emerging areas including MOOCs, learning-path mining, and gamification analytics.

**Limitations:** As a broad survey, it does not evaluate reliability, stability, or trustworthiness of individual prediction pipelines in depth.

**Relevance to this research:** Provides the disciplinary foundation and terminology (EDM vs LA) underpinning Theme 1 of the proposed framework and situates prediction-of-performance as the field's most persistent task.

### \[2\] Papamitsiou, Z., & Economides, A (2014)

**APA citation:** Papamitsiou, Z., & Economides, A. A. (2014). Learning analytics and educational data mining in practice: A systematic literature review of empirical evidence. Journal of Educational Technology & Society, 17(4), 49-64.

**IEEE citation:** Z. Papamitsiou and A. A. Economides, "Learning analytics and educational data mining in practice: A systematic literature review of empirical evidence," J. Educ. Technol. Soc., vol. 17, no. 4, pp. 49-64, 2014.

**DOI / Link:** <https://www.jstor.org/stable/jeductechsoci.17.4.49>

**Year:** 2014

**Venue:** Journal of Educational Technology & Society

**Research objective:** Systematically review 40 empirical LA/EDM case studies (from 209 screened) to categorise objectives, methods, and findings.

**Dataset characteristics:** 40 empirical studies published 2008-2013, drawn from a pool of 209 candidate papers.

**Features used:** Categorises studies by the type of data used (behavioural, performance, demographic) rather than proposing new features.

**Prediction model(s):** Surveys prediction, clustering, social-network analysis, visualisation, and recommendation approaches used across the reviewed studies.

**Explainability technique:** Not a focus of the reviewed period; interpretability is largely absent from the 2008-2013 literature it covers.

**Evaluation metrics:** Synthesises accuracy-oriented metrics reported by the reviewed studies without proposing new evaluation criteria.

**Key findings:** Identifies four dominant objective categories: pedagogy-related, evaluation-related, domain-application-related, and technical issues, with performance prediction being the most common pedagogy-related task.

**Limitations:** Restricted to 2008-2013 literature; does not capture the more recent shift toward deep learning or explainability.

**Relevance to this research:** One of the most widely cited LA/EDM classification frameworks; used here to justify why this study is framed as an LA (decision-support) rather than a pure EDM (technique-focused) contribution.

### \[3\] Author(s) not fully confirmed from available search metadata (2024)

**APA citation:** Author(s) not fully confirmed from available search metadata. (2024). Reviewing the differences between learning analytics and educational data mining: Towards educational data science. Computers & Education.

**IEEE citation:** Author(s) unverified, "Reviewing the differences between learning analytics and educational data mining: Towards educational data science," Computers & Education, 2024.

**DOI / Link:** <https://www.sciencedirect.com/science/article/abs/pii/S0747563224000220>

**Year:** 2024

**Venue:** Computers & Education

**Research objective:** Conduct a PRISMA-guided systematic review of papers that explicitly compare LA and EDM, synthesising 11 identified differences between the fields.

**Dataset characteristics:** 10 research works meeting PRISMA inclusion criteria on the LA-vs-EDM distinction.

**Features used:** Not applicable - conceptual/bibliometric review rather than a predictive-modelling study.

**Prediction model(s):** Not applicable.

**Explainability technique:** Not directly addressed; the review is positioning-oriented rather than technique-oriented.

**Evaluation metrics:** Not applicable (qualitative synthesis).

**Key findings:** Confirms that LA and EDM, while historically distinguished by holistic vs. reductionist analytical philosophy, increasingly overlap in practice, motivating the umbrella term 'educational data science.'

**Limitations:** Small final sample (10 papers) limits generalisability of the 11 identified differences.

**Relevance to this research:** Supports the framing of this research as sitting at the LA/EDM boundary - using EDM-style predictive modelling in service of an LA-style decision-support goal.

**_⚠ Verification note:_** _Full author list could not be confirmed from the available search snippet; please verify directly via the ScienceDirect record before citing in the final dissertation._

### \[4\] Author(s) not fully confirmed from available search metadata (2021)

**APA citation:** Author(s) not fully confirmed from available search metadata. (2021). Comparison of learning analytics and educational data mining: A topic modeling approach. Computers and Education: Artificial Intelligence, 2, 100034.

**IEEE citation:** Author(s) unverified, "Comparison of learning analytics and educational data mining: A topic modeling approach," Computers and Education: Artificial Intelligence, vol. 2, 100034, 2021.

**DOI / Link:** <https://www.sciencedirect.com/science/article/pii/S2666920X21000102>

**Year:** 2021

**Venue:** Computers and Education: Artificial Intelligence

**Research objective:** Use topic modelling (rather than narrative review) to empirically compare the research foci of LA and EDM publications from 2015-2019.

**Dataset characteristics:** Corpus of LA and EDM conference/journal abstracts published 2015-2019.

**Features used:** Text-mining features (topic-term distributions) rather than student-level features.

**Prediction model(s):** Latent Dirichlet Allocation (LDA) topic modelling.

**Explainability technique:** Not applicable in the predictive-modelling sense; the paper's own method is inherently interpretable (topic-term weights).

**Evaluation metrics:** Topic coherence and qualitative topic-label validation.

**Key findings:** Finds that the difference between LA and EDM topics is 'a matter of degree rather than kind': both are heavily focused on student performance and platform behaviour, with LA leaning toward engagement/social-network topics and EDM toward algorithmic/technique topics.

**Limitations:** Topic modelling is sensitive to corpus selection and preprocessing choices; does not capture qualitative nuance a narrative review would.

**Relevance to this research:** Empirically corroborates Papamitsiou and Economides' conceptual distinction and reinforces that prediction-of-performance is the shared core task this research builds on.

**_⚠ Verification note:_** _Full author list could not be confirmed from the available search snippet; please verify directly via the ScienceDirect record before citing in the final dissertation._

# Theme 2 - Student Performance Prediction

This theme reviews the core predictive-modelling literature: which algorithms, features, and datasets are used to forecast student academic performance, and how researchers currently benchmark predictive accuracy.

### \[5\] Ahmed, et al (2024)

**APA citation:** Ahmed, et al. (2024). Student performance prediction using machine learning algorithms. Applied Computational Intelligence and Soft Computing, 2024, 4067721.

**IEEE citation:** M. Ahmed et al., "Student performance prediction using machine learning algorithms," Appl. Comput. Intell. Soft Comput., vol. 2024, Art. no. 4067721, 2024.

**DOI / Link:** <https://doi.org/10.1155/2024/4067721>

**Year:** 2024

**Venue:** Applied Computational Intelligence and Soft Computing (Wiley)

**Research objective:** Compare SVM, Decision Tree, Naïve Bayes, and KNN classifiers for predicting student academic performance.

**Dataset characteristics:** Institutional student records including demographic and prior-performance attributes (exact size not specified in available abstract).

**Features used:** Demographic variables (gender, age), prior academic records, and behavioural indicators associated with e-learning/LMS engagement.

**Prediction model(s):** Support Vector Machine, Decision Tree, Naïve Bayes, K-Nearest Neighbours.

**Explainability technique:** Not addressed - the study is accuracy-focused rather than interpretability-focused.

**Evaluation metrics:** Classification accuracy (SVM/DT/KNN reported as more accurate than Naïve Bayes at 83.3%).

**Key findings:** SVM, Decision Tree, and KNN outperformed Naïve Bayes; ensemble/tree-based and margin-based classifiers were more versatile across feature types.

**Limitations:** No stability analysis (single train/test split implied), no explainability, no discussion of fairness across subgroups.

**Relevance to this research:** Representative of the still-dominant 'accuracy comparison' paradigm this research explicitly moves beyond - illustrating Research Gap 1 (overemphasis on algorithm comparison).

**_⚠ Verification note:_** _Full first-author given name/full author list not confirmed from the available abstract; verify via the Wiley record before final citation._

### \[6\] Yadav, N (2023)

**APA citation:** Yadav, N. R., & Deshmukh, S. S. (2023). Prediction of student performance using machine learning techniques: A review. In Proceedings of ICAMIDA 2022 (pp. 735-741). Atlantis Press.

**IEEE citation:** N. R. Yadav and S. S. Deshmukh, "Prediction of student performance using machine learning techniques: A review," in Proc. ICAMIDA 2022, 2023, pp. 735-741.

**DOI / Link:** <https://doi.org/10.2991/978-94-6463-136-4_63>

**Year:** 2023

**Venue:** Proceedings of the International Conference on Applications of Machine Intelligence and Data Analytics (ICAMIDA 2022), Atlantis Press

**Research objective:** Review machine-learning and data-mining techniques used to predict and classify student academic performance in higher education.

**Dataset characteristics:** Narrative review spanning multiple institutional and public datasets cited across prior studies.

**Features used:** Reviews commonly used feature categories: demographic, prior grades, attendance, and LMS interaction data.

**Prediction model(s):** Decision Tree, SVM, clustering (k-means) and classification approaches reported across reviewed studies.

**Explainability technique:** Not a focus; the review pre-dates the recent uptake of SHAP/LIME in this sub-field.

**Evaluation metrics:** Reports accuracy figures cited from reviewed studies (no independent evaluation).

**Key findings:** Confirms that classification and clustering are the two most common EDM techniques applied to student performance, echoing Theme 1 findings.

**Limitations:** Narrow review scope, does not assess reliability or stability of the models it summarises.

**Relevance to this research:** Useful as a recent (2023) confirmation that mainstream literature remains accuracy-centred, reinforcing the motivation for the proposed reliability-based framework.

### \[7\] Author(s) not fully confirmed from available search metadata (2026)

**APA citation:** Author(s) not fully confirmed from available search metadata. (2026). Predicting student performance: A comprehensive review of machine learning, deep learning, and explainable AI approaches. Computers and Education: Artificial Intelligence.

**IEEE citation:** Author(s) unverified, "Predicting student performance: A comprehensive review of machine learning, deep learning, and explainable AI approaches," Computers and Education: Artificial Intelligence, 2026.

**DOI / Link:** <https://www.sciencedirect.com/science/article/pii/S2666920X26000093>

**Year:** 2026

**Venue:** Computers and Education: Artificial Intelligence

**Research objective:** Provide a comprehensive, recent (2026) review spanning classical ML, deep learning (CNN/GNN), and XAI approaches to student performance prediction.

**Dataset characteristics:** Reviews multiple public datasets, including the UCI Student Performance dataset (used in five of the surveyed studies) and proprietary institutional datasets.

**Features used:** Grades, demographic, social, and school-related attributes; behavioural and contextual factors such as dormitory residence and sponsorship in some reviewed studies.

**Prediction model(s):** Classical ML (SVM, RF, XGBoost), CNNs, and Graph Neural Networks (GNNs), including hybrid architectures such as relationship-matrix hybrid neural networks.

**Explainability technique:** Explicitly reviews XAI approaches as one of its three pillars, alongside ML and DL - notes CNNs' black-box nature limits practical educational use.

**Evaluation metrics:** Accuracy and F1-score are the dominant metrics reported across surveyed studies (e.g., 93.1% accuracy / 90.4% F1 for one hybrid neural network).

**Key findings:** Identifies a shift toward graph-based and hybrid deep-learning models but confirms that interpretability trade-offs remain unresolved, particularly for CNN/GNN architectures.

**Limitations:** As a very recent review, the underlying primary studies it covers have not yet accumulated substantial independent replication.

**Relevance to this research:** The most directly comparable existing review to this research's Part C; it confirms that explainability and interpretability remain secondary considerations relative to raw accuracy - directly supporting the identified research gap.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet (article appears very recently indexed); verify via the ScienceDirect record before final citation._

### \[8\] Author(s) not fully confirmed from available search metadata (2024)

**APA citation:** Author(s) not fully confirmed from available search metadata. (2024). High school student GPA prediction by various linear regression models.

**IEEE citation:** Author(s) unverified, "High school student GPA prediction by various linear regression models," 2024.

**DOI / Link:** <https://www.researchgate.net/publication/384442979>

**Year:** 2024

**Venue:** Preprint / conference paper (exact venue unconfirmed)

**Research objective:** Compare linear, ridge, lasso, and LassoCV regression models for predicting high-school student GPA.

**Dataset characteristics:** 2,392 North American high-school students (Kaggle 'Kharoua' dataset), including age, gender, ethnicity, parental education, study time, absences, tutoring, and extracurricular indicators.

**Features used:** Age, gender, ethnicity, parental education, weekly study time, absences, tutoring, parental support, extracurricular/sports/music/volunteering participation.

**Prediction model(s):** Linear regression, Ridge regression, Lasso regression, LassoCV.

**Explainability technique:** Relies on the inherent transparency of linear-model coefficients rather than post-hoc explainability tools such as SHAP.

**Evaluation metrics:** R² and RMSE, compared across the four linear model variants.

**Key findings:** LassoCV achieved the best R²/RMSE trade-off among the tested linear variants; ridge regression remained competitive and notably more stable under multicollinearity than ordinary least squares.

**Limitations:** Restricted to linear-model families; a single dataset and snapshot in time, with no explicit stability or cross-semester analysis.

**Relevance to this research:** Directly supports the methodological justification in Part B for selecting Ridge Regression: it demonstrates that regularised linear regression is competitive with more complex alternatives for GPA-style prediction tasks while remaining transparent.

**_⚠ Verification note:_** _Full author list and exact publication venue not confirmed from the available search snippet; verify via ResearchGate/publisher record before final citation._

# Theme 3 - Early Warning Systems

This theme reviews systems designed to flag at-risk students as early as possible within a course or programme, focusing on the trade-off between early prediction and reliability, and how EWS research treats intervention timing.

### \[9\] Author(s) not fully confirmed from available search metadata (2020)

**APA citation:** Author(s) not fully confirmed from available search metadata. (2020). An early warning system to detect at-risk students in online higher education.

**IEEE citation:** Author(s) unverified, "An early warning system to detect at-risk students in online higher education," 2020.

**DOI / Link:** <https://www.researchgate.net/publication/342528584>

**Year:** 2020

**Venue:** Conference/journal venue not confirmed from available metadata

**Research objective:** Develop and test an end-to-end early warning system (EWS) for detecting at-risk students in an online higher-education setting, including a method for setting a decision threshold.

**Dataset characteristics:** Institutional data mart with curated data spanning six semesters of an online higher-education programme.

**Features used:** Graded assessment activity data used to construct a binary pass/fail prediction target.

**Prediction model(s):** Predictive classifiers compared against a LOESS-regression-based submodel; best classifier and training-set selection method proposed.

**Explainability technique:** Not addressed - focus is on threshold calibration and deployment, not on interpretability.

**Evaluation metrics:** True Positive Rate (TPR) improvements reported, ranging from roughly 45-86% for one method up to ~59-94% for the improved LOESS-based approach.

**Key findings:** Demonstrates that a properly calibrated threshold substantially improves real-world usability of an EWS, and that the system can provide personalised feedback to identified at-risk students.

**Limitations:** Single-institution deployment; no explicit stability/reliability analysis across repeated training runs or demographic subgroups.

**Relevance to this research:** Illustrates Research Gap 3 - EWS research prioritises detection threshold and accuracy over the reliability/stability dimensions central to this proposed framework.

**_⚠ Verification note:_** _Full author list and exact peer-reviewed venue could not be confirmed from the available search snippet; verify directly before final citation._

### \[10\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). ouladFormat R package: Preparing the Open University Learning Analytics Dataset for analysis. arXiv:2501.08366.

**IEEE citation:** Author(s) unverified, "ouladFormat R package: Preparing the Open University Learning Analytics Dataset for analysis," arXiv:2501.08366, 2025.

**DOI / Link:** <https://arxiv.org/pdf/2501.08366>

**Year:** 2025

**Venue:** arXiv preprint

**Research objective:** Present an R package for preparing the Open University Learning Analytics Dataset (OULAD) for analysis, illustrated through case studies including early identification of at-risk students.

**Dataset characteristics:** OULAD - a widely used public UK Open University dataset covering VLE interactions, assessment results, and demographics across multiple course presentations.

**Features used:** VLE clickstream/engagement data, assessment scores, and demographic variables.

**Prediction model(s):** References prior EWS work on OULAD (e.g., Drousiotis, Shi & Maskell, 2021) that predicts final results (withdrawn, fail, pass, distinction) as early as possible within the teaching semester.

**Explainability technique:** Not a primary focus; the package paper is a data-preparation and tooling contribution.

**Evaluation metrics:** Not independently reported; refers to accuracy metrics from cited early-identification studies.

**Key findings:** Confirms OULAD's continued role as a benchmark dataset for early at-risk identification research, and that identifying at-risk students 'as early as possible' remains an explicit, unresolved objective in this literature.

**Limitations:** As a tooling paper, it does not itself contribute new predictive-reliability evidence.

**Relevance to this research:** Supports the use of a semester-wise incremental approach for RQ1, and evidences that OULAD-based EWS research still frames 'earliness' primarily as a data-availability problem rather than a reliability problem.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via arXiv listing before final citation._

### \[11\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). AI-driven early warning systems for student success: Discovering static feature dominance in temporal prediction models. arXiv:2512.12493.

**IEEE citation:** Author(s) unverified, "AI-driven early warning systems for student success: Discovering static feature dominance in temporal prediction models," arXiv:2512.12493, 2025.

**DOI / Link:** <https://arxiv.org/pdf/2512.12493>

**Year:** 2025

**Venue:** arXiv preprint

**Research objective:** Compare Decision Tree and LSTM models across multiple temporal snapshots (up to week 20 of an online course, i.e., 50% course completion) to identify at-risk students earlier than prior work.

**Dataset characteristics:** Online course interaction data with weekly temporal snapshots up to the course midpoint.

**Features used:** Static demographic features and temporal/behavioural features captured at each weekly snapshot.

**Prediction model(s):** Decision Tree and LSTM, compared explicitly across time.

**Explainability technique:** Reports feature-importance decomposition showing static demographic features account for 68% of predictive importance at early snapshots.

**Evaluation metrics:** Predictive accuracy/importance decomposition across temporal snapshots (specific accuracy figures not detailed in the available abstract).

**Key findings:** Different models excel at different intervention stages, and static (non-behavioural) features dominate early predictions, enabling 'assessment-free' early prediction before substantial behavioural data accumulates.

**Limitations:** Restricted to a single online course context; the 50%-of-course cutoff may not generalise to semester-based, in-person higher-education settings.

**Relevance to this research:** Directly relevant to RQ1 and RQ2: demonstrates empirically that feature importance is not static across time - the central premise this research investigates via Linear SHAP.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via arXiv listing before final citation._

### \[12\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). Early prediction of at-risk students using minimal data: A machine learning framework for higher education. Digitus: Journal of Computer Science Applications.

**IEEE citation:** Author(s) unverified, "Early prediction of at-risk students using minimal data: A machine learning framework for higher education," Digitus J. Comput. Sci. Appl., 2025.

**DOI / Link:** <https://journal.idscipub.com/index.php/digitus/article/view/953>

**Year:** 2025

**Venue:** Digitus: Journal of Computer Science Applications

**Research objective:** Investigate whether pre-admission and first-four-week LMS data can reliably support early warning systems using minimal available data.

**Dataset characteristics:** Pre-admission records and early-semester (first four weeks) LMS interaction data from a higher-education institution.

**Features used:** Pre-admission academic indicators and early-semester LMS engagement signals.

**Prediction model(s):** CatBoost, benchmarked as the primary gradient-boosting classifier.

**Explainability technique:** Not a stated focus; the emphasis is on data minimality and early availability rather than interpretability.

**Evaluation metrics:** Predictive performance of CatBoost using minimal early data (specific figures not detailed in the available abstract).

**Key findings:** Limited, readily available early data can meaningfully support early warning systems, but institutional readiness, ethics, and inclusivity are needed for responsible deployment.

**Limitations:** Single-institution study; explicitly calls for cross-institutional generalisability testing in future work.

**Relevance to this research:** Reinforces the practical motivation for RQ1 - identifying the earliest point at which predictions are usable - while explicitly flagging the ethical deployment considerations this research's Educational Decision Framework addresses.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via publisher record before final citation._

# Theme 4 - Explainable Artificial Intelligence (SHAP)

This theme reviews the explainable AI (XAI) literature underpinning the study's Linear SHAP approach, from the foundational SHAP framework through its recent educational applications.

### \[13\] Lundberg, S (2017)

**APA citation:** Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems 30 (pp. 4765-4774). Curran Associates.

**IEEE citation:** S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Adv. Neural Inf. Process. Syst. 30, 2017, pp. 4765-4774.

**DOI / Link:** <https://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions>

**Year:** 2017

**Venue:** Advances in Neural Information Processing Systems (NeurIPS)

**Research objective:** Introduce SHAP (SHapley Additive exPlanations), a unified, game-theoretically grounded framework for interpreting the output of any machine-learning model.

**Dataset characteristics:** Not applicable - a methodological/theoretical contribution, illustrated on benchmark datasets.

**Features used:** Not applicable - defines a model-agnostic explanation method assigning an importance value (Shapley value) to each input feature per prediction.

**Prediction model(s):** Framework applicable to any model class; unifies prior additive feature-attribution methods (e.g., LIME, DeepLIFT) under one theoretical umbrella.

**Explainability technique:** SHAP itself is the explainability contribution: proves a unique solution exists within the class of additive feature-attribution methods satisfying local accuracy, missingness, and consistency properties.

**Evaluation metrics:** Theoretical properties (local accuracy, consistency) rather than predictive-performance metrics.

**Key findings:** Establishes SHAP as a theoretically grounded, consistent alternative to ad hoc feature-importance methods, and shows it unifies six previously disconnected explanation methods.

**Limitations:** Exact Shapley-value computation is combinatorially expensive; approximation methods (e.g., Kernel SHAP, Linear SHAP, Tree SHAP) are required in practice.

**Relevance to this research:** The foundational reference for the study's use of Linear SHAP; establishes the theoretical guarantee (consistency) that justifies interpreting semester-wise SHAP changes as genuine shifts in feature contribution rather than method artefacts.

### \[14\] Wang, S., & Luo, B (2024)

**APA citation:** Wang, S., & Luo, B. (2024). Academic achievement prediction in higher education through interpretable modeling. PLOS ONE, 19(9), e0309838.

**IEEE citation:** S. Wang and B. Luo, "Academic achievement prediction in higher education through interpretable modeling," PLOS ONE, vol. 19, no. 9, e0309838, 2024.

**DOI / Link:** <https://doi.org/10.1371/journal.pone.0309838>

**Year:** 2024

**Venue:** PLOS ONE

**Research objective:** Introduce the XGB-SHAP model, combining XGBoost with SHAP to predict and interpret student academic achievement across different instructional modes.

**Dataset characteristics:** 87 students enrolled in a Japanese-language course at a public university in Wuhan, China, between September 2021 and June 2023.

**Features used:** Instructional-mode-specific indicators (offline vs online teaching), plus academic and self-directed-learning indicators.

**Prediction model(s):** XGBoost (compared against three other ML models), interpreted using SHAP.

**Explainability technique:** SHAP summary and importance plots generated separately for offline and online teaching modes to reveal mode-specific driving factors.

**Evaluation metrics:** Mean Absolute Error (MAE ≈ 6) and R² (≈ 0.82), outperforming the three comparison models.

**Key findings:** The relative importance of features (e.g., self-directed learning skills) differs materially between instructional modes, showing that feature contributions are context-dependent rather than fixed.

**Limitations:** Very small sample (87 students) from a single course and institution limits generalisability.

**Relevance to this research:** Directly analogous methodologically to this research's RQ2: demonstrates that SHAP-based feature importance shifts meaningfully across contexts (here, teaching mode; in this study, semester/time) - supporting the premise that explanatory structure is not static.

### \[15\] Choi, W.-C., Choi, I.-C., Lam, C.-T., & Mendes, A (2026)

**APA citation:** Choi, W.-C., Choi, I.-C., Lam, C.-T., & Mendes, A. J. (2026). Explaining student performance prediction and generating personalized actionable feedback using explainable artificial intelligence (XAI) with SHAP. In Learning Technologies and Systems (LNCS 16425). Springer.

**IEEE citation:** W.-C. Choi, I.-C. Choi, C.-T. Lam, and A. J. Mendes, "Explaining student performance prediction and generating personalized actionable feedback using XAI with SHAP," in Learning Technologies and Systems, LNCS vol. 16425, Springer, 2026.

**DOI / Link:** <https://doi.org/10.1007/978-981-92-0042-9_19>

**Year:** 2026

**Venue:** Learning Technologies and Systems (SETE/ICWL), Lecture Notes in Computer Science, Springer

**Research objective:** Move beyond prediction to generate personalised, actionable feedback for both at-risk and high-performing students by linking SHAP-based explanations directly to feedback content.

**Dataset characteristics:** Programming-course performance data (building on the authors' earlier systematic review of performance prediction in learning-programming contexts).

**Features used:** Programming-course academic and behavioural performance indicators.

**Prediction model(s):** Machine-learning performance-prediction model interpreted via SHAP (specific base learner not detailed in the available abstract).

**Explainability technique:** SHAP explanations are explicitly translated into natural-language, personalised feedback - addressing a common EDM gap between prediction and actionable use.

**Evaluation metrics:** Not detailed in the available abstract; case studies are used to demonstrate interpretability and feedback quality.

**Key findings:** Case studies show SHAP-derived explanations can be operationalised into concrete guidance for both underperforming and high-performing students, closing the 'prediction-to-action' gap.

**Limitations:** Evaluation is case-study based rather than large-scale quantitative validation of feedback effectiveness.

**Relevance to this research:** Provides a direct precedent for this research's Educational Decision Framework - translating SHAP outputs into confidence-tiered, actionable guidance for educators rather than leaving explanations as a technical artefact.

### \[16\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). The integration of explainable AI in Educational Data Mining for student academic performance prediction and support system. (ScienceDirect-hosted journal, exact title unconfirmed.)

**IEEE citation:** Author(s) unverified, "The integration of explainable AI in Educational Data Mining for student academic performance prediction and support system," 2025.

**DOI / Link:** <https://www.sciencedirect.com/science/article/pii/S2772503025000180>

**Year:** 2025

**Venue:** ScienceDirect-hosted education-technology journal (exact journal title unconfirmed)

**Research objective:** Integrate multiple XAI techniques (SHAP, Shapash, ELI5, LIME) alongside classical and boosting classifiers to provide both global and local explanations for student performance classification.

**Dataset characteristics:** Not fully detailed in available metadata; multiclass student-performance classification task.

**Features used:** Academic and demographic indicators used for multiclass performance classification.

**Prediction model(s):** Decision Tree, Random Forest, Gradient Boosting, and XGBoost (multiclass classification); XGBoost reported best at 83% accuracy.

**Explainability technique:** Directly compares four XAI techniques (SHAP, Shapash, ELI5, LIME), characterising their relative strengths: SHAP for global understanding, Shapash for stakeholder communication, ELI5 for speed, LIME for local/individual explanations.

**Evaluation metrics:** Classification accuracy (83% for XGBoost) plus qualitative comparison of explanation techniques.

**Key findings:** No single XAI technique is universally best; technique choice should depend on the audience (technical vs non-technical stakeholders) and explanation scope (global vs local).

**Limitations:** Comparative XAI evaluation is largely qualitative; no formal agreement/consistency metric between the four XAI methods is reported.

**Relevance to this research:** Justifies this research's specific choice of Linear SHAP (rather than LIME or ELI5) as the most theoretically consistent method for global, semester-wise explanation, per the technique comparison this paper provides.

**_⚠ Verification note:_** _Author list and precise journal title could not be confirmed from the available search snippet; verify directly via the ScienceDirect record before final citation._

# Theme 5 - Trustworthy AI and Responsible AI in Education

This theme reviews frameworks and empirical studies addressing fairness, bias, transparency, and accountability in educational AI - the literature most directly aligned with this research's central 'trustworthiness' framing.

### \[17\] Morales Tirado, A., et al (2024)

**APA citation:** Morales Tirado, A., et al. (2024). Towards an operational responsible AI framework for learning analytics in higher education. arXiv:2410.05827.

**IEEE citation:** A. Morales Tirado et al., "Towards an operational responsible AI framework for learning analytics in higher education," arXiv:2410.05827, 2024.

**DOI / Link:** <https://arxiv.org/abs/2410.05827>

**Year:** 2024

**Venue:** arXiv preprint (not yet confirmed as peer-reviewed)

**Research objective:** Develop an operational Responsible AI (RAI) framework specifically for Learning Analytics in Higher Education, by mapping 11 established general-purpose RAI frameworks onto the LA/HE context.

**Dataset characteristics:** Not applicable - a framework-development paper rather than an empirical prediction study.

**Features used:** Not applicable.

**Prediction model(s):** Not applicable - proposes governance/design principles rather than a predictive model.

**Explainability technique:** Transparency and explainability are treated as one of several operational RAI principles (alongside fairness, accountability, and data privacy).

**Evaluation metrics:** Not applicable (qualitative framework).

**Key findings:** Existing generic Responsible AI frameworks (including those from major technology companies) are too high-level to guide practical LA deployment decisions; the proposed operational framework aims to close this practitioner-guidance gap.

**Limitations:** As a preprint, the framework has not yet undergone full peer review or large-scale institutional validation.

**Relevance to this research:** Provides direct precedent and structure for this research's Educational Decision Framework (Part B, Section 8), which similarly translates abstract trustworthiness principles (reliability, stability, bias) into concrete, tiered institutional guidance.

**_⚠ Verification note:_** _This is an arXiv preprint; peer-reviewed publication status should be re-checked before final citation, and the full author list should be verified against the arXiv listing._

### \[18\] Baker, R (2022)

**APA citation:** Baker, R. S., & Hawn, A. (2022). Algorithmic bias in education. International Journal of Artificial Intelligence in Education, 32(4), 1052-1092.

**IEEE citation:** R. S. Baker and A. Hawn, "Algorithmic bias in education," Int. J. Artif. Intell. Educ., vol. 32, no. 4, pp. 1052-1092, 2022.

**DOI / Link:** <https://doi.org/10.1007/s40593-021-00285-9>

**Year:** 2022

**Venue:** International Journal of Artificial Intelligence in Education

**Research objective:** Comprehensively review empirical evidence of algorithmic bias in education - which student groups are affected, and at which stages of the ML pipeline bias enters.

**Dataset characteristics:** Systematic review spanning the empirical algorithmic-bias-in-education literature (not a single dataset).

**Features used:** Reviews which demographic variables (race/ethnicity, gender, nationality, disability, socio-economic status) are studied and which are under-studied.

**Prediction model(s):** Reviews bias evidence across classification and prediction models generally, without proposing a single new model.

**Explainability technique:** Connects transparency/explainability to bias detection, arguing both are necessary but insufficient conditions for trustworthy educational AI.

**Evaluation metrics:** Surveys fairness metrics used across the reviewed literature (e.g., differential accuracy, calibration) without proposing a new metric.

**Key findings:** Confirms bias is empirically documented across multiple educational AI applications, disproportionately under-studied for students with disabilities, international students, and low-SES students, and overwhelmingly US-centric in current evidence.

**Limitations:** As a review, cannot quantify the magnitude of bias in any single new system; highlights evidentiary gaps rather than resolving them.

**Relevance to this research:** Provides the theoretical grounding for this research's directional-bias component of prediction reliability (RQ1), and motivates group-wise analysis across student performance groups.

### \[19\] Gardner, J., Brooks, C., & Baker, R (2019)

**APA citation:** Gardner, J., Brooks, C., & Baker, R. (2019). Evaluating the fairness of predictive student models through slicing analysis. In Proceedings of the 9th International Conference on Learning Analytics & Knowledge (LAK'19) (pp. 225-234). ACM.

**IEEE citation:** J. Gardner, C. Brooks, and R. Baker, "Evaluating the fairness of predictive student models through slicing analysis," in Proc. 9th Int. Conf. Learn. Anal. Knowl. (LAK'19), 2019, pp. 225-234.

**DOI / Link:** <https://doi.org/10.1145/3303772.3303791>

**Year:** 2019

**Venue:** Proceedings of the 9th International Conference on Learning Analytics & Knowledge (LAK'19), ACM (LAK'19 Best Full Paper)

**Research objective:** Introduce the ABROCA (Absolute Between-ROC Area) metric to quantify differential predictive-model performance between demographic subgroups without relying on a fixed classification threshold.

**Dataset characteristics:** MOOC performance-prediction datasets spanning multiple courses and models replicated from prior published work.

**Features used:** Course-interaction and demographic (gender) features used for subgroup slicing analysis.

**Prediction model(s):** Five predictive models replicated from prior published studies, evaluated via gender-based slicing.

**Explainability technique:** Not an explainability method per se, but provides an interpretable, threshold-independent visual/quantitative fairness diagnostic (the ABROCA plot).

**Evaluation metrics:** ABROCA (novel), plus underlying AUC/ROC comparisons across subgroups.

**Key findings:** Model fairness varies significantly by algorithm choice and feature set, and no consistent correlation was found between predictive performance and unfairness - meaning fairness can often be improved without materially sacrificing accuracy.

**Limitations:** Focuses primarily on gender as the sliced demographic variable; threshold-independence is a strength but ABROCA interpretation still requires care in low-base-rate settings.

**Relevance to this research:** Directly informs the prediction-reliability component of this research: the finding that fairness and accuracy are not inherently in tension supports the feasibility of the proposed group-wise directional-bias analysis without sacrificing overall reliability.

### \[20\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). Trustworthy AI in education: Framework, cases, and governance strategies. Innovation and Emerging Technologies, 12.

**IEEE citation:** Author(s) unverified, "Trustworthy AI in education: Framework, cases, and governance strategies," Innovation and Emerging Technologies, vol. 12, 2025.

**DOI / Link:** <https://doi.org/10.1142/S2737599425500264>

**Year:** 2025

**Venue:** Innovation and Emerging Technologies (World Scientific)

**Research objective:** Introduce a five-dimensional trust framework - privacy, safety, fairness, explainability, and accountability - to evaluate educational AI systems, validated through four case studies.

**Dataset characteristics:** Four case studies: a virtual teaching assistant, an adaptive learning platform, an algorithmic grading system, and an AI-based proctoring tool.

**Features used:** Not applicable in the predictive-modelling sense - a governance/case-analysis framework.

**Prediction model(s):** Not applicable.

**Explainability technique:** Explainability is one of the five core trust dimensions in the proposed framework, alongside privacy, safety, fairness, and accountability.

**Evaluation metrics:** Qualitative case-comparison rather than quantitative metrics.

**Key findings:** Recurring governance vulnerabilities identified across all four case types include insufficient human oversight, opaque decision-making, and ambiguous lines of accountability.

**Limitations:** Case-study methodology limits statistical generalisability; framework validation is illustrative rather than empirically tested at scale.

**Relevance to this research:** The five-dimension structure closely parallels this research's own three-pillar framework (trustworthy prediction, temporal explainability, responsible action), providing external validation for organising trustworthiness into discrete, addressable dimensions.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via publisher record before final citation._

# Theme 6 - Temporal Prediction and Longitudinal Learning Analytics

This theme reviews studies that explicitly model how student performance prediction changes across time - semester-wise, week-wise, or longitudinally - the most direct precedent for this study's RQ2 (temporal explainability).

### \[21\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). Predicting student next-term performance in degree programs using AI-based approach: A case study from Ghana. Cogent Education.

**IEEE citation:** Author(s) unverified, "Predicting student next-term performance in degree programs using AI-based approach: A case study from Ghana," Cogent Education, 2025.

**DOI / Link:** <https://doi.org/10.1080/2331186X.2025.2481000>

**Year:** 2025

**Venue:** Cogent Education (Taylor & Francis)

**Research objective:** Progressively predict semester-wise student performance across a full undergraduate degree programme using a temporal dynamic framework.

**Dataset characteristics:** 3,093 undergraduate Health Sciences students across eight semesters at a public university in Ghana, transformed into a time-series format.

**Features used:** Semester-wise academic performance indicators structured as sequential time-series data.

**Prediction model(s):** Four machine-learning methods compared, including BiLSTM and LSTM architectures explicitly designed to capture temporal dependencies.

**Explainability technique:** Not a stated focus; the emphasis is on temporal predictive accuracy rather than interpretability.

**Evaluation metrics:** Classification accuracy tracked per semester (e.g., BiLSTM improving from 62% at Semester 2 to 94% by Semester 6).

**Key findings:** Predictive accuracy improves substantially and consistently across semesters as more historical performance data accumulates, directly evidencing that prediction reliability is not constant over a student's academic journey.

**Limitations:** Uses only sequence models optimised for accuracy; does not analyse why accuracy improves (no feature-level temporal explanation), nor does it assess stability across repeated training runs.

**Relevance to this research:** Provides strong empirical precedent for RQ1 (the existence of a semester at which predictions become substantially more reliable) but stops short of RQ2 - explaining why - which is precisely the gap this research's Linear SHAP component addresses.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via the Taylor & Francis record before final citation._

### \[22\] Author(s) not fully confirmed (2024)

**APA citation:** Author(s) not fully confirmed. (2024). A method for prediction and analysis of student performance that combines multi-dimensional features of time and space. Mathematics, 12(22), 3597.

**IEEE citation:** Author(s) unverified, "A method for prediction and analysis of student performance that combines multi-dimensional features of time and space," Mathematics, vol. 12, no. 22, 3597, 2024.

**DOI / Link:** <https://doi.org/10.3390/math12223597>

**Year:** 2024

**Venue:** Mathematics (MDPI)

**Research objective:** Construct a spatiotemporal feature dataset (semester-stage performance plus place-of-origin educational indicators) and apply SHAP to identify which features matter most, and how.

**Dataset characteristics:** Multidimensional dataset combining student basic information, stage-wise semester performance, and regional/place-of-origin educational indicators.

**Features used:** Temporal features (performance at various semester stages) combined with spatial features (place-of-origin educational indicators) - structurally very similar to this research's district/province/Z-score variables.

**Prediction model(s):** Six machine-learning models trained and compared on the spatiotemporal dataset.

**Explainability technique:** SHAP analysis used explicitly to rank feature importance and to derive concrete teaching-strategy recommendations for educators.

**Evaluation metrics:** Predictive accuracy across the six compared models (specific figures not detailed in the available abstract).

**Key findings:** SHAP-derived importance rankings provide actionable guidance for two categories of educational strategy adjustment: student learning-behaviour interventions and teacher-side instructional adjustments, dynamically updated as the course progresses.

**Limitations:** Single-institution dataset; does not report cross-validated stability of the SHAP rankings themselves (i.e., whether importance rankings are stable if the model is retrained).

**Relevance to this research:** Closely mirrors this research's RQ2 in both structure (combining temporal and demographic/regional features) and method (SHAP for actionable ranking), making it one of the most directly comparable precedents identified in this review.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via the MDPI record before final citation._

### \[23\] Author(s) not fully confirmed (2014)

**APA citation:** Author(s) not fully confirmed. (2014). Predicting student risks through longitudinal analysis. In Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '14) (pp. 1544-1552). ACM.

**IEEE citation:** Author(s) unverified, "Predicting student risks through longitudinal analysis," in Proc. 20th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD '14), 2014.

**DOI / Link:** <https://doi.org/10.1145/2623330.2623355>

**Year:** 2014

**Venue:** Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '14)

**Research objective:** Use longitudinal, multi-year student data to predict dropout/at-risk status, building on earlier LMS-based early-warning-system foundations (e.g., Macfadyen & Dawson, 2010).

**Dataset characteristics:** Longitudinal, multi-year K-12/school-district student records (exact size not detailed in available abstract).

**Features used:** Longitudinal academic, attendance, and behavioural indicators tracked across multiple years.

**Prediction model(s):** Predictive risk-modelling approach benchmarked against prior EWS work (e.g., course-module-based key-predictor identification).

**Explainability technique:** Not addressed - pre-dates the widespread adoption of SHAP/LIME-style post-hoc explainability in EDM.

**Evaluation metrics:** Predictive accuracy of risk classification (specific figures not detailed in the available abstract).

**Key findings:** Confirms that longitudinal, multi-year data materially improves risk-prediction quality relative to single-snapshot approaches, an early and influential precedent for temporal/longitudinal EDM.

**Limitations:** An older (2014) study; lacks the explainability, fairness, and stability analyses now expected in contemporary trustworthy-AI-in-education research.

**Relevance to this research:** Historically important precedent establishing that longitudinal data collection strategy - not just modelling technique - is itself a key lever for prediction reliability, directly relevant to this research's semester-wise data design.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via the ACM Digital Library record before final citation._

### \[24\] Author(s) not fully confirmed (2025)

**APA citation:** Author(s) not fully confirmed. (2025). Predicting student academic performance using Bi-LSTM: A deep learning framework with SHAP-based interpretability and statistical validation. Frontiers in Education.

**IEEE citation:** Author(s) unverified, "Predicting student academic performance using Bi-LSTM: A deep learning framework with SHAP-based interpretability and statistical validation," Front. Educ., 2025.

**DOI / Link:** <https://doi.org/10.3389/feduc.2025.1581247>

**Year:** 2025

**Venue:** Frontiers in Education

**Research objective:** Combine a Bidirectional LSTM (Bi-LSTM) sequence model with SHAP-based interpretability and formal statistical validation for student performance prediction.

**Dataset characteristics:** Not fully detailed in available metadata; used to statistically compare Bi-LSTM against CatBoost, XGBoost, Hist Gradient Boosting, and LightGBM.

**Features used:** Sequential/temporal student performance and behavioural indicators.

**Prediction model(s):** Bi-LSTM (primary), benchmarked against CatBoost, XGBoost, Hist Gradient Boosting, and LightGBM.

**Explainability technique:** SHAP values used to interpret Bi-LSTM feature contributions, addressing the model's otherwise black-box temporal architecture.

**Evaluation metrics:** Accuracy (≈88.23%), plus precision, recall, and F1-score, with formal statistical significance testing across model comparisons.

**Key findings:** Bi-LSTM performance is statistically significantly different from (and superior to) the compared boosting methods on this dataset, and SHAP interpretation clarifies which features drive its temporal predictions.

**Limitations:** Explicitly notes that real-time updates and true time-series/temporal dynamics were not fully incorporated into the present framework, despite the sequential architecture.

**Relevance to this research:** Demonstrates growing convergence between temporal deep-learning models and SHAP-based interpretability, reinforcing that this research's simpler Ridge + Linear SHAP pairing achieves a comparable interpretability goal via a far more transparent and computationally lighter route.

**_⚠ Verification note:_** _Full author list not confirmed from the available search snippet; verify via the Frontiers record before final citation._

# 2\. Thematic Synthesis

Rather than repeating the paper-by-paper detail above, this section synthesises what the literature collectively shows within and across the six themes.

## 2.1 Learning Analytics and Educational Data Mining

The foundational LA/EDM literature (Romero & Ventura, 2020; Papamitsiou & Economides, 2014) consistently identifies performance prediction as the single most persistent task across both fields, regardless of how the LA/EDM boundary is drawn. More recent empirical comparisons (the topic-modelling study; the 2024 differences review) confirm that the conceptual distinction between LA and EDM has become 'a matter of degree rather than kind' in practice. This matters for framing: this research sits deliberately at the LA/EDM boundary, using EDM-style predictive techniques (Ridge Regression) in service of an explicitly LA-style goal (educational decision support), which the literature confirms is now the field's typical mode of work rather than an unusual hybrid.

## 2.2 Student Performance Prediction

The core prediction literature remains dominated by algorithm-comparison studies (Ahmed et al., 2024; Yadav & Deshmukh, 2023) that report a single accuracy figure per model with no discussion of stability, bias, or temporal change. Even the most recent 2026 comprehensive review confirms this pattern persists despite growing model sophistication (CNNs, GNNs, hybrid architectures) - accuracy remains the default and often sole evaluation lens, and interpretability is treated as a secondary, separable concern rather than integrated into the evaluation framework. The GPA-specific regression literature, however, directly supports the methodological choice of Ridge Regression: regularised linear models are shown to be highly competitive with more complex alternatives for GPA-style continuous targets while remaining transparent and stable under multicollinearity.

## 2.3 Early Warning Systems

EWS research treats 'earliness' primarily as a data-availability engineering problem - how little data, how early in a course, can support usable predictions (Digitus, 2025; the OULAD case studies) - rather than a reliability problem. Where reliability is addressed, it is usually through threshold calibration (the 2020 online-higher-education EWS paper) rather than through repeated-run stability or cross-semester consistency analysis. The most directly relevant recent paper (AI-Driven EWS, 2025) is a partial exception: it shows empirically that different models excel at different intervention stages and that static demographic features dominate early predictions - an important precedent for RQ1/RQ2, though it stops short of a formal reliability metric.

## 2.4 Explainable AI (SHAP)

SHAP has become the dominant explainability technique in recent education-prediction literature, consistently valued for its theoretical consistency (Lundberg & Lee, 2017) relative to alternatives such as LIME or ELI5 (as directly compared in the XAI-integration ScienceDirect paper). The XGB-SHAP (Wang & Luo, 2024) and spatiotemporal SHAP (Mathematics, 2024) studies both demonstrate - in different contexts (teaching mode; semester stage) - that SHAP-derived feature importance is context-dependent rather than fixed, directly supporting this research's premise that feature importance evolves across semesters. The Choi et al. (2026) SHAP-to-feedback paper is the closest existing precedent for translating explanations into actionable guidance, though at the level of individual student feedback rather than institutional confidence-tiered intervention policy.

## 2.5 Trustworthy and Responsible AI in Education

This theme most directly parallels the framing of the proposed research. Baker & Hawn (2022) and Gardner, Brooks & Baker (2019) together establish that (a) algorithmic bias in education is well-documented but unevenly studied across demographic groups, and (b) fairness and accuracy are not inherently in tension - meaning fairness-aware evaluation need not come at a meaningful accuracy cost. The Morales Tirado et al. (2024) operational Responsible AI framework and the five-dimension trust framework (2025) both independently converge on the idea that abstract trustworthiness principles must be decomposed into discrete, addressable dimensions to be actionable for institutions - precisely the design logic behind this research's own three-pillar structure (reliability, explainability, responsible action).

## 2.6 Temporal Prediction and Longitudinal Learning Analytics

The temporal/longitudinal literature provides the strongest direct empirical precedent for RQ1: the Ghana next-term-performance study shows accuracy climbing from roughly 62% at semester 2 to 94% by semester 6, and the 2014 KDD longitudinal-risk paper shows multi-year data materially outperforms single-snapshot prediction. However, none of the reviewed temporal studies combine (a) a formal, repeated-run reliability/stability metric, (b) SHAP-based explanation of why reliability changes over time, and (c) explicit translation into confidence-tiered educational guidance, in a single integrated framework. This is the most concrete evidence for the research gap this study addresses.

# 3\. Comparison Table Across Studies

The table below compares representative studies across the dimensions most relevant to positioning this research: whether reliability/stability (beyond a single accuracy figure) is assessed, whether explainability is used, whether fairness/bias across groups is assessed, and whether a temporal/longitudinal dimension is present.

| **Study**                                     | **Reliability / Stability**    | **Explainability**      | **Fairness / Bias**   | **Temporal Dimension**  | **Educational Decision Guidance** |
| --------------------------------------------- | ------------------------------ | ----------------------- | --------------------- | ----------------------- | --------------------------------- |
| Romero & Ventura (2020) - LA/EDM survey       | Discussed conceptually         | Noted as emerging       | Not central focus     | Not central focus       | General, not operational          |
| Ahmed et al. (2024) - ML algorithm comparison | No                             | No                      | No                    | No                      | No                                |
| Wang & Luo (2024) - XGB-SHAP                  | No                             | Yes (SHAP)              | No                    | Partial (teaching mode) | Partial (mode-specific)           |
| Choi et al. (2026) - SHAP feedback            | No                             | Yes (SHAP)              | No                    | No                      | Yes (individual feedback)         |
| Baker & Hawn (2022) - Algorithmic bias review | No                             | Discussed conceptually  | Yes (central focus)   | No                      | Policy-level                      |
| Gardner, Brooks & Baker (2019) - ABROCA       | No                             | No                      | Yes (ABROCA metric)   | No                      | No                                |
| Morales Tirado et al. (2024) - RAI framework  | Discussed conceptually         | One of 5 principles     | Yes (principle)       | No                      | Yes (operational framework)       |
| Ghana next-term study (2025) - semester-wise  | Partial (accuracy by semester) | No                      | No                    | Yes (8 semesters)       | No                                |
| Spatiotemporal SHAP (Mathematics, 2024)       | No                             | Yes (SHAP)              | No                    | Yes (semester stage)    | Yes (teaching strategy)           |
| AI-Driven EWS temporal (2025)                 | Partial (per-snapshot)         | Feature importance only | No                    | Yes (weekly snapshots)  | No                                |
| This proposed research                        | Yes (RMSE, stability, CV)      | Yes (Linear SHAP)       | Yes (group-wise bias) | Yes (semester-wise)     | Yes (confidence-tiered)           |

As the table illustrates, no single reviewed study combines all five dimensions in one framework. Studies typically strong on explainability (SHAP-based papers) are weak on reliability/stability and fairness; studies strong on fairness (Baker & Hawn; Gardner, Brooks & Baker) do not address temporal change; and studies strong on temporal analysis (Ghana study; spatiotemporal SHAP) do not formally assess prediction stability across repeated runs. This gap pattern is explored further below.

# 4\. Summary of Unresolved Research Gaps

### Gap 1 - Reliability treated as a single accuracy figure, not a multi-dimensional property

Across all six themes, the dominant evaluation pattern remains reporting one accuracy/R²/F1 figure per model. Very few studies report standard deviation across repeated cross-validation runs, and none of the reviewed studies combine accuracy, stability, and directional bias into a single reliability profile the way this research's RQ1 proposes.

### Gap 2 - Explainability and reliability are investigated separately

SHAP-based studies (Theme 4) rarely assess model stability, and reliability-focused studies rarely use SHAP. No reviewed paper explains why prediction reliability changes over time using SHAP - despite temporal SHAP shifts being independently documented in non-reliability contexts (teaching mode, spatiotemporal features).

### Gap 3 - Fairness analysis is rarely combined with temporal or reliability analysis

Baker & Hawn (2022) and Gardner, Brooks & Baker (2019) establish strong fairness-evaluation methodology, but neither - nor any other reviewed paper - applies group-wise fairness analysis across a temporal/semester-wise prediction sequence to see whether bias itself changes as more data accumulates.

### Gap 4 - Early warning research treats 'earliness' as a data-engineering problem, not a trust problem

EWS papers ask 'how little data can we use and still predict early?' rather than 'at what point are these early predictions reliable enough to justify an intervention?' This is a subtle but important reframing this research adopts.

### Gap 5 - Responsible/Trustworthy AI frameworks remain largely conceptual rather than empirically operationalised

The Responsible AI and five-dimension trust frameworks reviewed in Theme 5 provide strong conceptual scaffolding but are not paired with a concrete, empirically validated predictive pipeline demonstrating how confidence tiers should be derived from actual model outputs - the gap this research's Educational Decision Framework is designed to fill.

# 5\. Positioning the Proposed Framework Relative to the Literature

Based on the evidence gathered, the proposed Trustworthy Learning Analytics Group-aware Framework can be positioned as an integration contribution rather than a purely novel-technique contribution: each of its individual components (Ridge Regression for transparency, repeated cross-validation for stability, SHAP for explainability, group-wise analysis for fairness, semester-wise temporal design) has independent precedent in the literature reviewed above, but no single reviewed study combines all of them into one coherent reliability-to-explainability-to-action pipeline.

- Against Theme 2 (prediction studies): position as a deliberate move away from algorithm-competition toward reliability-first evaluation, using a simpler, more transparent model (Ridge) rather than the field's trend toward increasingly complex architectures.
- Against Theme 3 (EWS studies): reframe 'earliest usable semester' as a trustworthiness question rather than a pure data-availability question, directly extending the AI-Driven EWS (2025) temporal-snapshot approach with a formal reliability metric.
- Against Theme 4 (SHAP studies): extend single-context SHAP applications (teaching mode, spatiotemporal features) into an explicitly longitudinal, semester-by-semester explanatory sequence, and connect explanations to confidence tiers rather than only feature rankings.
- Against Theme 5 (Trustworthy/Responsible AI): operationalise the conceptual five-dimension / operational-RAI frameworks into a concrete, empirically testable pipeline grounded in an actual predictive model, addressing the 'framework without implementation' gap identified above.
- Against Theme 6 (temporal studies): add the missing reliability and fairness dimensions to existing semester-wise/longitudinal prediction designs, and formally test whether SHAP-identified explanatory shifts coincide with the semester(s) at which reliability crosses acceptable thresholds.

This positioning should be refined once the dissertation's related-work section is drafted in full, ideally after the flagged uncertain references are verified and after a small number of additional targeted searches (e.g., specifically for Sri Lankan / South Asian university GPA-prediction studies using district, province, and Z-score admission variables, which did not surface prominently in this search pass and may need a dedicated regional search).

# 6\. Reference List (IEEE Numbered Order)

**\[1\]** C. Romero and S. Ventura, "Educational data mining and learning analytics: An updated survey," WIREs Data Min. Knowl. Discov., vol. 10, no. 3, e1355, 2020.

**\[2\]** Z. Papamitsiou and A. A. Economides, "Learning analytics and educational data mining in practice: A systematic literature review of empirical evidence," J. Educ. Technol. Soc., vol. 17, no. 4, pp. 49-64, 2014.

**\[3\]** Author(s) unverified, "Reviewing the differences between learning analytics and educational data mining: Towards educational data science," Computers & Education, 2024.

**\[4\]** Author(s) unverified, "Comparison of learning analytics and educational data mining: A topic modeling approach," Computers and Education: Artificial Intelligence, vol. 2, 100034, 2021.

**\[5\]** M. Ahmed et al., "Student performance prediction using machine learning algorithms," Appl. Comput. Intell. Soft Comput., vol. 2024, Art. no. 4067721, 2024.

**\[6\]** N. R. Yadav and S. S. Deshmukh, "Prediction of student performance using machine learning techniques: A review," in Proc. ICAMIDA 2022, 2023, pp. 735-741.

**\[7\]** Author(s) unverified, "Predicting student performance: A comprehensive review of machine learning, deep learning, and explainable AI approaches," Computers and Education: Artificial Intelligence, 2026.

**\[8\]** Author(s) unverified, "High school student GPA prediction by various linear regression models," 2024.

**\[9\]** Author(s) unverified, "An early warning system to detect at-risk students in online higher education," 2020.

**\[10\]** Author(s) unverified, "ouladFormat R package: Preparing the Open University Learning Analytics Dataset for analysis," arXiv:2501.08366, 2025.

**\[11\]** Author(s) unverified, "AI-driven early warning systems for student success: Discovering static feature dominance in temporal prediction models," arXiv:2512.12493, 2025.

**\[12\]** Author(s) unverified, "Early prediction of at-risk students using minimal data: A machine learning framework for higher education," Digitus J. Comput. Sci. Appl., 2025.

**\[13\]** S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," in Adv. Neural Inf. Process. Syst. 30, 2017, pp. 4765-4774.

**\[14\]** S. Wang and B. Luo, "Academic achievement prediction in higher education through interpretable modeling," PLOS ONE, vol. 19, no. 9, e0309838, 2024.

**\[15\]** W.-C. Choi, I.-C. Choi, C.-T. Lam, and A. J. Mendes, "Explaining student performance prediction and generating personalized actionable feedback using XAI with SHAP," in Learning Technologies and Systems, LNCS vol. 16425, Springer, 2026.

**\[16\]** Author(s) unverified, "The integration of explainable AI in Educational Data Mining for student academic performance prediction and support system," 2025.

**\[17\]** A. Morales Tirado et al., "Towards an operational responsible AI framework for learning analytics in higher education," arXiv:2410.05827, 2024.

**\[18\]** R. S. Baker and A. Hawn, "Algorithmic bias in education," Int. J. Artif. Intell. Educ., vol. 32, no. 4, pp. 1052-1092, 2022.

**\[19\]** J. Gardner, C. Brooks, and R. Baker, "Evaluating the fairness of predictive student models through slicing analysis," in Proc. 9th Int. Conf. Learn. Anal. Knowl. (LAK'19), 2019, pp. 225-234.

**\[20\]** Author(s) unverified, "Trustworthy AI in education: Framework, cases, and governance strategies," Innovation and Emerging Technologies, vol. 12, 2025.

**\[21\]** Author(s) unverified, "Predicting student next-term performance in degree programs using AI-based approach: A case study from Ghana," Cogent Education, 2025.

**\[22\]** Author(s) unverified, "A method for prediction and analysis of student performance that combines multi-dimensional features of time and space," Mathematics, vol. 12, no. 22, 3597, 2024.

**\[23\]** Author(s) unverified, "Predicting student risks through longitudinal analysis," in Proc. 20th ACM SIGKDD Int. Conf. Knowl. Discov. Data Min. (KDD '14), 2014.

**\[24\]** Author(s) unverified, "Predicting student academic performance using Bi-LSTM: A deep learning framework with SHAP-based interpretability and statistical validation," Front. Educ., 2025.