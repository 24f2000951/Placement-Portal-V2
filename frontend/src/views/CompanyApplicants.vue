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
  <div class="container mt-4">
    <table class="table mb-0 align-middle text-center w-100" style="table-layout: fixed;">
      <thead>
        <tr>
          <th scope="col" class="text-start ps-4">Student Name</th>
          <th scope="col">Email</th>
          <th scope="col">Phone</th>
          <th scope="col">CGPA</th>
          <th scope="col">Branch</th>
          <th scope="col" class="pe-4">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="applicant in applicants" :key="applicant.id">
          <td class="text-start ps-4">{{ applicant.name }}</td>
          <td>{{ applicant.email }}</td>
          <td>{{ applicant.phone }}</td>
          <td>{{ applicant.cgpa }}</td>
          <td>{{ applicant.dept }}</td>
          <td class="pe-4">
            <button class="btn btn-outline-primary btn-sm">View Details</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>