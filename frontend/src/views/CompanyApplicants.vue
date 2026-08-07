<script setup>
import { ref, onMounted } from 'vue';
import {useRouter,useRoute} from 'vue-router';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';


const router = useRouter();
const route = useRoute();
const driveId=route.params.id
const applicants = ref([]);
const accessToken = localStorage.getItem("access_token");

const fetchApplicants = async () => {
  try {
    const response = await axios.get(`/api/company/drives/${driveId}/applicants`, {
      headers: { Authorization: `Bearer ${accessToken}` },
    });
    applicants.value = response.data;
  } catch (error) {
    console.error('Error fetching applicants:', error);
  }
};

onMounted(() => {
    if (!accessToken) {
        router.push("/login");
        return;
    }
  fetchApplicants();
});
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
            <tr v-for="(applicant,index) in applicants" :key="applicant.id">
              <td class="text-start ps-4">{{ index + 1 }}</td>
              <td class="text-start ps-4">{{ applicant.name }}</td>
              <td>{{ applicant.email }}</td>
              <td>{{ applicant.phone }}</td>
              <td>{{ applicant.cgpa }}</td>
              <td>{{ applicant.dept }}</td>
             <td>
            <span :class="{
              'text-secondary': applicant?.status?.toLowerCase() === 'applied',
              'text-danger': applicant?.status?.toLowerCase() === 'rejected',
              'text-info': applicant?.status?.toLowerCase() === 'shortlisted',
              'text-success': applicant?.status?.toLowerCase() === 'placed',
            }">
              {{ applicant?.status ? applicant.status.charAt(0).toUpperCase() + applicant.status.slice(1).toLowerCase() : 'Pending'
              }}
            </span>
          </td>
              
                <td class="pe-4 gap-2 d-flex justify-content-center">
                    <button class="btn btn-primary btn-sm" @click="router.push(`/company/drive/${driveId}/applicant/${applicant.id}`)">View Resume</button>
                    <button class="btn btn-success btn-sm" @click="router.push(`/company/drive/${driveId}/applicant/${applicant.id}/schedule`)">Schedule Interview</button>
                    <button class="btn btn-danger btn-sm" @click="router.push(`/company/drive/${driveId}/applicant/${applicant.id}/reject`)">Reject</button>
                </td>
            </tr>
            
            <tr v-if="applicants.length === 0">
              <td colspan="6" class="text-center text-muted py-4">No applicants found for this drive.</td>
            </tr>
          </tbody>
        </table>
      </div>
</template>