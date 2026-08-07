<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';

const router = useRouter();
const drives = ref([]);
const total_applicants = ref({});
const accessToken = localStorage.getItem("access_token");

// Fetch all drives posted by this company
const fetchDrives = async () => {
    try {
        const response = await axios.get('/api/company/drives', {
            headers: { Authorization: `Bearer ${accessToken}` },
        });
        drives.value = response.data;
    } catch (error) {
        console.error('Error fetching company drives:', error);
    }
};

// Delete drive function
const deleteDrive = async (driveId) => {
    if (!confirm("Are you sure you want to delete this drive? This will also remove associated applications.")) {
        return;
    }
    
    try {
        await axios.delete(`/api/company/drives/${driveId}`, {
            headers: { Authorization: `Bearer ${accessToken}` },
        });
        // Refresh the list instantly
        fetchDrives();
    } catch (error) {
        console.error('Error deleting drive:', error);
        alert('Failed to delete the drive.');
    }
};

onMounted(() => {
    fetchDrives();
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
          <th>Deadline</th>
          <th class="pe-4 text-end">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="drive in drives" :key="drive.id">
          <td class="text-start ps-4 fw-bold">{{ drive.title }}</td>
          
          <!-- Dynamic Status Badge -->
          <td>
            <span 
              class="badge px-3 py-2" 
              :class="{
                'bg-warning text-dark': drive?.status?.toLowerCase() === 'pending',
                'bg-success': drive?.status?.toLowerCase() === 'approved',
                'bg-danger': drive?.status?.toLowerCase() === 'rejected',
                'bg-secondary': drive?.status?.toLowerCase() === 'closed'
              }"
            >
              {{ drive?.status ? drive.status.charAt(0).toUpperCase() + drive.status.slice(1).toLowerCase() : 'Pending' }}
            </span>
          </td>

          <td>{{ total_applicants[drive.id] || 0 }}</td>
          <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
          
          <!-- Actions: View Applicants (if approved), View Details, and Delete -->
          <td class="pe-4 text-end">
            <!-- View Applicants Button (Only enabled if approved) -->
            <button 
              class="btn btn-outline-primary btn-sm me-2" 
              :disabled="drive?.status?.toLowerCase() !== 'approved'"
              @click="router.push(`/company/drive/${drive.id}`)"
            >
              Applicants
            </button>

            <!-- Delete Drive Button -->
            <button 
              class="btn btn-outline-danger btn-sm" 
              @click="deleteDrive(drive.id)"
            >
              Delete
            </button>
          </td>
        </tr>

        <!-- Empty state -->
        <tr v-if="drives.length === 0">
          <td colspan="5" class="text-center text-muted py-4">No drive history found.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>