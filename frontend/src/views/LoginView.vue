<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const form = ref({
  email: "",
  password:""
});



const handleLogin = async()=>{
  try{
    const response=await axios.post("http://localhost:5000/api/login",form.value);
    console.log("Login successful",response.data);
    localStorage.setItem("access_token",response.data.access_token);
   
    const userRole=response.data.role;
    if (userRole==="admin")
      router.push("/admin");
    else if (userRole==="student")
      router.push("/student");
    else if (userRole==="company")
      router.push("/company");
  }

  catch(error){
    console.error("Login failed",error);


  }
}

</script>

<template>
  
<div class="vh-100 d-flex align-items-center justify-content-center bg-light">
  
  <div class="container">
    <div class="row justify-content-center">
     
      <div class="col-md-6 col-lg-5 col-xl-4">
        
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <h2 class="text-center mb-4">Login</h2>
            
            
            <form @submit.prevent="handleLogin" action="#" method="POST">
              
              <div class="mb-3">
                <label for="emailInput" class="form-label">Email address</label>
                <input type="email" class="form-control" id="emailInput" v-model="form.email" required>
              </div>
              
              
              <div class="mb-3">
                <label for="passwordInput" class="form-label">Password</label>
                <input type="password" class="form-control" id="passwordInput" v-model="form.password" required>
              </div>
              
              <div class="d-grid mt-4 mb-3">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
              
            </form>

           
            <div class="text-center mt-3">
              <span class="text-muted">Don't have an account? </span>
              <RouterLink to="/register" class="text-decoration-none">Register now</RouterLink>
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