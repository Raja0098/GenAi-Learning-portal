<template>


  <div class="sidebarmenu">
    <div class="offcanvas offcanvas-start show" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel" style="background-color:#f8ede3;">
      <div class="offcanvas-header" style="background-color: #906056; color:whitesmoke">
        <h5 class="offcanvas-title" id="offcanvasLabel">
          <b>LECTURES</b>
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="sidebar-header" style="background-color: #8d493a; color:whitesmoke; padding-left: 10px; padding-top: 2px;">
            <h1> <b>{{ name }}</b> </h1>
          </div>
          <ul class="sidebar-menu list-group">
            <li v-for="(week, index) in weeks" :key="index" class="menu-item list-group-item btn" data-bs-toggle="collapse" :data-bs-target="'#collapseExample' + index" aria-expanded="false" :aria-controls="'collapseExample' + index" style="background-color: #d0b8a7; color: #8d493a; border: 2px solid whitesmoke; padding-left: 10px;">
              <b>{{ week.week }} </b> <span> ▼ </span>
              <div class="collapse" :id="'collapseExample' + index">
                <ul class="list-group bg-secondary">
                  <li v-for="(url, idx) in week.urls" :key="idx" class="list-unstyled" style="background-color: #d0b8a7;">
                    <a href="#" @click.prevent="handleTopicClick(url)" class="list-group-item" data-bs-dismiss="offcanvas" 
                      style=" border: 2px solid #906056; padding-left: 10px; margin: 3px; font-weight: bold; color:#906056">
                      Topic {{ idx + 1 }}
                    </a>
                  </li>
                </ul>
              </div>
            </li>
          </ul>
      </div>
    </div>
</div>

      



</template>

<script>
export default {
  name: 'SidebarMenu',
  props: {
    name: {
      type: String,
      required: false
    },
    weeks: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      isSidebarOpen: true
    }
  },
  methods: {
    handleTopicClick(url) {
      this.$emit('selectTopic', url)
    },
    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen
    }
  }
}
</script>

<style>
@media (min-width: 768px) {
  .offcanvas {
    width: 25%;
  }
}
</style>
