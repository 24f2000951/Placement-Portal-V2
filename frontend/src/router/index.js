import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AdminView from '../views/AdminView.vue'
import CompanyView from '../views/CompanyView.vue'
import StudentView from '../views/StudentView.vue'
import AdminCompany from '../views/AdminCompany.vue'
import AdminStudent from '../views/AdminStudent.vue'
import CreateDrive from '../views/CompanyCreateDrive.vue'
import AdminDrive from '../views/AdminDrives.vue'
import CompanyDrives from '../views/CompanyDrives.vue'
import StudentEditProfile from '../views/StudentEditProfile.vue'
import CompanyEditProfile from '../views/CompanyEditProfile.vue'
import StudentApplications from '../views/StudentApplications.vue'

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
      path: '/admin/students',
      component: AdminStudent,
    },
    {
      path: '/admin/drives',
      component:AdminDrive,
    },
    {
      path: '/company',
      component: CompanyView,
    },
    {
      path: '/student',
      component: StudentView,
    },
    {
      path: '/student/edit-profile',
      component: StudentEditProfile,
    },
    {
      path: '/student/applications',
      component: StudentApplications,
    },
    {
      path: '/company/edit-profile',
      component: CompanyEditProfile,
    },
    {
      path: '/company/create-drive',
      component: CreateDrive,
    },
    {
      path: '/company/drives',
      component: CompanyDrives,
    }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
