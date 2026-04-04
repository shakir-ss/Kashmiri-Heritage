import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import router from './router'
import App from './App.vue'
import './assets/style.css'
import { useAuthStore } from './stores/authStore'
import { API_URL } from './config'

// Project-wide Axios Base URL configuration
axios.defaults.baseURL = API_URL

const app = createApp(App)
app.use(createPinia())
app.use(router)

// Initialize auth
const auth = useAuthStore()
auth.init()

app.mount('#app')
