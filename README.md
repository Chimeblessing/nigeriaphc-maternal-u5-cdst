# nigeriaphc-maternal-u5-cdst
Android tablet CDST for maternal and under-5 triage in PHCs, with AI recommendations

# Maternal & Under-5 Triage CDST
## Overview
Android tablet Clinical Decision Support Tool (CDST) for maternal and under-5 triage in primary health care centers (PHCs).

Generates AI-assisted recommendations for:
- Urgent referral
- Monitoring
- PHC management

## Repository Structure
/docs — project documentation  
/android-app — Android project code  
/backend-api — backend API code  

## Team
- Clinical advisor
- Developers: Backend + Frontend
- Producer: Jeremiah Ngene: Founder - Axton-Vent Initiatives For Ethics And Moral Values And Building Families LTD/GTE and Axton-Vent Ethical Leadership School.
 
## 1. Data Collection & Preprocessing
### Data Collection
The MaternalU5Triage AI system will integrate multi-source datasets to enable predictive modeling of maternal and under-five health risks. The system will combine public health indicators, anonymized clinical records, and genomic datasets to build a comprehensive AI training dataset.

#### Public Health Datasets
Population-level maternal and child health indicators will be obtained from international health data repositories, including:
- World Health Organization Global Health Observatory
- UNICEF Data Warehouse
- World Bank Health Indicators Database
- Demographic and Health Surveys Program (DHS)
- Multiple Indicator Cluster Surveys (MICS)

**Key indicators include:**
- Maternal mortality ratio
- Under-five mortality rate
- Neonatal mortality rate
- Antenatal care coverage
- Skilled birth attendance
- Postnatal care coverage
- Childhood vaccination coverage
- Maternal nutrition indicators
- Child growth and nutrition indicators

These datasets will provide population-level predictors and contextual determinants of maternal and child health outcomes.

