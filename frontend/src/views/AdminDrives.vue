<script setup>
import { ref, onMounted,computed } from 'vue';
import AdminNavbar from '../components/AdminNavbar.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import ViewDrive from '../components/ViewDrive.vue';
import SearchBar from '@/components/SearchBar.vue';

const drives = ref([]);
const router = useRouter()
const isLoggedIn = ref(false);
const accessToken = localStorage.getItem("access_token");
const selectedDrive = ref(null);
const searchQuery = ref("");

const fetchDrives = async () => {
    try {
        const response = await axios.get('/api/admin/drives', {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        drives.value = response.data;
    } catch (error) {
        console.error('Error fetching drives:', error);
    }
};

const viewDrive = (drive) => {
    selectedDrive.value = drive;
}

const approveDrive = async (driveId) => {
    try {
        await axios.post(`/api/admin/drives/${driveId}/approve`, {}, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        fetchDrives();
    } catch (error) {
        console.error('Error approving drive:', error);
    }
};


const rejectDrive = async (driveId) => {
    try {
        await axios.post(`/api/admin/drives/${driveId}/reject`, {}, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        fetchDrives();
    } catch (error) {
        console.error('Error rejecting drive:', error);
    }
};

const handleSearch = (newQuery) => {
  searchQuery.value = newQuery;
}

const filteredDrives = computed(() => {
  if (!searchQuery.value) {
    return drives.value; 
  }
  
const lowerCaseSearch = searchQuery.value.toLowerCase();
  
  return drives.value.filter((drive) => {
    return drive.title.toLowerCase().includes(lowerCaseSearch)
  })
})


onMounted(() => {
    if (accessToken) {
        isLoggedIn.value = true;
        fetchDrives();
    } else {
        router.push("/login");
    }
});

</script>

<template>
    <AdminNavbar></AdminNavbar>
    <SearchBar @search="handleSearch"/>
    <div class="container my-2">
        <table class="table table-borderless">
            <thead>
                <tr>
                    <th scope="col">S No</th>
                    <th scope="col">Job Title</th>
                    <th scope="col">Company</th>
                    <th scope="col">Deadline</th>
                    <th scope="col">Status</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(drive, index) in filteredDrives" :key="drive.id">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ drive.title }}</td>
                    <td>{{ drive.company }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>
    <span 
        :class="{
            'text-dark': drive.status === 'pending' || drive.status === 'Pending',
            'text-success': drive.status === 'approved' || drive.status === 'Approved',
            'text-danger': drive.status === 'rejected' || drive.status === 'Rejected'
        }"
    >
        {{ drive.status.charAt(0).toUpperCase() + drive.status.slice(1) }}
    </span>
</td>
                    <td class="d-flex gap-2">
                        <button class="btn btn-primary btn-sm" @click="viewDrive(drive)" data-bs-toggle="modal"
                            data-bs-target="#viewDriveModal">
                            View
                        </button>
                        <button class="btn btn-success btn-sm" @click="approveDrive(drive.id)">Approve</button>
                        <button class="btn btn-danger btn-sm" @click="rejectDrive(drive.id)">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

<div class="modal fade" id="viewDriveModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <div class="modal-content border-0">
      
      <div class="modal-header bg-dark text-white">
        <h5 class="modal-title">Drive Details</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      
      <div class="modal-body p-0">
        <ViewDrive v-if="selectedDrive" :drive="selectedDrive" />
      </div>

    </div>
  </div>
</div>
</template>