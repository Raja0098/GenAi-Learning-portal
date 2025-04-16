<template>
  <div class="row m-3">
    <div v-if="no_of_courses == 0" style="text-align: center">
      You haven't registered for any courses!
    </div>
    <h3 class="text-start m-2">
      <b> MY CURRENT COURSES </b>
    </h3>
    <div
      v-for="course in courses"
      :key="course.id"
      class="card text-dark m-3" style="max-width: 22rem; color: #dfd3c3; padding-inline: 15px; padding-block: 15px; "
      @click="redirectCoursePage(course.id)"
    >
      <div class="card-header">
        <b>{{ course.name.toUpperCase() }}</b>
      </div>
      <div class="card-body" >
        <p class="card-text">{{ course.desc }}</p>
      </div>
      
    </div>
    <!-- <h3 class="text-start m-2">AI helper</h3> -->
    <!-- <div class="card text-dark m-3" style="max-width: 18rem;"
      @click="redirectChatbot"
    >
      <div class="card-header">Pdf Summarization</div>
      <div class="card-body">
        <p class="card-text">Get summary of pdf files</p>
      </div>
    </div> -->

    <!-- <div class="card text-dark m-3" style="max-width: 18rem;"
      @click="redirectCoursePage(1)"
    >
      <div class="card-header">Lecture Summary</div>
      <div class="card-body">
        <p class="card-text">Get key concepts and summary of video lectures</p>
      </div>
    </div> -->

    <!-- <div class="card text-dark m-3" style="max-width: 18rem;"
      @click="redirectChatbot"
    >
      <div class="card-header">Chatbot</div>
      <div class="card-body">
        <p class="card-text">Ask any doubt</p>
      </div>
    </div> -->
  </div>
  <div class="">
    <span class="chatbotContainer">
      <img src="../assets/robot.png" class="chatbotIcon" v-on:click="redirectChatbot" />
    </span>
    <p class="chatbotCaption">Your Virtual Assistant</p>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      user_id: this.$route.query.user_id,
      courses: [],
      no_of_courses: null
    }
  },
  created() {
    this.getCourses()
  },
  methods: {
    async getCourses() {
      const response = await fetch(
        `http://127.0.0.1:5000/api/studentDashboard?user_id=${this.user_id}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
      const data = await response.json()
      if (response.ok) {
        this.courses = data['courses']
        this.no_of_courses = data['no_of_courses']
      }
    },
    redirectCoursePage(course_id) {
      //console.log('Redirecting to course ID:', course_id)
      this.$router.push({
        path: '/coursePage',
        query: { course_id: course_id, user_id: this.user_id }
      })
    },
    redirectChatbot() {
      //console.log('Redirecting to Chatbot:')
      this.$router.push({
        path: '/Chatbot',
        
      })
    },

  }
}
</script>

<style scoped>
.card-header {
  background-color: #69352a;
  color:white;
  margin: 10px;
  font-size: larger;
}
.card-body{
  background-color: #8d493a;
  margin: 10px;
  color:whitesmoke
}
.card-text{
  font-weight: bold;
  font-size: large;
}
.course-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(200px, 1fr));
  gap: 16px;
  padding: 16px;
}

.course-card {
  background-color: #dfd3c3;
  border: 1px solid #8d493a;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.course-name {
  background-color: #d0b8a8;
  font-size: 27px;
  color: #973131;
  font-family: 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-weight: bolder;
  padding: 10px;
  text-align: center;
}
.course-desc {
  background-color: #d0b8a8;
  margin: 100px;
  font-size: 20px;
  color: #8d493a;
  font-family: 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-weight: bolder;
  padding: 10px;
  text-align: center;
}
.card-header:hover{
  cursor: pointer;
  background-color: #d0b8a8;
  color: black
}
.card-body:hover {
  background-color: #d0b8a8;
  cursor: pointer;
  color: black
}
.chatbotIcon{
  height: 70px;
  padding: 10px;
}
.chatbotCaption{
  float:right;
  position: absolute; 
  top: 80%;
}
.chatbotContainer{
  height: fit-content;
  width: fit-content;
  border-radius: 11cm;
  background-color: #8d493a;
  float:right;
  position: absolute; 
  top: 80%;
  right: 10%; 
  /* z-index: 1000;  */
}
.chatbotIcon:hover{
  cursor: pointer;
}
.chatbotContainer:hover{
  opacity: 95%;
  border: 2px solid #d0b8a8;
}
.chatbotCaption{
  float:right;
  position: absolute; 
  top: 83.5%;
  left:74%;
  color:#69352a;
  font-weight: bold;
}
</style>
