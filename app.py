from flask import Flask, request, make_response, jsonify, session
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import requests
import markdown
import fitz
import re

# Initialize Flask application
app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Configure SQLAlchemy database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'jdhfhufhuishuhuihufhu'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = "myauthkey"
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "myauthtoken"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

#----database models---
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name= db.Column(db.String,nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    password= db.Column(db.String,nullable=False)
    role = db.Column(db.String, nullable=False)
    enrolled_courses = db.relationship('Enrollment', backref='user', lazy='subquery',cascade='all, delete-orphan')

class Course(db.Model):
    __tablename__="course"
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String, nullable=False)
    enrolled_students = db.relationship('Enrollment', backref='course', lazy='subquery',cascade='all, delete-orphan')
    weeks = db.relationship('Week', backref='course', lazy='subquery', cascade='all, delete-orphan')

class Enrollment(db.Model):
    __tablename__="enrollment"
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'course_id'),)

class Week(db.Model):
    __tablename__="week"
    week_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    week_no=db.Column(db.Integer,nullable=False)
    links = db.relationship('Link', backref='week', lazy='subquery', cascade='all, delete-orphan')

class Link(db.Model):
    __tablename__='link'
    link_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    week_id=db.Column(db.Integer, db.ForeignKey('week.week_id'), nullable=False)
    link_order=db.Column(db.Integer,nullable=False)
    url=db.Column(db.String,nullable=False)

# db.create_all()

#-----------API Controllers-----------

class PDFtoText(Resource):
    @staticmethod
    def clean_text(text):
        # Remove all non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', '', text)
        # Remove all HTML tags
        text = re.sub(r'<.*?>', '', text)
        # Replace multiple spaces or newlines with a single space
        text = re.sub(r'\s+', ' ', text).strip()
        #print("clean_text called"+text)
        return text

    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file uploaded'}, 400

        file = request.files['file']


        file_ext = file.filename.split('.')[1]

        if file_ext != 'pdf':
            return {'error': 'Incorrect File Type'}, 400

        if file:
            try:
                pdf_document = fitz.open(stream=file.read(), filetype="pdf")
                text = ""
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    text += page.get_text()

                    print(self.clean_text(text))
                return jsonify({'text': self.clean_text(text)})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        return {'error': 'File upload failed'}, 400


class YTSummary(Resource):
    def get(self):
        url = request.args.get('video_url')
        if not url:
            return {'message': 'Missing video_url'}, 400
        vid=extract.video_id(url)
        srt = YouTubeTranscriptApi.get_transcript(vid)
        subtitles=[]
        for i in srt:
            subtitles.append(i['text'])
        full_srt = "\n".join(subtitles)

        if full_srt:
            return { 'summary' : full_srt }, 200
        else:
            return {'message' : 'failed to fetch transcript'},401

        '''

        if full_srt:

            api_key = "Your-API-Key-Here"
            url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key="+api_key

            headers = {
                'Content-Type': 'application/json',
            }
            data = { "contents":[ {"role": "user","parts":[{"text": full_srt}]} ]}

            response = requests.post(url, headers=headers, json=data)
            #print(response.status_code,response.text)
            if response.status_code == 200:
                message = response.json()['candidates'][0]['content']['parts'][0]['text']

                #html = markdown.markdown(message)
                return { 'summary': message }, 200 
            else:
                return { 'summary': response.text }, 500
        else:
            return { 'message':'failed to fetch transcript'}, 401
        '''


        


class Chat(Resource):
    def post(self):
        #query = request.args.get('query')
        chat_history=request.get_json()
        #print(chat_history)
        if chat_history:

            api_key = "Your-API-Key-Here"
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key="+api_key

            headers = {
                'Content-Type': 'application/json',
            }
            #data = { "contents":[ {"role": "user","parts":[{"text": query}]} ]}
            data = { "contents":chat_history['query']}
            print(data)
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:

                message = response.json()['candidates'][0]['content']['parts'][0]['text']

                html = markdown.markdown(message)
            else:
                return { 'message':response.json()['error']['message']}, 500

            return { 'message':html }, 200 
        else:
            return { 'message':'failed to fetch transcript'}, 401


