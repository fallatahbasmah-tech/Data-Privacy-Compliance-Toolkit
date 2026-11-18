from collections import defaultdict
from questions import QUESTIONS, QUESTION_BY_CODE

def calculate(responses):
    """Educational weighted readiness index; N/A answers excluded from denominator."""
    answers = {r.code:r.answer for r in responses}
    groups = defaultdict(lambda: {'earned':0, 'possible':0, 'gaps':0})
    findings = []
    earned = possible = 0
    for q in QUESTIONS:
        answer = answers.get(q['code'], 'na')
        if answer == 'na': continue
        weight = q['weight']
        credit = weight if answer == 'yes' else weight * .5 if answer == 'partial' else 0
        earned += credit; possible += weight
        groups[q['category']]['earned'] += credit
        groups[q['category']]['possible'] += weight
        if answer != 'yes':
            groups[q['category']]['gaps'] += 1
            findings.append({**q,'answer':answer,'severity':'High' if weight==3 and answer=='no' else 'Medium' if weight>=2 else 'Low'})
    score = round(100*earned/possible,1) if possible else None
    categories = [{'name':name, 'score':round(100*g['earned']/g['possible'],1), 'gaps':g['gaps']}
                  for name,g in groups.items() if g['possible']]
    findings.sort(key=lambda f: (-f['weight'], f['answer']!='no'))
    return {'score':score, 'categories':categories, 'findings':findings,
            'answered':sum(a!='na' for a in answers.values()), 'total':len(QUESTIONS),
            'risk':'Not assessed' if score is None else 'High' if score<50 else 'Moderate' if score<80 else 'Lower'}
