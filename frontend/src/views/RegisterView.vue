<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
const router = useRouter();

const [successMsg,errorMsg] = [ref(""), ref("")];

const form = ref({
  name: "",
  email: "",
  password: "",
  role: "",
  website: "",
  hrcontact: ""
});

const handleRegister = async () => {

  if (!form.value.name || !form.value.email || !form.value.password || !form.value.role) {
    errorMsg.value = "Please fill out all required fields.";
    return;
  }

  if (form.value.role === 'company' && !form.value.website) {
    errorMsg.value = "Please provide your company website.";
    return;
  }

  try {
    await axios.post("/api/register", form.value);
    
    successMsg.value = "Registration successful! Redirecting to login...";
    
    setTimeout(() => {
      router.push("/login");
    }, 1500);

  } catch (error) {
    console.error("Registration failed", error);
    errorMsg.value=error.response.data.error;
  }
};
</script>

<template>

  <div class="vh-100 d-flex align-items-center justify-content-center bg-light">

    <div class="container">
      <div v-if="errorMsg" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ errorMsg }}
      <button type="button" class="btn-close" @click= "errorMsg = ''" aria-label="Close"></button>
    </div>

    <div v-if="successMsg" class="alert alert-success fade show mb-3" role="alert">
            {{ successMsg }}
      </div>

      <div class="row justify-content-center">
      

        <div class="col-md-6 col-lg-5 col-xl-4">

          <div class="card shadow-sm">
            <div class="card-body p-4">
              <h2 class="text-center mb-4">Register</h2>


              <form @submit.prevent="handleRegister" action="#" method="POST" novalidate>
                <div class="mb-3">
                  <label for="nameInput" class="form-label">Full Name</label>
                  <input type="text" class="form-control" id="nameInput" v-model="form.name" required>
                </div>


                <div class="mb-3">
                  <label for="emailInput" class="form-label">Email address</label>
                  <input type="email" class="form-control" id="emailInput" v-model="form.email" required>
                </div>


                <div class="mb-3">
                  <label for="passwordInput" class="form-label">Password</label>
                  <input type="password" class="form-control" id="passwordInput" v-model="form.password" required>
                </div>

                <div class="mb-3">
                  <label for="roleSelect" class="form-label">I am a</label>
                  <select class="form-select" id="roleSelect" v-model="form.role" required>
                    <option value="" selected disabled>Select role</option>
                    <option value="student">Student</option>
                    <option value="company">Recruiter</option>
                  </select>
                </div>

                <div class="mb-3" v-if="form.role === 'company'">
                  <label for="websiteInput" class="form-label">Company Website</label>
                  <input type="text" class="form-control" id="websiteInput" v-model="form.website" placeholder="Enter NA if not available" required>
                  <label for="hrContactInput" class="form-label">HR Contact</label>
                  <input type="text" class="form-control" id="hrContactInput" v-model="form.hrcontact" placeholder="" required>
                </div>


                <div class="d-grid mt-4 mb-3">
                  <button type="submit" class="btn btn-primary">Create Account</button>
                </div>

              </form>

              <div class="text-center mt-3">
                <span class="text-muted">Already have an account? </span>
                <RouterLink to="/login" class="text-decoration-none">Login here</RouterLink>
              </div>

            </div>
          </div>


          <div class="text-center mt-3">
            <RouterLink to="/" class="text-secondary text-decoration-none small">
              &larr;Back to Home
            </RouterLink>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>