<script setup>
import { ref, onMounted } from "vue"; // Import onMounted
import axios from "axios";
import { useRouter, useRoute } from "vue-router"; // Import useRoute

const router = useRouter();
const route = useRoute(); // Allows us to read the URL parameters

// Assuming your route is set up like /company/edit-drive/:id
const driveId = route.params.id; 

const form = ref({
  title: "",
  description: "",
  cgpa: "",
  branches:"",
  skills:"",
  salary:"",
  deadline: "",
  location: "",
  year:"",
  status:"pending"
});

// Fetch the existing drive data when the page loads
onMounted(async () => {
  const accessToken = localStorage.getItem("access_token");
  
  if (!accessToken) {
    router.push("/login");
    return;
  }

  try {
    const response = await axios.get(`/api/company/drives/${driveId}`, {
      headers: { Authorization: `Bearer ${accessToken}` }
    });
    
    const drive = response.data;
    
    form.value.title = drive.title;
    form.value.description = drive.description;
    form.value.cgpa = drive.cgpa_criteria;
    form.value.branches = drive.allowed_branches;
    form.value.skills = drive.skills;
    form.value.salary = drive.salary;
    form.value.location = drive.location;
    form.value.year = drive.graduation_year;
    form.value.deadline = drive.deadline;
    form.value.posted_on = drive.posted_on;
    
  } catch (error) {
    console.error("Error fetching drive details:", error);
    alert("Failed to load drive details.");
  }
});

const editDrive = async () => {
  const accessToken = localStorage.getItem("access_token");

  try {
    const response = await axios.post(
      `/api/company/edit-drive/${driveId}`, 
      form.value,
      {
        headers: { Authorization: `Bearer ${accessToken}` },
      }
    );
    
    console.log("Drive edited successfully:", response.data);
    router.push("/company");
  } catch (error) {
    console.error("Error editing drive:", error);
    alert("Failed to update the drive.");
  }
};
</script>

<template>
  <div class="min-vh-100 py-5 d-flex align-items-center justify-content-center bg-light">
    <div class="container">
      <div class="row justify-content-center">
        
        <div class="col-12 col-md-10 col-lg-8 col-xl-6">
          <div class="card shadow-sm">
            <div class="card-body p-4 p-md-5">
              <h2 class="text-center mb-4">Edit Placement Drive</h2>

              <form @submit.prevent="editDrive" novalidate>
                
                <div class="mb-3">
                  <label for="titleInput" class="form-label">Job Title</label>
                  <input type="text" class="form-control" id="titleInput" v-model="form.title" required>
                </div>

                <div class="mb-3">
                  <label for="descInput" class="form-label">Job Description</label>
                  <textarea class="form-control" id="descInput" v-model="form.description" rows="4" required></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="cgpaInput" class="form-label">Minimum CGPA</label>
                    <input type="number" step="0.1" class="form-control" id="cgpaInput" v-model="form.cgpa" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="yearInput" class="form-label">Graduation Year</label>
                    <input type="number" class="form-control" id="yearInput" v-model="form.year" required>
                  </div>
                </div>

                <div class="mb-3">
                  <label for="branchesInput" class="form-label">Eligible Branches</label>
                  <input type="text" class="form-control" id="branchesInput" v-model="form.branches" placeholder="e.g., CSE, ISE, ECE" required>
                </div>

                <div class="mb-3">
                  <label for="skillsInput" class="form-label">Skills Required</label>
                  <input type="text" class="form-control" id="skillsInput" v-model="form.skills" required>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="salaryInput" class="form-label">Salary (CTC)</label>
                    <input type="text" class="form-control" id="salaryInput" v-model="form.salary" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="deadlineInput" class="form-label">Deadline</label>
                    <input type="date" class="form-control" id="deadlineInput" v-model="form.deadline" required>
                  </div>
                </div>

                <div class="mb-4">
                  <label for="locationInput" class="form-label">Location</label>
                  <input type="text" class="form-control" id="locationInput" v-model="form.location" required>
                </div>

                <div class="d-grid mt-4 mb-3">
                  <button type="submit" class="btn btn-primary btn-lg">Edit Drive</button>
                </div>

              </form>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>