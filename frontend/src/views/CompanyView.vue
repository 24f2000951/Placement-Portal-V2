<script setup>
import { ref, onMounted,computed } from 'vue';
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
});

const approvedDrives = computed(() => {
    return drives.value.filter(drive => drive?.status?.toLowerCase() === 'approved');
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
        <h5>Website: {{current_user.company?.website}}</h5>
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
              <tr v-for="drive in approvedDrives" :key="drive.id">
    <td class="text-start ps-4">{{ drive.title }}</td>
    
    <td class="text-success">
        {{ drive?.status ? drive.status.charAt(0).toUpperCase() + drive.status.slice(1).toLowerCase() : 'Approved' }}
    </td>
    
    <td>{{ total_applicants[drive.id] || 0 }}</td>
    <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
    
    <td class="pe-4">
      <button class="btn btn-primary btn-sm me-2" @click="router.push(`/company/drive/${drive.id}`)">View Applicants</button>
      <button class="btn btn-danger btn-sm me-2" @click="router.push(`/company/drive/${drive.id}/close`)">Close Drive</button>
    </td>
</tr>

<tr v-if="approvedDrives.length === 0">
      <td colspan="5" class="text-center text-muted py-4">No approved drives found.</td>
</tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>