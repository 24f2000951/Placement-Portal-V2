<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const current_user = ref({});
const drives = ref([]);
const total_applicants = ref(0);
const isLoggedIn = ref(false);


const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
}

onMounted(() => {
  axios.get('/api/company/profile', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      current_user.value = response.data;
    });

  axios.get('/api/company/drives', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      drives.value = response.data;
    });

  axios.get('/api/company/applicants', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      total_applicants.value = response.data;
    });
});



</script>

<template>
  <CompanyNavbar></CompanyNavbar>

<div class="container my-4">

  <div class="d-flex justify-content-center mb-4 gap-3">
    <div class="card shadow" style="width: 25rem;">
      <div class="card-body text-center">
        <h1>Profile</h1>
        <h4>Company: {{current_user.name}}</h4>
        <h5 class="text-muted">Email: {{current_user.email}}</h5>
        <h5>HR Contact No: {{current_user.company?.hrcontact}}</h5>
        <h5>Website: {{current_user.company?.cwebsite}}</h5>
      </div>
    </div>
  </div>
</div>

<div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Ongoing Placement Drives</h2>
      <button class="btn btn-success fw-bold" @click="router.push('/company/create-drive')">Create New Drive</button>
    </div>

    <div class="card border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table mb-0 align-middle text-center">
            
            <thead>
              <tr>
                <th scope="col" class="text-start ps-4">Job Title</th>
                <th scope="col">Status</th>
                <th scope="col">Applicants</th>
                <th scope="col">Deadline</th>
                <th scope="col" class="pe-4">Actions</th>
              </tr>
            </thead>
            
            <tbody>
              <tr>
                <td class="text-start ps-4">
                <div class="fw-bold">Software Engineering Intern</div>
                </td>
                <td><span class="text-success fw-bold">Approved</span></td>
                <td>
                  <span class="fs-5 fw-bold text-primary">150</span>
                </td>
                <td>Oct 15, 2026</td>
                <td class="pe-4">
                  <button class="btn btn-primary btn-sm me-2">View Applicants</button>
                  <button class="btn btn-danger btn-sm">Close Drive</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>