<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';
import ViewDrive from '../components/ViewDrive.vue';

const router = useRouter();
const drives = ref([]);
const total_applicants = ref({});
const accessToken = localStorage.getItem("access_token");
const selectedDrive = ref(null);
const isLoggedIn = ref(false);

const fetchDrives = async () => {
  try {
    const response = await axios.get('/api/company/drives?status=history', {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    drives.value = response.data;
  } catch (error) {
    console.error('Error fetching company drives:', error);
  }
};

const deleteDrive = async (driveId) => {
  if (!confirm("Are you sure you want to delete this drive? This will also remove associated applications.")) {
    return;
  }

  try {
    await axios.delete(`/api/company/drives/${driveId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    fetchDrives();
  } catch (error) {
    console.error('Error deleting drive:', error);
    alert('Failed to delete the drive.');
  }
};

const viewDrive = (drive) => {
  selectedDrive.value = drive;
}

onMounted(() => {
  if (accessToken) {
    isLoggedIn.value = true;
    fetchDrives();
  } else {
    router.push("/login");
  }
});
</script>

<template>
  <CompanyNavbar />
  <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>All Posted Drives (History)</h3>
    </div>

    <table class="table table-borderless align-middle shadow-sm rounded bg-white p-3">
      <thead>
        <tr>
          <th class="ps-4">Job Title</th>
          <th>Status</th>
          <th>Applicants</th>
          <th>Date Posted</th>
          <th>Deadline</th>
          <th class="text-center" style="min-width: 250px;">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drive in drives" :key="drive.id">
          <td class="text-start ps-4 fw-bold">{{ drive.title }}</td>

          <td>
            <span :class="{
              'text-secondary': drive?.status?.toLowerCase() === 'pending',
              'text-danger': drive?.status?.toLowerCase() === 'rejected',
              'text-danger': drive?.status?.toLowerCase() === 'closed'
            }">
              {{ drive?.status ? drive.status.charAt(0).toUpperCase() + drive.status.slice(1).toLowerCase() : 'Pending'
              }}
            </span>
          </td>

          <td>{{ total_applicants[drive.id] || 0 }}</td>
          <td>{{ new Date(drive.posted_on).toLocaleDateString("en-GB") }}</td>
          <td>{{ new Date(drive.deadline).toLocaleDateString("en-GB") }}</td>

  <td class="align-middle">
  <div class="d-flex justify-content-center gap-2">
    <button 
      class="btn btn-outline-primary btn-sm" 
      @click="viewDrive(drive)" 
      data-bs-toggle="modal" 
      data-bs-target="#viewDriveModal"
    >
      View Details
    </button>

    <button 
      class="btn btn-outline-danger btn-sm" 
      @click="deleteDrive(drive.id)"
    >
      Delete
    </button>
  </div>
</td>
        </tr>

        <tr v-if="drives.length === 0">
          <td colspan="5" class="text-center text-muted py-4">No drive history found.</td>
        </tr>
      </tbody>
    </table>
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