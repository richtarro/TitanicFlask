import urllib3, requests, json, os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField
from wtforms.validators import Required, Length, NumberRange


app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = 'my top secret secret'
bootstrap = Bootstrap(app)

class SurvivorForm(FlaskForm):
    Pclass = RadioField('Ticket class', coerce=int, choices=[(1, 'Upper'),(2 ,'Middle'),(3, 'Lower')])
    Sex = RadioField('Gender', coerce=str, choices=[('male', 'Male'),('female' ,'Female')])
                                                     
    Age = FloatField('Age in years', validators=[NumberRange(1,100)])
    SibSp = IntegerField('Number of siblings/spouses aboard', validators=[NumberRange(1,)])
    Parch = IntegerField('Number of parents/children aboard', validators=[NumberRange(1,)])
    Fare = FloatField('Passenger fare (in British Pounds)', validators=[NumberRange(1,870)])
    Embarked = RadioField('Port of Embarkation', coerce=str, choices=[('C', 'Cherbourg'),('Q' ,'Queenstown'),('S','Southampton')])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    
    #result = None
    #response_scoring = None
    form = SurvivorForm()
    #if request.method == 'POST':
    if form.validate_on_submit():
        Pclass = form.Pclass.data
        form.Pclass.data = ''
        Sex = form.Sex.data
        form.Sex.data = ''
        Age = form.Age.data
        form.Age.data = ''
        SibSp = form.SibSp.data
        form.SibSp.data = ''
        Parch = form.Parch.data
        form.Parch.data = ''
        Fare = form.Fare.data
        form.Fare.data = ''
        Embarked = form.Embarked.data
        form.Embarked.data = ''
        
        service_path = 'https://ibm-watson-ml.mybluemix.net'
        username = '81d30f85-f4bb-4e42-adc2-6278cc383065'
        password = '5ec1a485-102a-4008-a41a-64dd048e3d5e'

        headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
        url = '{}/v2/identity/token'.format(service_path)
        response = requests.get(url, headers=headers)
        mltoken = json.loads(response.text).get('token')

        header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
        scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/1724"
        payload_scoring = {"record":[Pclass, Sex, Age, SibSp, Parch, Fare, Embarked]}

        response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
        result = response_scoring.text
        
        data = request.form

        return render_template('score.html', form=form, result=result, data=data, response_scoring=response_scoring)
    
    return render_template('index.html', form=form)
    
    
@app.route('/scoretest', methods=['GET', 'POST'])
def scoretest():
    
    service_path = 'https://ibm-watson-ml.mybluemix.net'
    username = '81d30f85-f4bb-4e42-adc2-6278cc383065'
    password = '5ec1a485-102a-4008-a41a-64dd048e3d5e'

    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    url = '{}/v2/identity/token'.format(service_path)
    response = requests.get(url, headers=headers)
    mltoken = json.loads(response.text).get('token')
    header_online = {'Content-Type': 'application/json', 'Authorization': mltoken}
    scoring_href = "https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/1724"
    payload_scoring = {"record":[2, 'female', 40.0, 1, 1, 15.0, "C"]}
    
    response_scoring = requests.put(scoring_href, json=payload_scoring, headers=header_online)
    
    result = response_scoring.text
    return render_template('scoretest.html', result=result, response_scoring=response_scoring)
    


#if __name__ == '__main__':
#	app.run(debug=True)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
