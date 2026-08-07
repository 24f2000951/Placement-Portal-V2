<script setup>
import {ref,onMounted,computed} from "vue";
import AdminNavbar from "../components/AdminNavbar.vue";
import { useRouter } from "vue-router";
import axios from "axios";
import SearchBar from "@/components/SearchBar.vue";

const isLoggedIn = ref(false);
const router = useRouter();
const students = ref([]);
const accessToken = localStorage.getItem("access_token");
const searchQuery=ref("");

const fetchStudents=async()=>{
    try{
        const response=await axios.get("/api/admin/students",{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        students.value=response.data;
    }
    catch(error){
        console.error("Error fetching students:", error);
    }
}

const approveStudent=async(studentId)=>{
    try{
        await axios.post(`/api/admin/students/${studentId}/approve`,{},{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        fetchStudents();
    }
    catch(error){
        console.error("Error approving student:", error);
    }
}

const rejectStudent=async(studentId)=>{
    try{
        await axios.post(`/api/admin/students/${studentId}/reject`,{},{
            headers: {
                Authorization: `Bearer ${accessToken}`
            },
        });
        fetchStudents();
    }
    catch(error){
        console.error("Error rejecting student:", error);
    }
}

onMounted(() => {
  if (accessToken) {
    isLoggedIn.value = true;
    fetchStudents();
  } else {
    router.push("/login");
  }
});


const handleSearch = (newQuery) => {
  searchQuery.value = newQuery;
}

const filteredStudents = computed(() => {
  if (!searchQuery.value) {
    return students.value; 
  }
  
const lowerCaseSearch = searchQuery.value.toLowerCase();
  
  return students.value.filter((student) => {
    return student.name.toLowerCase().includes(lowerCaseSearch)
  })
})


</script>

<template>
      <AdminNavbar />
      <SearchBar @search="handleSearch"/>

      <div class="container my-2">
      <table class="table table-borderless">
      <thead>
      <tr>
      <th scope="col">S No</th>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Phone</th>
      <th scope="col">Branch</th>
      <th scope="col">Status</th>
      <th scope="col">Action</th>
     </tr>
  </thead>
  <tbody>
    <tr v-for="(student, index) in filteredStudents" :key="student.id">
      <th scope="row">{{ index + 1 }}</th>
      <td>{{ student.name }}</td>
      <td>{{ student.email }}</td>
      <td>{{ student.phone }}</td>
      <td>{{ student.branch }}</td>
      <td>
    <span v-if="student.status === 'Approved'" class="text-success">
      {{ student.status }}
    </span>
    <span v-if="student.status === 'Blacklisted'" class="text-danger">
      {{ student.status }}
    </span>
    </td>
      <td>
        <button class="btn btn-success btn-sm me-2" @click="approveStudent(student.id)">Approve</button>
        <button class="btn btn-danger btn-sm" @click="rejectStudent(student.id)">Reject</button>
      </td>
    </tr>

    <tr v-if="filteredStudents.length === 0">
          <td colspan="5" class="text-center text-muted">No students found.</td>
    </tr>
</tbody>
</table>
</div>
</template>