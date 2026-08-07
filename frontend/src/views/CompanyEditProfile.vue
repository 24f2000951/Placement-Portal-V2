<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import CompanyNavbar from '../components/CompanyNavbar.vue';
import EditProfile from '../components/EditProfile.vue';

const router = useRouter();
const profileData = ref({});
const accessToken = localStorage.getItem("access_token");

const fetchProfile = async () => {
  try {
    const res = await axios.get('/api/company/profile', {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    
    // Flatten the data to match the company fields in your shared EditProfile component
    profileData.value = {
      name: res.data.name,
      website: res.data.company?.website,
      hrcontact: res.data.company?.hrcontact
    };
  } catch (error) {
    console.error("Error fetching company profile:", error);
  }
};

const handleSave = async (updatedValues) => {
  try {
    await axios.put('/api/company/profile', updatedValues, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    alert("Company profile updated successfully!");
    router.push('/company');
  } catch (error) {
    console.error("Failed to update profile", error);
    alert("Update failed.");
  }
};

onMounted(fetchProfile);
</script>

<template>
  <CompanyNavbar />
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <EditProfile 
          role="company" 
          :initialData="profileData" 
          @save="handleSave" 
        />
      </div>
    </div>
  </div>
</template>