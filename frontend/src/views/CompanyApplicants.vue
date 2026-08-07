<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import CompanyNavbar from '../components/CompanyNavbar.vue'

const router = useRouter()
const route = useRoute()
const driveId = route.params.id
const applicants = ref([])
const accessToken = localStorage.getItem('access_token')
const loadingResumeId = ref(false)
const selectedApplicant = ref(null)
const isSubmitting = ref(false)
const closeModalBtn = ref(null)

const scheduleData = ref({
  interview_date_time: '',
  location: '',
})

const submitSchedule = async () => {
  if (!selectedApplicant.value) return;
  
  const applicantId = selectedApplicant.value.id || selectedApplicant.value.application_id;

  try {
    isSubmitting.value = true;
    
    await axios.post(`/api/company/applicant/${applicantId}/schedule`, scheduleData.value, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });

    alert("Interview scheduled successfully!");
    
    scheduleData.value = { interview_date_time: '', location: '' };
    fetchApplicants();

    if (closeModalBtn.value) {
      closeModalBtn.value.click();
    }

  } catch (error) {
    console.error("Failed to schedule interview:", error);
    alert(error.response?.data?.error || "Failed to schedule interview.");
  } finally {
    isSubmitting.value = false;
  }
};

const rejectApplicant = async (applicantId) => {
  try {
    await axios.post(
      `/api/company/applicant/${applicantId}/reject`,
      {},
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      },
    )
    fetchApplicants()
  } catch (error) {
    console.error('Error rejecting applicant:', error)
    alert('Failed to reject applicant.')
  }
}

const markAsPlaced = async (applicantId) => {
  if (!confirm("Are you sure you want to mark this student as Placed?")) return;

  try {
    await axios.post(
      `/api/company/applicant/${applicantId}/place`,
      {},
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    )
    alert("Student marked as Placed successfully!")
    fetchApplicants()
  } catch (error) {
    console.error('Error updating placement status:', error)
    alert(error.response?.data?.error || 'Failed to update status.')
  }
}

const viewResume = async (studentId) => {
  if (!studentId) return

  try {
    loadingResumeId.value = studentId

    const response = await axios.get(`/api/company/student-resume/${studentId}`, {
      headers: { Authorization: `Bearer ${accessToken}` },
      responseType: 'blob',
    })

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const blobUrl = window.URL.createObjectURL(blob)

    window.open(blobUrl, '_blank')

    setTimeout(() => window.URL.revokeObjectURL(blobUrl), 10000)
  } catch (error) {
    console.error('Failed to load resume:', error)
    alert(error.response?.data?.error || 'This student has not uploaded a resume.')
  } finally {
    loadingResumeId.value = null
  }
}

const fetchApplicants = async () => {
  try {
    const response = await axios.get(`/api/company/drives/${driveId}/applicants`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
    applicants.value = response.data
  } catch (error) {
    console.error('Error fetching applicants:', error)
  }
}

onMounted(() => {
  if (!accessToken) {
    router.push('/login')
    return
  }
  fetchApplicants()
})
</script>

<template>
  <CompanyNavbar />
  <div class="container mt-2">
    <table class="table table-borderless mb-0 align-middle text-center">
      <thead class="table">
        <tr>
          <th scope="col" class="text-start ps-4">S.No</th>
          <th scope="col" class="text-start ps-4">Name</th>
          <th scope="col">Email</th>
          <th scope="col">Phone</th>
          <th scope="col">CGPA</th>
          <th scope="col">Branch</th>
          <th scope="col" class="pe-4">Status</th>
          <th scope="col" class="pe-4">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(applicant, index) in applicants" :key="applicant.id">
          <td class="text-start ps-4">{{ index + 1 }}</td>
          <td class="text-start ps-4">{{ applicant.name }}</td>
          <td>{{ applicant.email }}</td>
          <td>{{ applicant.phone }}</td>
          <td>{{ applicant.cgpa }}</td>
          <td>{{ applicant.dept }}</td>
          <td>
            <span
              :class="{
                'text-secondary': applicant?.status?.toLowerCase() === 'applied',
                'text-danger': applicant?.status?.toLowerCase() === 'rejected',
                'text-info': applicant?.status?.toLowerCase() === 'shortlisted',
                'text-success': applicant?.status?.toLowerCase() === 'placed',
              }"
            >
              {{
                applicant?.status
                  ? applicant.status.charAt(0).toUpperCase() +
                    applicant.status.slice(1).toLowerCase()
                  : 'Pending'
              }}
            </span>
          </td>

          <td class="pe-4 gap-2 d-flex justify-content-center">
            <button
              class="btn btn-primary btn-sm"
              @click="viewResume(applicant.student_id)"
              :disabled="loadingResumeId === applicant.student_id"
            >
              <span
                v-if="loadingResumeId === applicant.student_id"
                class="spinner-border spinner-border-sm me-1"
              ></span>
              View Resume
            </button>

            <template v-if="applicant?.status?.toLowerCase() !== 'placed'">
              
              <button
                v-if="applicant?.status?.toLowerCase() === 'shortlisted'"
                class="btn btn-warning btn-sm text-dark fw-bold"
                @click="markAsPlaced(applicant.application_id)"
              >
                Place
              </button>

              <button 
                v-else
                class="btn btn-success btn-sm" 
                @click="selectedApplicant = applicant"
                data-bs-toggle="modal" 
                data-bs-target="#scheduleModal"
              >
                Schedule Interview
              </button>

              <button
                class="btn btn-danger btn-sm"
                @click="rejectApplicant(applicant.application_id)"
                :disabled="applicant?.status?.toLowerCase() === 'rejected'"
              >
                Reject
              </button>
            </template>
          </td>
        </tr>

        <tr v-if="applicants.length === 0">
          <td colspan="8" class="text-center text-muted py-4">
            No applicants found for this drive.
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="modal fade" id="scheduleModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content border-0 shadow">
        
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title">Schedule Interview</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <div class="modal-body p-4">
          <form @submit.prevent="submitSchedule">
            
            <div class="mb-3">
              <label class="form-label fw-bold">Interview Date & Time</label>
              <input 
                type="datetime-local" 
                class="form-control" 
                v-model="scheduleData.interview_date_time" 
                required 
              />
            </div>

            <div class="mb-3">
              <label class="form-label fw-bold">Location / Meeting Link</label>
              <input
                type="text"
                class="form-control"
                placeholder="Room No. or Google Meet link"
                v-model="scheduleData.location"
                required
              />
            </div>

            <div class="d-flex justify-content-end gap-2 mt-4">
              <button 
                type="button" 
                class="btn btn-secondary" 
                data-bs-dismiss="modal"
                ref="closeModalBtn"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-success" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-1"></span>
                {{ isSubmitting ? 'Scheduling...' : 'Confirm & Schedule' }}
              </button>
            </div>

          </form>
        </div>

      </div>
    </div>
  </div>
</template>