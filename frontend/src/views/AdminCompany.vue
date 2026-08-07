<script setup>
import {ref,onMounted} from "vue";
import AdminNavbar from "../components/AdminNavbar.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import SearchBar from "@/components/SearchBar.vue";

const isLoggedIn = ref(false);
const router = useRouter();
const companies = ref([]);
const accessToken = localStorage.getItem("access_token");
const searchQuery=ref("");

const fetchCompanies=async()=>{
    try{
        const response=await axios.get("/api/admin/companies",{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        companies.value=response.data;
    }
    catch(error){
        console.error("Error fetching companies:", error);
    }
}

onMounted(() => {
  if (accessToken) {
    isLoggedIn.value = true;
    fetchCompanies();
  } else {
    router.push("/login");
  }
});


</script>

<template>
      <AdminNavbar />
      <SearchBar />

      <div class="container my-2">
      <table class="table table-borderless">
      <thead>
      <tr>
      <th scope="col">S No</th>
      <th scope="col">Company</th>
      <th scope="col">Website</th>
      <th scope="col">Status</th>
      <th scope="col">Action</th>
     </tr>
  </thead>
  <tbody>
    <tr v-for="(company, index) in companies" :key="company.id">
      <th scope="row">{{ index + 1 }}</th>
      <td>{{ company.name }}</td>
      <td>{{ company.website }}</td>
      <td>
        <button class="btn btn-success btn-sm me-2" @click="approveCompany(company.id)">Approve</button>
        <button class="btn btn-danger btn-sm" @click="rejectCompany(company.id)">Reject</button>
      </td>
    </tr>

    <tr v-if="companies.length === 0">
          <td colspan="5" class="text-center text-muted">No companies found.</td>
    </tr>
</tbody>
</table>
</div>
      
</template>