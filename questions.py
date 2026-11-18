"""Question bank adapted from Appendix A of the graduation project report.
Wording shortened for UI; this is a reconstructed educational implementation.
"""
CATEGORIES = {
 'Consent & lawful basis': [
 ('2.2.1','Are consent requests freely given, specific, informed and unambiguous?',3,'Document consent language, legal basis and affirmative opt-in.'),
 ('2.2.1.1','Can your organization demonstrate when and how consent was obtained?',3,'Maintain auditable consent records.'),
 ('2.2.1.1.1','Can individuals withdraw consent as easily as they gave it?',3,'Provide and test a withdrawal process.'),
 ('2.2.2','Have existing consent records been reviewed against GDPR standards?',2,'Audit legacy consent records.'),
 ('2.2.2.1','Is renewed consent obtained where older consent is insufficient?',3,'Re-collect consent where required.'),
 ('2.3.1.1','Where children use services, are age and guardian consent controls in place?',3,'Implement age-appropriate consent safeguards.'),
 ],
 'Data subject rights': [
 ('3.1.1.1','Can you respond to access requests within the applicable deadline?',3,'Establish a tracked subject-access workflow.'),
 ('3.2','Can individuals request correction of inaccurate personal data?',2,'Provide a rectification request process.'),
 ('3.3','Can individuals request erasure when applicable?',3,'Document erasure eligibility and execution.'),
 ('3.4','Can processing be restricted when required?',2,'Create a restriction workflow.'),
 ('3.5.1.1','Can processing stop when a valid objection is received?',3,'Track and enforce objections.'),
 ('3.6','Can you provide personal data in a portable format where required?',2,'Implement structured data export.'),
 ],
 'Accuracy & retention': [
 ('4.1.1','Is personal data used only for documented purposes?',3,'Review processing purposes and compatibility.'),
 ('4.2.1','Is collection limited to data necessary for each purpose?',3,'Minimize collected data fields.'),
 ('4.3.1','Are records kept accurate and up to date?',2,'Establish accuracy checks and correction procedures.'),
 ('4.4.1','Are retention periods documented and enforced?',3,'Publish and enforce a retention schedule.'),
 ('4.5.2','Is personal data securely destroyed at the end of retention?',3,'Document secure deletion and disposal.'),
 ('4.6.1','Are duplicate or unnecessary records identified and removed?',1,'Schedule data inventory and deduplication.'),
 ],
 'Transparency': [
 ('5.1.1','Are customers and employees clearly informed how data is used?',3,'Publish clear, accessible privacy notices.'),
 ('5.2','Is required privacy information supplied when data is collected directly?',3,'Show collection-time privacy information.'),
 ('5.3','Is privacy information provided when data comes from third parties?',2,'Add third-party collection notice procedures.'),
 ('5.4','Is privacy information easy to find at the point of interaction?',2,'Link notices prominently in all collection flows.'),
 ('5.5','Are individuals told how to exercise their privacy rights?',2,'Provide a rights-request contact and instructions.'),
 ],
 'Governance & DPIA': [
 ('6.1.1','Are processor and supplier data protection agreements in place?',3,'Review and update data processing agreements.'),
 ('6.1.3','Has the need to appoint a Data Protection Officer been assessed?',2,'Document the DPO applicability assessment.'),
 ('6.1.3.1','If no DPO is appointed, is that decision documented?',1,'Record the reasoning for the DPO decision.'),
 ('6.1.3.1.2','Where appointed, are DPO contact details published?',2,'Publish DPO contact details as appropriate.'),
 ('6.2.1','Is a DPIA performed for processing likely to be high risk?',3,'Create a DPIA screening and review process.'),
 ],
 'Data security': [
 ('7.1.1','Have risks to personal data been assessed and mitigated?',3,'Maintain a documented privacy risk register.'),
 ('7.1.2','Is there a documented technical and organizational security program?',3,'Define and review security policies and controls.'),
 ('7.1.3','Is there a process for investigating security complaints?',2,'Introduce a security complaint handling workflow.'),
 ('7.1.4','Is someone responsible for investigating security incidents?',3,'Assign incident response ownership.'),
 ('7.1.5','Is appropriate encryption used in transit and at rest?',3,'Review encryption and key management.'),
 ('7.1.6','Is personal data securely erased or anonymized when no longer needed?',3,'Implement verified deletion or anonymization.'),
 ('7.1.7','Can access to personal data be restored after an incident?',3,'Test backups and recovery procedures.'),
 ],
}
QUESTIONS = [dict(code=code, text=text, weight=weight, recommendation=rec, category=category)
             for category, entries in CATEGORIES.items() for code,text,weight,rec in entries]
QUESTION_BY_CODE = {q['code']:q for q in QUESTIONS}
