<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import StudentNavbar from '../components/StudentNavbar.vue';
import EditProfile from '../components/EditProfile.vue';

const router = useRouter();
const profileData = ref({});
const accessToken = localStorage.getItem("access_token");


if (!accessToken) {
  router.push("/login");
}

const fetchProfile = async () => {
  try {
    const res = await axios.get('/api/student/profile', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    profileData.value = {
      name: res.data.name,
      dept: res.data.student?.dept,
      cgpa: res.data.student?.scgpa,
      phone: res.data.student?.sphone,
      passing_year: res.data.student?.passing_year
    };
  } catch (error) {
    console.error("Error fetching profile:", error);
  }
};

const handleSave = async (updatedValues) => {
  try {
    await axios.put('/api/student/profile', updatedValues, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    alert("Profile updated successfully!");
    router.push('/student');
  } catch (error) {
    console.error("Failed to update profile", error);
    alert("Update failed.");
  }
};

onMounted(fetchProfile);
</script>

<template>
  <StudentNavbar />
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <EditProfile 
          role="student" 
          :initialData="profileData" 
          @save="handleSave" 
        />
      </div>
    </div>
  </div>
</template>