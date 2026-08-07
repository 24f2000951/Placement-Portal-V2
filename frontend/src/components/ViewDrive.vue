<script setup>
defineProps({
  drive: {
    type: Object,
    required: true,
    default: () => ({})
  }
});
</script>

<template>
  <div class="card shadow-sm border-0">
    <div class="card-header bg-dark text-white py-3">
      <h4 class="mb-0">{{ drive?.title || 'Job Title Not Available' }}</h4>
    </div>

    <div class="card-body p-4">
      
      <div class="row mb-4 text-center">
        <div class="col-6 border-end">
          <span class="text-muted d-block small text-uppercase fw-bold">CTC / Salary</span>
          <span class="fs-5 fw-bold text-success">{{ drive?.salary || 'N/A' }}</span>
        </div>
        <div class="col-6">
          <span class="text-muted d-block small text-uppercase fw-bold">Deadline</span>
          <span class="fs-5 fw-bold text-danger">{{ drive?.deadline || 'N/A' }}</span>
        </div>
      </div>

      <div class="mb-4">
        <h6 class="text-muted text-uppercase fw-bold">Job Description</h6>
        <p class="bg-light p-3 rounded text-secondary" style="white-space: pre-line;">
          {{ drive?.description || 'No description provided.' }}
        </p>
      </div>

      <ul class="list-group list-group-flush mb-3">
        <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
          <strong>Minimum CGPA</strong>
          <span class="badge bg-secondary">{{ drive?.cgpa_criteria }}</span>
        </li>
        <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
          <strong>Graduation Year</strong>
          <span class="badge bg-secondary">{{ drive?.graduation_year }}</span>
        </li>
        <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
          <strong>Location</strong>
          <span>{{ drive?.location }}</span>
        </li>
        <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
          <strong>Eligible Branches</strong>
          <span>{{ drive?.allowed_branches }}</span>
        </li>
      </ul>

      <div>
        <h6 class="text-muted text-uppercase fw-bold mb-2">Skills Required</h6>
        <p class="mb-0">{{ drive?.skills }}</p>
      </div>

    </div>
  </div>
</template>