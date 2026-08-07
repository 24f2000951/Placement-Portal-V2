<script setup>
import {ref,onMounted} from "vue";
import { useRouter } from "vue-router";
const router = useRouter();

const isLoggedIn = ref(false);

onMounted(() => {
  const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    isLoggedIn.value = true;
  } else {
    router.push("/login");
  }
});

</script>

<template>
        <h1>Student View</h1>
</template>