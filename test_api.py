import unittest
import requests
class TestLearningPortalAPI(unittest.TestCase):

    BASE_URL = 'http://localhost:5000/api'

    def test_student_login_success(self):
        response = requests.post(f'{self.BASE_URL}/studentLogin', json={
            "username": "2024No1@xxx.com",
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "User login successful",
            "user_id": 3,
            "user_name": "Tux"
        })

    def test_student_login_unauthorized(self):
        response = requests.post(f'{self.BASE_URL}/studentLogin', json={
            "username": "2024No1@xxx.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'Invalid password'})
    
    def test_student_login_Forbidden(self):
        response = requests.post(f'{self.BASE_URL}/studentLogin', json={
            "username": "student",
            "password": "password"
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message':'Invalid username'})

    def test_student_dashboard_success(self):
        response = requests.get(f'{self.BASE_URL}/studentDashboard', params={
            "user_id": "3"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "courses": [
                {
                    "id": 1,
                    "name": "Python",
                    "desc": "Python is a programming course with programming assignments"
                },
                {
                    "id": 2,
                    "name": "Java",
                    "desc": "Java is a programming course with programming assignments"
                }
            ],
            "no_of_courses": 2
        })
        
    def test_student_dashboard_Unauthorized(self):
        response = requests.get(f'{self.BASE_URL}/studentDashboard', params={
            "user_id": "12"
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Invalid username'})

    def test_course_page_success(self):
        response = requests.get(f'{self.BASE_URL}/coursePage', params={
            "user_id": 3,
            "course_id": 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
  "details": {
    "1": [
      "https://youtu.be/8ndsDXohLMQ?si=zzBeQkVNL8_wM0V-",
      "https://youtu.be/As7_aq6XGfI?si=raOPJcE3wTYsh5Ph",
      "https://youtu.be/Yg6xzi2ie5s?si=c5JwCbzq6dkCiNsQ"
    ],
    "2": [
      "https://youtu.be/8n4MBjuDBu4?si=k0dT1tePpduohww5"
    ],
    "3": [
      "https://youtu.be/ruQb8jzkGyQ?si=0nxtD-qx9Fea222X"
    ],
    "4": [
      "https://youtu.be/tDaXdoKfX0k?si=ThdLpjCc-_8TDi2l"
    ]
  },
  "course_name": "Python"
})

    def test_course_page_user_not_found(self):
        response = requests.get(f'{self.BASE_URL}/coursePage', params={
            "user_id": 999,
            "course_id": 1
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            "message": "User not found"
        })

    def test_youtube_summary_success(self):
        response = requests.get(f'{self.BASE_URL}/YTSummary', params={
            "video_url": "https://youtu.be/8ndsDXohLMQ?si=zzBeQkVNL8_wM0V-"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_youtube_summary_bad_request(self):
        response = requests.get(f'{self.BASE_URL}/YTSummary', params={
            "video_url": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Missing video_url'})

    
    def test_PDFtoText_success(self):
        with open('/Users/raj/Downloads/dl_notes/Lecture-2.pdf', 'rb') as file:
            response = requests.post(f'{self.BASE_URL}/PDFtoText', files={'file': file})
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json())
    
    def test_PDFtoText_file_not_uploaded(self):
        response = requests.post(f'{self.BASE_URL}/PDFtoText')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'No file uploaded'})
        

if __name__ == '__main__':
    unittest.main()