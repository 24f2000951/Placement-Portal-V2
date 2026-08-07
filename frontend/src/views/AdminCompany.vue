<script setup>
import {ref,onMounted,computed} from "vue";
import AdminNavbar from "../components/AdminNavbar.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import SearchBar from "@/components/SearchBar.vue";

const isLoggedIn = ref(false);
const router = useRouter();
const companies = ref([]);
const accessToken = localStorage.getItem("access_token");
const searchQuery=ref("")

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

const approveCompany=async(companyId)=>{
    try{
        await axios.post(`/api/admin/companies/${companyId}/approve`,{},{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        fetchCompanies();
    }
    catch(error){
        console.error("Error approving company:", error);
    }
}

const rejectCompany=async(companyId)=>{
    try{
        await axios.post(`/api/admin/companies/${companyId}/reject`,{},{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        fetchCompanies();
    }
    catch(error){
        console.error("Error rejecting company:", error);
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

const handleSearch = (newQuery) => {
  searchQuery.value = newQuery;
}

const filteredCompanies = computed(() => {
  if (!searchQuery.value) {
    return companies.value; 
  }
  
const lowerCaseSearch = searchQuery.value.toLowerCase();
  
  return companies.value.filter((company) => {
    return company.name.toLowerCase().includes(lowerCaseSearch)
  })
})
</script>

<template>
      <AdminNavbar />
      <SearchBar @search="handleSearch" />

      <div class="container my-2">
      <table class="table table-borderless">
      <thead>
      <tr>
      <th scope="col">S No</th>
      <th scope="col">Company</th>
      <th scope="col">Website</th>
      <th scope="col">HR Contact</th>
      <th scope="col">Status</th>
      <th scope="col">Action</th>
     </tr>
  </thead>
  <tbody>
    <tr v-for="(company, index) in filteredCompanies" :key="company.id">
      <th scope="row">{{ index + 1 }}</th>
      <td>{{ company.name }}</td>
      <td>{{ company.website }}</td>
      <td>{{ company.hrcontact }}</td>
     <td>
    <span v-if="company.status === 'Pending'" class="text-warning">
      {{ company.status }}
    </span>
    <span v-else-if="company.status === 'Approved'" class="text-success">
      {{ company.status }}
    </span>
    <span v-else-if="company.status === 'Blacklisted'" class="text-danger">
      {{ company.status }}
    </span>
  </td>
      <td>
        <button class="btn btn-success btn-sm me-2" @click="approveCompany(company.id)">Approve</button>
        <button class="btn btn-danger btn-sm" @click="rejectCompany(company.id)">Reject</button>
      </td>
    </tr>

    <tr v-if="filteredCompanies.length === 0">
          <td colspan="5" class="text-center text-muted">No companies found.</td>
    </tr>
</tbody>
</table>
</div>
      
</template>