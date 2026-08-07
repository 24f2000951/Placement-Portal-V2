import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminView from '../views/AdminView.vue'
import CompanyView from '../views/CompanyView.vue'
import StudentView from '../views/StudentView.vue'
import AdminCompany from '../views/AdminCompany.vue'
import SearchBar from "@/components/SearchBar.vue";

const routes=[
  {
      path: '/',
      component: HomeView,
    },
    {
      path: '/login',
      component:LoginView,
    },
    {
      path: '/register',
      component: RegisterView,
    },
    {
      path: '/admin',
      component: AdminView,
    },
    {
      path: '/admin/companies',
      component: AdminCompany,
    },
    {
      path: '/company',
      component: CompanyView,
    },
    {
      path: '/student',
      component: StudentView,
    }


]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
