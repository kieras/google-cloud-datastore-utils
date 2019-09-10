# Google Cloud Datastore Utils

Utilities for Google Cloud Datastore.

Supported commands:

- **export**: Export entities from any project/namespace to a file.
- **import**: Import entities from a file into any project/namespace.

## Installation

Simply run:

```bash
pipsi install gcdu
```

---

## Usage

To use it:

```bash
gcdu --help
```

Export command:

```bash
gcdu export -p [project] -n [namespace] -k [comma separated list of datastore kinds]
```

Import command:

```bash
gcdu import -p [project] -n [namespace] -k [comma separated list of datastore kinds]
```

## Authentication

You can execute the program with your user authenticated in the using `gcloud`:

```bash
gcloud auth application-default login
gcloud config set project PROJECT_ID
```

If you want, you can use a Service Account to authenticate by exporting the following variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS='service-account-key.json'
```

## Example execution of an import

```bash
gcdu import --project my-project-stage --namespace e2e-20190313-192340 --data-dir=resources/database --kinds=AuditLog,Budget,BudgetBigqueryIntegration,BudgetChannel,BudgetCostCenter,BudgetEntity,BudgetGLCode,BudgetLocation,BudgetProduct,CurrencyCode,CurrencyEntity,Entry,FeatureToggle,LoadVersionControl,Settings,Submission,SubmissionForEmailCron,SubmissionLinePreview,SubmissionSequence,Team,Template,Transaction,User,Checkpoint,CostCenter,Header,OptionEntry,Question,QuestionAlias,BudgetQuarterSnapshot
Executing import. Project=my-project-stage, Namespace=e2e-20190313-192340, Kinds=[u'AuditLog', u'Budget', u'BudgetBigqueryIntegration', u'BudgetChannel', u'BudgetCostCenter', u'BudgetEntity', u'BudgetGLCode', u'BudgetLocation', u'BudgetProduct', u'CurrencyCode', u'CurrencyEntity', u'Entry', u'FeatureToggle', u'LoadVersionControl', u'Settings', u'Submission', u'SubmissionForEmailCron', u'SubmissionLinePreview', u'SubmissionSequence', u'Team', u'Template', u'Transaction', u'User', u'Checkpoint', u'CostCenter', u'Header', u'OptionEntry', u'Question', u'QuestionAlias', u'BudgetQuarterSnapshot'].
Starting tasks...
Done. 30 tasks started.
Executing...
Done. Kind=Template
Done. Kind=Header
Done. Kind=LoadVersionControl
Done. Kind=Question
Done. Kind=BudgetEntity
Done. Kind=Checkpoint
Done. Kind=User
Done. Kind=BudgetLocation
Done. Kind=Settings
Done. Kind=BudgetCostCenter
Done. Kind=FeatureToggle
Done. Kind=BudgetChannel
Done. Kind=BudgetGLCode
Done. Kind=Team
Done. Kind=BudgetProduct
Done. Kind=OptionEntry
Done. Kind=CostCenter
Done. Kind=Budget
Done. Kind=QuestionAlias
Done. Kind=Transaction
Done. Kind=CurrencyEntity
Done. Kind=CurrencyCode
Done. Kind=SubmissionSequence
Done. Kind=BudgetQuarterSnapshot
Done. Kind=SubmissionForEmailCron
Done. Kind=SubmissionLinePreview
Done. Kind=Submission
Done. Kind=AuditLog
Done. Kind=Entry
Done. Kind=BudgetBigqueryIntegration
Finished!
```

Notice that we previously exported the database (not shown here), and now we are importing it into another project and namespace.

Another nice thing is that export/import executes in parallel, starting a task for each entity separately.
