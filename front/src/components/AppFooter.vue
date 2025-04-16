<template>
    <!-- <div class="chatbotContainer">
        <img src="../assets/robot.png" class="chatbotIcon" v-on:click="redirectChatbot" />
    </div> -->
    <footer class="sticky-bottom d-flex align-items-center justify-content-center mt-auto">
        <hr>
        <center>Team12 &copy; 2024</center>    
    </footer>
</template>

<script>
export default {
  name: 'Footer',
  props: ['footnote'],
  methods: {
    redirectChatbot() {
      //console.log('Redirecting to Chatbot:')
      this.$router.push({
        path: '/Chatbot',
        
      })
    },

  }
}
</script>

<style>

</style>