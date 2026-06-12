<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

const API_URL = '/api/campaigns/'

const campaigns = ref([])
const errorMessage = ref('')
const isLoading = ref(false)

const form = reactive({
  id: null,
  name: '',
  budget: '',
  spend: '',
})

const isEditing = computed(() => form.id !== null)

const statusLabels = {
  ok: 'On track',
  warning: 'At risk',
  overspent: 'Overspent',
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',
  }).format(Number(value))
}

function resetForm() {
  form.id = null
  form.name = ''
  form.budget = ''
  form.spend = ''
}

async function loadCampaigns() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(API_URL)

    if (!response.ok) {
      throw new Error('Could not load campaigns')
    }

    campaigns.value = await response.json()
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

async function saveCampaign() {
  errorMessage.value = ''

  const payload = {
    name: form.name,
    budget: form.budget,
    spend: form.spend,
  }

  const url = isEditing.value ? `${API_URL}${form.id}/` : API_URL
  const method = isEditing.value ? 'PATCH' : 'POST'

  try {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(JSON.stringify(data))
    }

    resetForm()
    await loadCampaigns()
  } catch (error) {
    errorMessage.value = error.message
  }
}

function editCampaign(campaign) {
  form.id = campaign.id
  form.name = campaign.name
  form.budget = campaign.budget
  form.spend = campaign.spend
}

async function deleteCampaign(id) {
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_URL}${id}/`, { method: 'DELETE' })

    if (!response.ok) {
      throw new Error('Could not delete campaign')
    }

    if (form.id === id) {
      resetForm()
    }

    await loadCampaigns()
  } catch (error) {
    errorMessage.value = error.message
  }
}

onMounted(loadCampaigns)
</script>

<template>
  <main class="page">
    <header class="page-header">
      <div>
        <h1>Campaign Budget Tracker</h1>
        <p>Track campaign budgets, spend and overspend risk.</p>
      </div>
    </header>

    <section class="card">
      <h2>{{ isEditing ? 'Edit campaign' : 'Add campaign' }}</h2>

      <form class="campaign-form" @submit.prevent="saveCampaign">
        <label>
          Name
          <input v-model="form.name" required maxlength="200" placeholder="Enter Campaign Name Here." />
        </label>

        <label>
          Budget
          <input v-model="form.budget" required type="number" min="0.01" step="0.01" placeholder="1000.00" />
        </label>

        <label>
          Spend
          <input v-model="form.spend" required type="number" min="0" step="0.01" placeholder="0.00" />
        </label>

        <div class="form-actions">
          <button type="submit">{{ isEditing ? 'Update' : 'Add' }}</button>
          <button v-if="isEditing" type="button" class="secondary" @click="resetForm">Cancel</button>
        </div>
      </form>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </section>

    <section class="card">
      <div class="table-header">
        <h2>Campaigns</h2>
        <span v-if="isLoading">Loading...</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Budget</th>
            <th>Spend</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="campaigns.length === 0 && !isLoading">
            <td colspan="5">No campaigns yet.</td>
          </tr>
          <tr v-for="campaign in campaigns" :key="campaign.id">
            <td>{{ campaign.name }}</td>
            <td>{{ formatCurrency(campaign.budget) }}</td>
            <td>{{ formatCurrency(campaign.spend) }}</td>
            <td>
              <span class="badge" :class="campaign.status">
                {{ statusLabels[campaign.status] ?? campaign.status }}
              </span>
            </td>
            <td class="row-actions">
              <button type="button" class="secondary" @click="editCampaign(campaign)">Edit</button>
              <button type="button" class="danger" @click="deleteCampaign(campaign.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>
