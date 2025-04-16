import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import store from './store'; // Import the store

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(store); // Use the store

app.mount('#app')




