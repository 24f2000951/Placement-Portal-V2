<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const current_user = ref({});
const drives = ref([]);
const isLoggedIn = ref(false);

const accessToken = localStorage.getItem("access_token");
if (accessToken) {
  isLoggedIn.value = true;
} else {
  router.push("/login");
}

const fetchDrives = async () => {
  try {
    const response = await axios.get('/api/company/drives?status=active&status=pending', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    drives.value = response.data;
  } catch (error) {
    console.error('Error fetching drives:', error);
  }
};

const closeDrive = async (driveId) => {
  try {
    await axios.post(`/api/company/drives/${driveId}/close`, {}, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    await fetchDrives();
  } catch (error) {
    console.error('Error closing drive:', error);
    alert('Failed to close the drive.');
  }
};

onMounted(() => {
  axios.get('/api/company/profile', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      current_user.value = response.data;
    });


  fetchDrives();
});

const currentDrives = computed(() => {
    return drives.value.filter(drive => drive?.status?.toLowerCase() === 'approved' || drive?.status?.toLowerCase() === 'pending');
});

const deleteDrive = async (driveId) => {
  if (!confirm("Are you sure you want to delete this drive? This will also remove associated applications.")) {
    return;
  }

  try {
    await axios.delete(`/api/company/drives/${driveId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    
    await fetchDrives();
    
  } catch (error) {
    console.error('Error deleting drive:', error);
    alert('Failed to delete the drive.');
  }
};
</script>

<template>
  <CompanyNavbar />

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
                <th scope="col">Applicants</th>
                <th scope="col">Date Posted</th>
                <th scope="col" class="pe-4">Deadline</th>
                <th scope="col" class="pe-4">Actions</th>
              </tr>
            </thead>
            
            <tbody>
              <tr v-for="drive in currentDrives" :key="drive.id">
    <td class="text-start ps-4">{{ drive.title }}</td>
    
    
    <td>{{ drive.applicant_count || 0 }}</td>
    <td>{{ new Date(drive.posted_on).toLocaleDateString("en-GB") }}</td>
    <td>{{ new Date(drive.deadline).toLocaleDateString("en-GB") }}</td>
    
    <td v-if="drive.status === 'approved'" class="pe-4">
      <button class="btn btn-primary btn-sm me-2" @click="router.push(`/company/drive/${drive.id}/applicants`)">View Applicants</button>
      <button class="btn btn-danger btn-sm me-2" @click="closeDrive(drive.id)">Close Drive</button>
    </td>
    
    <td v-else-if="drive.status === 'pending'" class="pe-4">
       <button class="btn btn-primary btn-sm me-2" @click="router.push(`/company/drive/${drive.id}/edit`)">Edit</button>
       <button class="btn btn-danger btn-sm me-2" @click="deleteDrive(drive.id)">Delete</button>
    </td>
</tr>

<tr v-if="currentDrives.length === 0">
      <td colspan="5" class="text-center text-muted py-4">No active or approved drives found.</td>
</tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

</template>