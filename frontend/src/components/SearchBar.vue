<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])

const searchQuery = ref('')

const handleSearch = () => {
  // Emits the current typed word to the parent component
  emit('search', searchQuery.value)
}
</script>

<template>
  <div class="d-flex justify-content-center my-4">
    
    <form class="d-flex w-50 gap-2" @submit.prevent="handleSearch">
      
      <input 
        class="form-control"
        type="search"
        placeholder="Search"
        v-model="searchQuery" 
      >
      
      <button class="btn btn-primary px-4" type="submit">
        Search
      </button>
      
    </form>
    
  </div>
</template>