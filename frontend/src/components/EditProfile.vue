<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  role: {
    type: String,
    required: true
  },
  initialData: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['save']);

// Local reactive form state
const formData = ref({ ...props.initialData });

// Without deep watch, changes to nested properties in initialData won't be reflected in formData. Hence, we use a deep watch.
watch(() => props.initialData, (newData) => {
  formData.value = { ...newData };
}, { deep: true });

const handleSubmit = () => {
  emit('save', formData.value);
};
</script>

<template>
  <div class="card shadow p-4" style="max-width: 35rem; margin: auto;">
    <h3 class="mb-4 text-center">Edit Profile</h3>
    
    <form @submit.prevent="handleSubmit">
      
      <div class="mb-3">
        <label class="form-label fw-bold">Full Name</label>
        <input type="text" class="form-control" v-model="formData.name" required />
      </div>

      <template v-if="role === 'student'">
        <div class="mb-3">
          <label class="form-label fw-bold">Department</label>
          <input type="text" class="form-control" v-model="formData.dept" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">CGPA</label>
          <input type="number" step="0.01" class="form-control" v-model="formData.cgpa" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">Phone Number</label>
          <input type="text" class="form-control" v-model="formData.phone" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">Passing Year</label>
          <input type="number" class="form-control" v-model="formData.passing_year" />
        </div>
      </template>

      <template v-if="role === 'company'">
        <div class="mb-3">
          <label class="form-label fw-bold">Website</label>
          <input type="url" class="form-control" v-model="formData.website" />
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">HR Contact</label>
          <input type="text" class="form-control" v-model="formData.hrcontact" />
        </div>
      </template>

      <div class="d-flex justify-content-end gap-2 mt-4">
        <button type="submit" class="btn btn-primary w-100">Save Changes</button>
      </div>

    </form>
  </div>
</template>