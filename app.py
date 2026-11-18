"""Data Privacy Compliance Toolkit — educational GDPR self-assessment."""
import os, csv, io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort, Response as FlaskResponse, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import select
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape
from models import db, User, Assessment, Response
from questions import QUESTIONS, CATEGORIES, QUESTION_BY_CODE
from scoring import calculate

login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY','dev-only-change-me'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL','sqlite:///privacy_toolkit.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False, MAX_CONTENT_LENGTH=1024*1024,
        SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
    if test_config: app.config.update(test_config)
    db.init_app(app); login_manager.init_app(app); csrf.init_app(app)
    login_manager.login_view = 'login'
    with app.app_context(): db.create_all()

    @app.route('/')
    def index(): return render_template('index.html', question_count=len(QUESTIONS))

    @app.route('/about')
    def about(): return render_template('about.html')

    @app.route('/register', methods=['GET','POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email','').strip().lower()
            password = request.form.get('password','')
            if '@' not in email or len(email)>255 or len(password)<10:
                flash('Enter a valid email and password of at least 10 characters.', 'error')
            elif db.session.scalar(select(User).where(User.email==email)):
                flash('An account with that email already exists.', 'error')
            else:
                user=User(email=email); user.set_password(password)
                db.session.add(user); db.session.commit(); login_user(user)
                return redirect(url_for('dashboard'))
        return render_template('auth.html', mode='register')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email=request.form.get('email','').strip().lower()
            user=db.session.scalar(select(User).where(User.email==email))
            if user and user.check_password(request.form.get('password','')):
                login_user(user); return redirect(url_for('dashboard'))
            flash('Invalid email or password.', 'error')
        return render_template('auth.html', mode='login')

    @app.route('/logout', methods=['POST'])
    @login_required
    def logout(): logout_user(); return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        assessments=db.session.scalars(select(Assessment).where(Assessment.user_id==current_user.id).order_by(Assessment.created_at.desc())).all()
        summaries=[(a,calculate(a.responses)) for a in assessments]
        return render_template('dashboard.html', summaries=summaries)

    @app.route('/assessment/new', methods=['GET','POST'])
    @login_required
    def assessment_new():
        if request.method == 'POST':
            org=request.form.get('organization','').strip()[:160]
            industry=request.form.get('industry','').strip()[:80]
            employees=request.form.get('employees','').strip()[:40]
            if not org or not industry or not employees:
                flash('Complete the organization information.', 'error')
            else:
                answers={q['code']:request.form.get('q_'+q['code']) for q in QUESTIONS}
                if any(v not in ('yes','partial','no','na') for v in answers.values()):
                    flash('Please answer all assessment questions.', 'error')
                else:
                    a=Assessment(user_id=current_user.id, organization=org,industry=industry,employees=employees)
                    db.session.add(a); db.session.flush()
                    db.session.add_all([Response(assessment_id=a.id,code=code,answer=value) for code,value in answers.items()])
                    db.session.commit()
                    return redirect(url_for('assessment_detail',assessment_id=a.id))
        return render_template('assessment.html', categories=CATEGORIES, questions=QUESTIONS)

    def owned_assessment(assessment_id):
        a=db.session.get(Assessment,assessment_id)
        if a is None or a.user_id!=current_user.id: abort(404)
        return a

    @app.route('/assessment/<int:assessment_id>')
    @login_required
    def assessment_detail(assessment_id):
        a=owned_assessment(assessment_id)
        return render_template('results.html', assessment=a, result=calculate(a.responses), answers={r.code:r.answer for r in a.responses}, questions=QUESTIONS)

    @app.route('/assessment/<int:assessment_id>/delete', methods=['POST'])
    @login_required
    def assessment_delete(assessment_id):
        a=owned_assessment(assessment_id); db.session.delete(a); db.session.commit()
        flash('Assessment deleted.', 'success'); return redirect(url_for('dashboard'))

    @app.route('/assessment/<int:assessment_id>/csv')
    @login_required
    def assessment_csv(assessment_id):
        a=owned_assessment(assessment_id); output=io.StringIO(); writer=csv.writer(output)
        writer.writerow(['Organization',a.organization]); writer.writerow(['Date',a.created_at.isoformat()]); writer.writerow([])
        writer.writerow(['Code','Category','Question','Answer','Importance','Recommendation'])
        answers={r.code:r.answer for r in a.responses}
        for q in QUESTIONS:
            writer.writerow([q['code'],q['category'],q['text'],answers.get(q['code'],'na'),q['weight'],q['recommendation']])
        result=calculate(a.responses)
        writer.writerow([]);writer.writerow(['Educational readiness score',result['score'] if result['score'] is not None else 'N/A'])
        return FlaskResponse('\ufeff'+output.getvalue(),mimetype='text/csv',headers={'Content-Disposition':f'attachment; filename="assessment_{a.id}.csv"'})

    @app.route('/assessment/<int:assessment_id>/pdf')
    @login_required
    def assessment_pdf(assessment_id):
        a=owned_assessment(assessment_id); result=calculate(a.responses)
        buffer=io.BytesIO(); doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42)
        styles=getSampleStyleSheet(); story=[Paragraph('Data Privacy Compliance Toolkit',styles['Title']),Spacer(1,14),
            Paragraph('GDPR Self-Assessment Report (Educational)',styles['Heading2']),
            Paragraph('Organization: '+escape(a.organization),styles['Normal']),
            Paragraph('Date: '+a.created_at.strftime('%Y-%m-%d'),styles['Normal']),
            Paragraph('Readiness score: '+(str(result['score'])+'%' if result['score'] is not None else 'Not assessed'),styles['Normal']),
            Paragraph('Indicative risk: '+result['risk'],styles['Normal']),Spacer(1,16),
            Paragraph('Category summary',styles['Heading2'])]
        table=Table([['Category','Readiness','Gaps']]+[[c['name'],str(c['score'])+'%',str(c['gaps'])] for c in result['categories']],colWidths=[270,100,70],repeatRows=1)
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#152b43')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.3,colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),8)])); story.append(table)
        story.extend([Spacer(1,18),Paragraph('Priority recommendations',styles['Heading2'])])
        for f in result['findings']:
            story.append(Paragraph(escape(f['code']+' — '+f['severity']+': '+f['text']),styles['Normal']))
            story.append(Paragraph('Action: '+escape(f['recommendation']),styles['Italic']));story.append(Spacer(1,9))
        story.extend([Spacer(1,12),Paragraph('Disclaimer: This is a self-reported educational readiness index, not a legal GDPR compliance determination or certification.',styles['Italic'])])
        doc.build(story);buffer.seek(0)
        return send_file(buffer,mimetype='application/pdf',as_attachment=True,download_name=f'assessment_{a.id}.pdf')

    return app

@login_manager.user_loader
def load_user(user_id):
    try: return db.session.get(User,int(user_id))
    except (TypeError,ValueError): return None

app=create_app()
if __name__=='__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG')=='1',host='127.0.0.1')
