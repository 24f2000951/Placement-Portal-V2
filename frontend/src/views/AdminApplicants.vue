<script setup>
import { ref, onMounted,computed } from 'vue';
import {useRouter,useRoute} from 'vue-router';
import axios from 'axios';
import AdminNavbar from '@/components/AdminNavbar.vue';
import SearchBar from '@/components/SearchBar.vue';


const router = useRouter();
const route = useRoute();
const driveId=route.params.id
const searchQuery = ref('');
const applicants = ref([]);
const accessToken = localStorage.getItem("access_token");

const fetchApplicants = async () => {
    try {
        const response = await axios.get(`/api/admin/applicants`, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        console.log(response.data);
        applicants.value = response.data;
    } catch (error) {
        console.error("Error fetching applicants:", error);
    }
};

const handleSearch = (newQuery) => {
  searchQuery.value = newQuery;
}

const filteredApplicants = computed(() => {
  if (!searchQuery.value) {
    return applicants.value;
  }
  return applicants.value.filter(applicant =>
    applicant.student_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

onMounted(() => {
    if (!accessToken) {
        router.push("/login");
        return;
    }
    fetchApplicants();
  
});
</script>

<template>
  <AdminNavbar />
  <SearchBar @search="handleSearch" />
  <div class="container my-2">
        <table class="table table-borderless mb-0 align-middle text-center">
          <thead class="table">
            <tr>
              <th scope="col" class="text-start ps-4">ID</th>
              <th scope="col" class="text-start ps-4">Name</th>
              <th scope="col">Job Title</th>
              <th scope="col">Company</th>
              <th scope="col">Date Applied</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          
          <tbody>
            <tr v-for="(applicant) in filteredApplicants" :key="applicant.id">
              <td class="text-start ps-4">{{ applicant.id }}</td>
              <td class="text-start ps-4">{{ applicant.student_name }}</td>
              <td>{{ applicant.job_title }}</td>
              <td>{{ applicant.company_name }}</td>
              <td>{{ applicant.applied_on }}</td>
            <td>
            <span :class="{
              'text-secondary': applicant?.status?.toLowerCase() === 'applied',
              'text-danger': applicant?.status?.toLowerCase() === 'rejected',
              'text-info': applicant?.status?.toLowerCase() === 'scheduled',
              'text-success': applicant?.status?.toLowerCase() === 'placed',
            }">
              {{ applicant?.status ? applicant.status.charAt(0).toUpperCase() + applicant.status.slice(1).toLowerCase() : 'Pending'
              }}
            </span>
          </td>
            </tr>
            
            <tr v-if="filteredApplicants.length === 0">
              <td colspan="6" class="text-center text-muted py-4">No applicants found for this drive.</td>
            </tr>
          </tbody>
        </table>
    </div>

</template>