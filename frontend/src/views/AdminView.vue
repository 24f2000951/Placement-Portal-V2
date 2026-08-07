<script setup>
import {ref} from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const isLoggedIn = ref(false);


  const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
  }


</script>

<template>
        <h1>Admin View</h1>
</template>