class StudentLogin(Resource):
    def post(self):
        data=request.get_json()
        user=User.query.filter_by(email=data['username']).first()
        if user:
            if user.role == 'student':
                if (user.password == data['password']):
                    #session['username']=user.name
                    #session['user_id']=user.user_id
                    response=({
                        'message': 'User login successful',
                        'user_id': user.user_id,
                        'user_name':user.name,

                    })
                    message=make_response(response)
                    return message
                else:
                    return {'message':'Invalid password'} , 401 #Forbidden
            else:
                return {'message':'Only users can access this page'} , 403 #Unauthorised 
        else:
            return {'message':'Invalid username'} , 401 #Forbidden


class RegisteredCourses(Resource):
    
    def get(self):
        user_id = request.args.get('user_id')

        if user_id == '':
            return {'message':'UserId Required'} , 401
        
        user=User.query.filter_by(user_id=int(user_id)).first()
        if user:
            enrolled_courses=Enrollment.query.filter_by(user_id=user_id).all()
            response={'courses':[],'no_of_courses':0}
            if enrolled_courses:
                for course in enrolled_courses:
                    course_details = Course.query.filter_by(course_id=course.course_id).first()
                    course_name = course_details.name
                    course_description = course_details.description
                    response['courses'].append({
                        'id':course.course_id,
                        'name':course_name,
                        'desc':course_description
                    })
                    response['no_of_courses']=response['no_of_courses']+1
                #print(response)
                return response, 200
            else:
                return {'message':'No registered courses'} , 201
        else:
            return {'message':'Invalid username'} , 401 #Forbidden

class StudentDashboard(Resource):
    def get(self):
        user_id = request.args.get('user_id')

        if user_id == '':
            return {'message':'UserId Required'} , 401
        
        if user_id:
            user = User.query.filter_by(user_id=user_id).all()
            if user:
                enrollments = Enrollment.query.filter_by(user_id=user_id).all()
                courses = []
                for enrollment in enrollments:
                    course = Course.query.get(enrollment.course_id)
                    if course:
                        courses.append({
                            "name": course.name,
                            "desc": course.description
                        })
                no_of_courses = len(courses)
                # print(courses)
                return jsonify({"courses": courses, "no_of_courses": no_of_courses}),200
            else:
                return jsonify({"message": "User not found"}), 401
        else:
            return jsonify({"message": "User ID is required"}), 400

class CourseDetails(Resource):
    def get(self):
        user_id=request.args.get('user_id')
        course_id=request.args.get('course_id')
        if user_id or course_id:
            user = User.query.filter_by(user_id=user_id).all()
            course = Course.query.filter_by(course_id=course_id).first()

            if not course:
                return ({"message": "Course not available"}), 401

            if user:
                enrolled = Enrollment.query.filter_by(user_id=user_id).filter_by(course_id=course_id).first()
                if enrolled:
                    course = Course.query.filter_by(course_id=course_id).first()
                    course_name=course.name
                    # print(f"course_name type: {type(course_name)}, value: {course_name}")
                    course_weeks=Week.query.filter_by(course_id=course_id).all() #returns all the week_ids of the course 
                    # print(course_weeks)
                    details={}
                    for w in course_weeks: #for each week of a course
                        w_id=w.week_id
                        w_links = Link.query.filter_by(week_id=w_id).order_by(Link.link_order).all() #all the links of a week
                        # print(w_links)
                        w_link_details = []
                        for l in w_links:
                            w_link_details.append(l.url)
                        # print(w_link_details)
                        details[w.week_no] = w_link_details
                    # print(details)
                    return ({"details":details,"course_name":course_name}), 200
                    # return ({"course_name":course_name}), 200
                else:
                    return ({"message":"Not enrolled to this course"}), 401
            else:
                return ({"message": "User not found"}), 401
        else:
            return ({"message": "User ID and Course ID is required"}), 400


# Add the resource to the API
api.add_resource(StudentLogin,'/api/studentLogin') 
api.add_resource(RegisteredCourses,'/api/studentDashboard') 
api.add_resource(CourseDetails, '/api/coursePage')
api.add_resource(YTSummary, '/api/YTSummary')
#api.add_resource(Chat, '/api/Chat')
api.add_resource(PDFtoText,'/api/PDFtoText')

@app.route("/")
def hello_world():
    return "<p>Hello, Team 12!</p>"


if __name__ == "__main__":
    app.run(debug=True)
