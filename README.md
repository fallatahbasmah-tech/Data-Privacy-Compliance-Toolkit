# Data Privacy Compliance Toolkit

A **reconstructed, educational full-stack GDPR self-assessment application** inspired by the graduation project report *Data Privacy – A Compliance Toolkit* (especially Chapters 5–7 and Appendices A–B). **This is new implementation code, not the original submitted source code.**

## Features
- User registration, password hashing, sign-in and assessment ownership controls
- 35 GDPR-inspired questions across 6 categories (adapted from report Appendix A)
- Yes / Partially / No / N/A responses; weighted educational readiness scoring
- Prioritized gaps and suggested actions
- Assessment history and dashboard
- PDF and CSV report downloads
- SQLite by default; optional MySQL via SQLAlchemy connection URL
- CSRF protection, session-cookie settings, input validation, basic access controls
- Automated tests

## Run on Kali Linux

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
unzip Data_Privacy_Compliance_Toolkit_Full.zip
cd Data_Privacy_Compliance_Toolkit_Full
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python app.py
```

Open **http://127.0.0.1:5000** in Kali's browser. Register and start an assessment.

### Optional MySQL

1. Create a MySQL database and restricted application user.
2. Set `DATABASE_URL` to `mysql+pymysql://USERNAME:PASSWORD@localhost:3306/privacy_toolkit`.
3. Run `python app.py` to initialize tables automatically.

SQLite is provided for quick local use; the report's proposed MySQL database is supported through configuration.

### Tests

```bash
pytest -q
```

## Project structure

```
app.py             Flask routes, authentication, assessment, exports
models.py          Database models
questions.py       Question bank adapted from Appendix A
scoring.py         Educational scoring and risk logic
templates/         Web pages
static/            Styles and interaction
 tests/            Automated tests
```

## Scoring

Yes = 100% of question weight; Partially = 50%; No = 0%; N/A = excluded. Weights are 1–3. The risk bands are **illustrative**: High (<50), Moderate (50–79.9), Lower (80+). These thresholds are **not GDPR legal thresholds**. Responses are self-reported; a high score does not prove compliance.

## Source alignment and limitations

- The source report specifies Python, Flask, HTML/CSS/JavaScript, questionnaire, weighted risk analysis, database storage and PDF/CSV reports.
- Question codes and themes are adapted from the report's Appendix A; wording has been shortened and some detailed branching has been flattened for usability.
- The source Appendix B contains earlier implementation examples; this project is a fresh implementation, not a verbatim extraction.
- No consent management platform, automated legal decision engine, formal DPIA workflow, or independent security audit is claimed.
- For production deployment: use HTTPS, a strong `SECRET_KEY`, secure cookies, database migrations, rate limiting, backups, logging, secret management, and a privacy/data retention policy. Do not upload real personal data to a public demo.

## License

Educational demonstration; adapt and review before any real-world use.
