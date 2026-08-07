<script setup>
import {ref} from "vue";
import { useRouter } from "vue-router";
const router = useRouter();
import AdminNavbar from "../components/AdminNavbar.vue";

const isLoggedIn = ref(false);


  const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
  }


</script>

<template>
      <AdminNavbar></AdminNavbar>
</template>