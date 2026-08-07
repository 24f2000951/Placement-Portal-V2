<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<template>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm">
    <div class="container-fluid">
      
      <RouterLink class="navbar-brand fw-bolder text-primary fs-4" to="/admin/dashboard">
        <i class="bi bi-briefcase-fill me-1"></i> HireHub
      </RouterLink>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        
        <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4">
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/admin/dashboard">Dashboard</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/admin/students">Students</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/admin/companies">Companies</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/admin/applications">Applications</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/admin/drives">Drives</RouterLink>
          </li>
        </ul>
    
        <form class="d-flex me-lg-4 my-2 my-lg-0" @submit.prevent>
          <input class="form-control me-2" type="search" placeholder="Search..." aria-label="Search">
          <button class="btn btn-outline-primary" type="submit">Search</button>
        </form>

        <div class="d-flex align-items-center">
          <i class="bi bi-person-circle fs-4 me-3 text-secondary"></i>
          <button class="btn btn-danger btn-sm fw-bold shadow-sm" @click="handleLogout">Logout</button>
        </div>

      </div>
    </div>
  </nav>
</template>
