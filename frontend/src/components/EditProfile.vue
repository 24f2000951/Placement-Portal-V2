<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

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

const isUploading = ref(false);
const accessToken = localStorage.getItem("access_token");
const uploadedFileName = ref('');

const handleFileUpload = async (event) => {
  if (props.role !== 'student') return;

  const file = event.target.files[0];
  if (!file) return;

  const uploadData = new FormData();
  uploadData.append('resume', file);

  try {
    isUploading.value = true;
    const response = await axios.post('/api/student/resume', uploadData, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    uploadedFileName.value = file.name;
  } catch (error) {
    console.error('Upload failed:', error);
    alert(error.response?.data?.error || 'Upload failed.');
  } finally {
    isUploading.value = false;
    event.target.value = ''; // Reset the file input so the same file can be uploaded again if needed
  }
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

        <div class="mb-3">
          <label class="form-label fw-bold  small">Upload New Resume (PDF)</label>
          <input 
            type="file" 
            class="form-control" 
            accept=".pdf" 
            @change="handleFileUpload" 
            :disabled="isUploading"
          />
          <small v-if="isUploading" class="text-primary mt-1 d-block">Uploading resume...</small>
          
          <small v-else-if="uploadedFileName" class="text-success mt-1 d-block fw-bold">
            ✓ Uploaded: {{ uploadedFileName }}
          </small>
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