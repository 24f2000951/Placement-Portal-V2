<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import StudentNavbar from '../components/StudentNavbar.vue';
import ViewDrive from '../components/ViewDrive.vue';

const router = useRouter();
const applications = ref([]);
const selectedDrive = ref(null);
const accessToken = localStorage.getItem("access_token");

const fetchApplications = async () => {
  if (!accessToken) {
    router.push("/login");
    return;
  }

  try {
    const response = await axios.get('/api/student/applications', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    applications.value = response.data;
  } catch (error) {
    console.error('Error fetching applications:', error);
  }
};

const viewDrive = (app) => {
  selectedDrive.value = {
    id: app.drive_id,
    title: app.title,
    company: app.company,
    posted_on: app.application_date,
    description: app.description,
    location: app.location,
    salary: app.salary,
    skills: app.skills,
    allowed_branches: app.allowed_branches,
    cgpa_criteria: app.cgpa_criteria,
    graduation_year: app.graduation_year,
    deadline: app.deadline
  };
};

onMounted(fetchApplications);
</script>

<template>
  <StudentNavbar />
  
  <div class="container my-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3>Your Applications</h3>
    </div>

    <div class="card border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table mb-0 align-middle text-center">
            <thead class="table">
              <tr>
                <th class="text-start ps-4">Job Title</th>
                <th>Company</th>
                <th>Status</th>
                <th>Date Applied</th>
                <th class="pe-4">Actions</th> <!-- FIXED: Added Actions column header -->
              </tr>
            </thead>

            <tbody>
              <tr v-if="applications.length === 0">
                <td colspan="5" class="text-center text-muted py-4">
                  You have not applied to any drives yet.
                </td>
              </tr>

              <tr v-for="app in applications" :key="app.application_id">
                <td class="text-start ps-4 fw-bold">{{ app.title }}</td>
                <td>{{ app.company }}</td>
                <td>
                  <span
                    :class="{
                      'text-secondary': (app.status || '').toLowerCase() === 'pending' || (app.status || '').toLowerCase() === 'applied',
                      'text-success': (app.status || '').toLowerCase() === 'accepted' || (app.status || '').toLowerCase() === 'approved',
                      'text-info': (app.status || '').toLowerCase() === 'shortlisted',
                      'text-danger': (app.status || '').toLowerCase() === 'rejected'
                    }"
                  >
                    {{ app.status ? app.status.charAt(0).toUpperCase() + app.status.slice(1).toLowerCase() : 'Applied' }}
                  </span>
                </td>
                <td>{{ app.application_date || 'N/A' }}</td>
                
                <td class="pe-4">
                  <button 
                    class="btn btn-outline-primary btn-sm" 
                    @click="viewDrive(app)"
                    data-bs-toggle="modal" 
                    data-bs-target="#viewDriveModal"
                  >
                    View Details
                  </button>
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