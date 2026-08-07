<script setup>
import {ref,onMounted} from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import StudentNavbar from "../components/StudentNavbar.vue";

const router = useRouter();
const current_user = ref({});
const isLoggedIn = ref(false);

const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
  }

onMounted(() => {
  axios.get('/api/student/profile', {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
    .then(response => {
      current_user.value = response.data;
    });
});

</script>

<template>
      <StudentNavbar />
      <div class="container my-4">

  <div class="d-flex justify-content-center mb-4 gap-3">
    <div class="card shadow" style="width: 25rem;">
      <div class="card-body text-center">
        <h1>Profile</h1>
        <h4>Name: {{current_user.name}}</h4>
        <h5 class="text-muted">Email: {{current_user.email}}</h5>
        <h5>Department: {{current_user.student?.dept}}</h5>
        <h5>CGPA: {{current_user.student?.cgpa}}</h5>
        <h5>Phone: {{current_user.student?.phone}}</h5>
        <h5>Passing Year: {{current_user.student?.passing_year}}</h5>
      </div>
    </div>
  </div>
</div>
</template>