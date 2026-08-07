import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'

const app = createApp(App)

axios.defaults.baseURL = 'http://localhost:5000'

app.use(router)

app.mount('#app')
