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
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <RouterLink class="navbar-brand fw-bolder text-primary fs-4" to="/company">
        <i class="bi bi-briefcase-fill me-1"></i> HireHub
      </RouterLink>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        
      <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4">
          <li class="nav-item">
            <RouterLink class="nav-link custom-link" active-class="active-blue" to="/company/drives">Drives</RouterLink>
          </li>
      </ul>
     <div class="d-flex align-items-center gap-2">

        <button class="btn btn-outline-primary btn-sm" @click="router.push('/company/edit-profile')">
          <i class="bi bi-person-gear me-1"></i> Edit Profile
        </button>

        <button class="btn btn-danger btn-sm fw-bold shadow-sm" @click="handleLogout">
          Logout
        </button>
      </div>
    </div>
  </div>
</nav>
</template>
