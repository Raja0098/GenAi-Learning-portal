<script>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import store from './store'; // Ensure the store is imported

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
  },
  data() {
    return {
      heading: '',
    }
  },
  watch: {
    $route(to) {
      this.heading = to.meta.heading
    }
  },
  created() {
    this.heading = this.$route.meta.heading;

  },
  methods:{
    currentUser() {
      return this.$store.state.current_user;
    },
  },
  
}

</script>

<template>
<body class="d-flex flex-column min-vh-100 text-dark">
  <AppHeader :heading="heading" />
  
    <router-view></router-view>
  
  <AppFooter/>
</body>
</template>

<style>

header {
  background-color: #8d493a;
  color: #f8ede3;
  width: 100%;
  height: fit-content;
  text-align: center;
  /*
  top: 0;
  left: 0;
  position: fixed;
  */
}

footer {
  background-color: #8d493a;
  color: #f8ede3;
  width: 100%;
  height: fit-content;
  text-align: center;
  /*
  bottom: 0;
  left: 0;
  position: fixed;
  */
}

a {
  text-decoration: none;
  color: black;
}

body {
    background-color: rgb(248, 237, 227);
  }

</style>
