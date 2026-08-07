<script setup>
</script>

<template>

  <div class="vh-100 d-flex align-items-center justify-content-center bg-light">
    
    <div class="container text-center">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          
          <div class="mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-mortarboard text-primary" viewBox="0 0 16 16">
              <path d="M8.211 2.047a.5.5 0 0 0-.422 0l-7.5 3.5a.5.5 0 0 0 .025.917l7.5 3a.5.5 0 0 0 .372 0L14 7.14V13a1 1 0 0 0-1 1v2h3v-2a1 1 0 0 0-1-1V6.739l.686-.275a.5.5 0 0 0 .025-.917l-7.5-3.5ZM8 8.46 1.758 5.965 8 3.052l6.242 2.913L8 8.46Z"/>
              <path d="M4.176 9.032a.5.5 0 0 0-.656.327l-.5 1.7a.5.5 0 0 0 .294.605l4.5 1.8a.5.5 0 0 0 .372 0l4.5-1.8a.5.5 0 0 0 .294-.605l-.5-1.7a.5.5 0 0 0-.656-.327L8 10.466 4.176 9.032Zm-.068 1.873.22-.748 3.496 1.311a.5.5 0 0 0 .352 0l3.496-1.311.22.748L8 12.46l-3.892-1.555Z"/>
            </svg>
          </div>

          <h1 class="display-4 fw-bold text-dark mb-3">
            Welcome to the HireHub
          </h1>
          
          <p class="lead text-muted mb-5">
            Bridging the gap between top engineering talent and industry leaders. 
            Streamline your recruitment process, manage applications, and jumpstart your career all in one place.
          </p>
          
          <div class="d-grid gap-3 d-sm-flex justify-content-sm-center">
            <RouterLink to="/login" class="btn btn-primary btn-lg px-5 shadow-sm">
              Login
            </RouterLink>
            <RouterLink to="/register" class="btn btn-outline-secondary btn-lg px-5">
              Register
            </RouterLink>
          </div>

        </div>
      </div>
    </div>
    
  </div>
</template>
