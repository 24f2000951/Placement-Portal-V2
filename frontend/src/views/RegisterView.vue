<script setup>
import { ref } from "vue";
import axios from "axios";



const form = ref({
  name: "",
  email: "",
  password: "",
  role: "",
  company: ""
});

const methods = {
  async handleRegister() {
    try {
      await axios.post(
        "http://localhost:3000/api/register",
        form.value
      );
      console.log("Registration sucessful",form.value);

    } catch (error) {
      console.error("Registration failed", error);
    }
  }
};


</script>

<template>

  <div class="vh-100 d-flex align-items-center justify-content-center bg-light">

    <div class="container">
      <div class="row justify-content-center">

        <div class="col-md-6 col-lg-5 col-xl-4">

          <div class="card shadow-sm">
            <div class="card-body p-4">
              <h2 class="text-center mb-4">Register</h2>


              <form @submit.prevent="methods.handleRegister" action="#" method="POST">
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
                    <option value="recruiter">Recruiter</option>
                  </select>
                </div>

                <div class="mb-3" v-if="form.role === 'recruiter'">
                  <label for="companyInput" class="form-label">Company Website</label>
                  <input type="text" class="form-control" id="companyInput" v-model="form.company" placeholder="Enter your company website" required>
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