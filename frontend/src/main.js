import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const routes = [
    {path: '/dashboard', component: Dashboard},
    {path: '/login', component: Login}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;

createApp(App).use(router).mount('#app')