Current Release field validation v1.3 from v1.0 clinical validation.
Citation:
Ngene, J. (2026). MaternalU5Triage v1.0 Pilot 2024-2025: Clinical Validation in 12 PHCs Enugu State, Nigeria - Correct Triage and Referral Completion Outcomes (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.23009967   
and Demand Registry: https://docs.google.com/spreadsheets/d/1-3BXMfXPU--t0ns9UUacAq9mTw_qZpznhe8C9M4KCNU/edit?gid=0#gid=0
---
#### Clinical Datasets
Anonymized clinical datasets will be used to capture patient-level variables relevant to maternal and neonatal outcomes.
**Sources include:**
- Public clinical trial repositories
- Open electronic health record datasets
- Maternal and neonatal health registries
- Hospital datasets shared under ethical approval
**Key clinical variables include:**
- Maternal age
- Parity and obstetric history
- Blood pressure measurements
- Hemoglobin levels
- Pregnancy complications (e.g., preeclampsia, gestational diabetes)
- Delivery type and birth outcomes
- Neonatal birth weight
- Apgar scores
- Neonatal complications

All patient data will be fully anonymized and de-identified to comply with ethical and privacy standards.

#### Genomic and Biological Datasets
To support AI-driven biomedical discovery, the system will incorporate open biological and genomic datasets relevant to maternal and neonatal health.
**Sources include:**
- National Center for Biotechnology Information (NCBI) genomic repositories
- European Genome-phenome Archive
- UK Biobank (open-access datasets where available)

**Relevant biological data may include:**
- Gene variants associated with pregnancy complications
- Genetic markers related to neonatal disorders
- Proteomic and biomarker datasets
- Phenotypic measures related to maternal and child health
These datasets support the development of AI models capable of identifying biological patterns linked to maternal and neonatal risk factors.
### Data Preprocessing
Before training AI models, all datasets will undergo rigorous preprocessing and harmonization to ensure quality and interoperability.
#### Data Cleaning
The following preprocessing procedures will be applied:
- Removal of duplicate records
- Handling missing values using statistical imputation methods
- Detection and correction of inconsistent or erroneous entries
- Standardization of units and measurement formats
#### Data Standardization
To allow integration across multiple datasets:
- Variables will be normalized to consistent units
- Health indicators will be mapped to standardized clinical terminology
- Categorical variables will be encoded using machine-readable formats
#### Data Anonymization
All patient-level datasets will undergo strict privacy protection procedures:
- Removal of personally identifiable information
- De-identification of patient identifiers
- Compliance with global ethical standards for health data research
#### Data Integration
After preprocessing, datasets will be merged into a unified AI training dataset containing:
- Demographic variables
- Clinical health indicators
- Public health contextual data
- Biological and genomic features
- ## 2. Feature Engineering
Feature engineering is a critical step in the development of the MaternalU5Triage AI system, as it transforms raw datasets into structured variables that can be used effectively by machine learning models to predict maternal and under-five health risks. The system will derive meaningful predictors from integrated public health, clinical, and biological datasets to improve the accuracy of AI-based triage and early warning systems.
### Identification of Key Risk Factors
Key predictive variables will be extracted from the collected datasets based on established maternal and child health research. These variables represent known determinants of maternal complications, neonatal outcomes, and under-five mortality.
**The main categories of risk factors include:**
#### Maternal Demographic Factors
- Maternal age
- Parity (number of previous births)
- Maternal education level
- Household socioeconomic status
- Geographic location (urban or rural)
#### Pre-Existing Medical Conditions
- Hypertension
- Diabetes mellitus
- Anemia
- Obesity or malnutrition
- Previous obstetric complications
#### Pregnancy and Birth Complications
- Preeclampsia or eclampsia
- Gestational diabetes
- Preterm labor
- Prolonged labor
- Cesarean delivery
- Postpartum hemorrhage
#### Neonatal and Child Health Indicators
- Birth weight
- Gestational age at delivery
- Apgar score
- Neonatal infections
- Immunization status
#### Environmental and Social Determinants
- Air pollution exposure
- Household sanitation conditions
- Access to clean drinking water
- Climate and seasonal factors
- Distance to health facilities
These variables form the core predictive features used by the MaternalU5Triage AI models.
### Generation of Derived Features
In addition to raw variables, the system will compute derived features that capture complex interactions between health indicators and environmental conditions. Derived features improve model performance by summarizing multiple risk factors into meaningful indices.
**Examples include:**
#### Maternal Comorbidity Score
A composite score representing the combined burden of maternal health conditions, calculated from variables such as:
- Hypertension
- Diabetes
- Anemia
- Previous pregnancy complications
#### Maternal Nutrition Index
An index calculated using indicators such as:
- Body Mass Index (BMI)
- Hemoglobin levels
- Dietary diversity indicators
- Micronutrient deficiencies
#### Neonatal Risk Index
A derived score combining early life indicators including:
- Low birth weight
- Premature birth
- Neonatal infection markers
- Apgar score
#### Environmental Exposure Metrics
Environmental risk indicators derived from geospatial and environmental datasets, including:
- Air pollution levels (PM2.5 exposure)
- Heat stress or extreme temperature exposure
- Flood or climate vulnerability indicators
### Data Transformation for Machine Learning
After generating raw and derived features, the following transformations will be applied:
- Encoding categorical variables using label or one-hot encoding
- ## Mobile Application Interface
The MaternalU5Triage system includes a mobile application used by frontline health workers to collect maternal and child health data and receive AI-assisted triage guidance.
![MaternalU5Triage Workflow](docs/MaternalU5Triage_Workflow.png) 
 ## Mobile Application Interface
### App Home Screen
![App Home Screen](docs/app-home-screen.jpg)
### Clinical Triage Guidance
![Patient Data Entry](docs/android-app-demo.jpg)
### AI Risk Prediction
![AI Risk Result](docs/ai-risk-result.jpg)
### Patient Data Entry
![Triage Advice](docs/triage-advice-screen.jpg)
### Development Environment
![Android Development](docs/android-development-environment.jpg)
## Quick Demo Workflow
The MaternalU5Triage system operates through a simple workflow designed for frontline health workers in primary healthcare facilities.
1. **Health Worker Opens the Mobile App**
   The MaternalU5Triage application is launched on an Android device.
2. **Patient Data Entry**
   Maternal and child health indicators such as age, symptoms, and vital signs are entered.
3. **AI Risk Assessment**
   Machine learning models analyze the data to detect possible maternal or child health risks.
4. **Clinical Decision Support**
   The system provides risk alerts and triage recommendations.
5. **Referral or Immediate Care**
   Health workers take appropriate action based on the AI-supported guidance.
## Repository Structure
nigeriaphc-maternal-u5-cdst
│
├── README.md                     # Project overview
├── models/                       # AI models
├── scripts/                      # Data processing scripts
├── data/                         # Sample datasets
└── docs/                         # Documentation and system diagrams
    ├── README.md
    ├── system_architecture.md
    ├── MaternalU5Triage_Workflow.png
    ├── app-home-screen.jpg
    ├── android-app-demo.jpg
    ├── ai-risk-result.jpg
    ├── triage-advice-screen.jpg
    └── android-development-environment.jpg
```
- Normalization of continuous variables
- Feature scaling to improve model convergence
- Removal of highly correlated or redundant variables
The resulting feature dataset will be stored in the **features layer** of the cloud data pipeline, where it becomes the input for AI model training and evaluation.


Maternal & Under-5 Triage CDST v1.0 Android Clinical Decision Support Tool for PHC triage in Nigeria
License: MIT 
Status: Field Pilot Developed by: Axton-Vent Initiatives AVI + Enugu SPHCDA
Funding: Pilot funded by Axton-Vent Initiatives AVI | Open source, no commercial dependencies
Overview: Tablet-based triage tool for CHEWs at PHCs to standardize maternal and under-5 triage. Addresses high mortality from delayed referral (114/1000 under-5 mortality in Nigeria) (NBS, 2023).Generates AI-assisted recommendations:RED: Urgent referral YELLOW: Monitoring + re-assessment in 30 mins GREEN: PHC management Field Evidence (v1.0)12 PHCs in Enugu State, Nigeria (Jun 2024 - Aug 2025)12,340 encounters triaged (7,200 U5, 5,140 maternal)98.2% concordance with clinician gold standard (kappa 0.82)Referral time: Reduced from 48 mins to 12 mins
Repository Structure
/docs - Clinical protocol, data dictionary, SOPs
/android-app - Android app (Kotlin, offline-first)
/backend-api - API + AI triage engine (Python/FastAPI)
/validation - Retrospective validation dataset (de-identified)
Installation
# Android
Open /android-app in Android Studio Hedgehog+ / Build APK

# Backend
cd backend-api && pip install -r requirements.txt && uvicorn main:app --reload

Data & Ethics
No PHI in repo. All data de-identified per NDPR.Ethics: Enugu State Health Research Ethics Committee (ESHEC/2024/011)DHIS2 compatible — FHIR JSON export
Roadmap v1.0 to Field platform completed (current release)v1.3: RCT 100 PHCs for Stage 2 v1.3: Integration with ESPHCDA/NPHCDA national platform. 
Citation: Ngene, J. (2026). MaternalU5Triage v1.0 Pilot 2024-2025: Clinical Validation in 12 PHCs Enugu State, Nigeria - Correct Triage and Referral Completion Outcomes (Version 1.0). Zenodo. https://doi.org/10.5281/zenodo.23009967  


































































