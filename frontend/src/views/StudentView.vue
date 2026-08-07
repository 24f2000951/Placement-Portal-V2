<script setup>
import {ref,onMounted} from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import StudentNavbar from "../components/StudentNavbar.vue";
import ViewDrive from "../components/ViewDrive.vue";

const router = useRouter();
const current_user = ref({});
const isLoggedIn = ref(false);
const drives=ref([]);
const selectedDrive=ref(null);
const appliedDrives=ref([]);

const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
  }

const fetchDrives = async () => {
  try {
    const response = await axios.get('/api/student/drives', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    drives.value = response.data;
  } catch (error) {
    console.error('Error fetching drives:', error);
  }
};

const viewDrive=(drive) => {
  selectedDrive.value = drive;
}

const applyDrive = async (driveId) => {
  try {
    await axios.post(`/api/student/drives/${driveId}/apply`, {}, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    if (!appliedDrives.value.includes(driveId)) {
      appliedDrives.value.push(driveId);
    }
  } catch (error) {
    console.error('Error applying for drive:', error);
  }
};


onMounted(() => {
  fetchDrives();
  axios.get('/api/student/profile', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      current_user.value = response.data;
    });
});

</script>

<template>
      <StudentNavbar />
      <div class="container my-4">

  <div class="d-flex justify-content-center mb-4 gap-3">
    <div class="card shadow" style="width: 25rem;">
      <div class="card-body text-center">
        <h1>Profile</h1>
        <h4>Name: {{current_user.name}}</h4>
        <h5 class="text-muted">Email: {{current_user.email}}</h5>
        <h5>Department: {{current_user.student?.dept}}</h5>
        <h5>CGPA: {{current_user.student?.cgpa}}</h5>
        <h5>Phone: {{current_user.student?.phone}}</h5>
        <h5>Passing Year: {{current_user.student?.passing_year}}</h5>
      </div>
    </div>
  </div>
</div>

 <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Ongoing Placement Drives</h2>
    </div>

 <div class="card border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table mb-0 align-middle text-center">
           
            <thead>
              <tr>
                <th scope="col" class="text-start ps-4">Job Title</th>
                <th scope="col">Date Posted</th>
                <th scope="col" class="pe-4">Deadline</th>
                <th scope="col" class="pe-4">Actions</th>
              </tr>
            </thead>
            
            <tbody>
              <tr v-if="drives.length === 0">
                <td colspan="5" class="text-muted py-3">No ongoing drives found.</td>
              </tr>

              <tr v-for="drive in drives" :key="drive.id">
                <td class="text-start ps-4 fw-bold">{{ drive.title }}</td>
               <td>{{ new Date(drive.posted_on).toLocaleDateString("en-GB") }}</td>
               <td>{{ new Date(drive.deadline).toLocaleDateString("en-GB") }}</td>
                <td class="align-middle">
  <div class="d-flex justify-content-center gap-2">
    <button 
      class="btn btn-primary btn-sm" 
      @click="viewDrive(drive)" 
      data-bs-toggle="modal" 
      data-bs-target="#viewDriveModal"
    >
      View Details
    </button>

    <button 
  class="btn btn-success btn-sm" 
  :class="{ 'btn-secondary': appliedDrives.includes(drive.id) }"
  @click="applyDrive(drive.id)"
  :disabled="appliedDrives.includes(drive.id)"
>
  {{ appliedDrives.includes(drive.id) ? 'Applied' : 'Apply' }}
</button>
  </div>
 </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    </div>

    <div class="modal fade" id="viewDriveModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content border-0">

        <div class="modal-header bg-dark text-white">
          <h5 class="modal-title">Drive Details</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body p-0">
          <ViewDrive v-if="selectedDrive" :drive="selectedDrive" />
        </div>

      </div>
    </div>
  </div>
</template>