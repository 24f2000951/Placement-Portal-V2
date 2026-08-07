<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import AdminNavbar from "../components/AdminNavbar.vue";
import axios from "axios";

import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const router = useRouter();
const isLoggedIn = ref(false);

const barChartRef = ref(null);
const donutChartRef = ref(null);

const accessToken = localStorage.getItem("access_token");
if (accessToken) {
  isLoggedIn.value = true;
} else {
  router.push("/login");
}


onMounted(async () => {
  try {
    const response = await axios.get('/api/admin/', {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    });
    
    const data = response.data;
    
    document.getElementById('stat-students').innerText = data.totals.students;
    document.getElementById('stat-placed').innerText = data.totals.placed_students;
    document.getElementById('stat-rate').innerText = data.totals.placement_rate + '%';
    document.getElementById('stat-companies').innerText = data.totals.companies;
    document.getElementById('stat-applications').innerText = data.totals.applications;
    document.getElementById('stat-drives').innerText = data.totals.drives;

    new Chart(barChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Students', 'Companies', 'Applications', 'Drives'],
        datasets: [{
          label: 'Count',
          data: [
            data.totals.students, 
            data.totals.companies, 
            data.totals.applications, 
            data.totals.drives
          ],
          backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0']
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        }
      }
    });

    new Chart(donutChartRef.value, {
      type: 'doughnut',
      data: {
        labels: [ 'Placed', 'Unplaced'],
        datasets: [{
          data: [
            data.applications_breakdown.accepted, 
            data.applications_breakdown.unplaced
          ],
          backgroundColor: ['#36A2EB', '#EE4B2B']
        }]
      },
      options: {
        responsive: true
      }
    });

  } catch (error) {
    console.error("Error loading admin dashboard stats:", error.response?.data || error.message);
  }
});
</script>

<template>
  <div class="admin-dashboard">
    <AdminNavbar />
    
    <div class="container mt-4">
      <h2 class="mb-4">Admin Dashboard</h2>
      
      <!-- Stat Cards Row -->
      <div class="row text-center my-4">
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Students</h6>
            <h3 id="stat-students">-</h3>
          </div>
        </div>
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Placed</h6>
            <h3 id="stat-placed">-</h3>
          </div>
        </div>
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Placement Rate</h6>
            <h3 id="stat-rate">-</h3>
          </div>
        </div>
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Companies</h6>
            <h3 id="stat-companies">-</h3>
          </div>
        </div>
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Applications</h6>
            <h3 id="stat-applications">-</h3>
          </div>
        </div>
        <div class="col-md-2 mb-3">
          <div class="card p-3 shadow-sm">
            <h6 class="text-muted">Drives</h6>
            <h3 id="stat-drives">-</h3>
          </div>
        </div>
      </div>

      <!-- Charts Row with Vue Template Refs -->
      <div class="row mt-5">
        <div class="col-md-6 mb-4">
          <div class="card p-3 shadow-sm">
            <h5 class="text-center mb-3">Platform Metrics</h5>
            <canvas ref="barChartRef"></canvas>
          </div>
        </div>
        <div class="col-md-6 mb-4">
          <div class="card p-3 shadow-sm">
            <h5 class="text-center mb-3">Application Status Breakdown</h5>
            <canvas ref="donutChartRef"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}
.card {
  border: none;
  border-radius: 8px;
}
</style>