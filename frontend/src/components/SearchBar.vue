<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])

const searchQuery = ref('')

const handleSearch = () => {
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
        @keyup.enter="handleSearch"
        @input="handleSearch"
      >
      
      <button class="btn btn-primary px-4" type="submit" @click="handleSearch">
        Search
      </button>
      
    </form>
    
  </div>
</template>