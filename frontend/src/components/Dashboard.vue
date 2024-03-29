<script setup>
import { onMounted, watch, ref } from 'vue';
import axios from 'axios';
import Chart from 'chart.js/auto';
import router from '@/main';

const COBRANCA_ULR = 'http://127.0.0.1:8000/api/cobranca/'
const PLANILHA_ULR = 'http://127.0.0.1:8000/api/planilha/'
const STATS_ULR = 'http://127.0.0.1:8000/api/stats/'
const monthInput = ref('')
const planihaInput = ref('')
const ativos = ref('')
const cancelados = ref('')
const stats = ref('')
const selectedFile = ref(null);

var cobrancas = ref([])
var planilhas = ref([])
var chartData
var canva1
var chart1
var query_params = {
  data_inicio: '2022-10-12',
  id: 13
}

watch(planihaInput, async (newValue, oldValue) => {
  query_params.id = newValue
  chart1.destroy()
  await fetchCobrancas(query_params)
  await fetchStats()
  createChart(chartData)
})

watch(monthInput, async (newValue, oldValue) => {
  query_params.data_inicio = newValue + '-01'
  chart1.destroy()
  await fetchCobrancas(query_params)
  await fetchStats()
  createChart(chartData)
})

async function fetchStats() {
  await axios.get(STATS_ULR, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('access')
    },
    params: query_params
  })
    .then(function (response) {
      stats.value = response.data
    })
    .catch(function (error) {
      console.log(error);
    });
}

async function fetchPlanilhas() {
  await axios.get(PLANILHA_ULR, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('access')
    },
  })
    .then(function (response) {
      planilhas.value = response.data
    })
    .catch(function (error) {
      console.log(error);
    });
}

async function fetchCobrancas(query_params) {
  await axios.get(COBRANCA_ULR, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('access')
    },
    params: query_params
  })
    .then(function (response) {
      var data = {
        labels: ['Ativos', 'Cancelados'],
        datasets: [{
          label: 'Teste',
          data: [0, 0],
          borderWidth: 1
        }],
      }
      cobrancas.value = response.data
      cobrancas.value.forEach(element => {
        if (element.status == "Ativa")
          data.datasets[0].data[0]++
        else
          data.datasets[0].data[1]++
      });
      chartData = data
    })
    .catch(function (error) {
      console.log(error);
    });
}

async function handleFileChange(event) {
  const formData = new FormData();
  formData.append('file', selectedFile.value);
  selectedFile.value = event.target.files[0];
  await axios.post(PLANILHA_ULR, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': 'Bearer ' + localStorage.getItem('access')
    },
  })
    .then(function (response) {
      router.push('/dashboard')
    })
    .catch(function (error) {
      console.log(error);
    });
}

function createChart(data) {
  chart1 = new Chart(canva1, {
    type: 'bar',
    data: data,
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

await fetchStats()
await fetchPlanilhas()
await fetchCobrancas(query_params)

onMounted(() => {
  const now = new Date();
  const year = now.getFullYear();
  const month = (now.getMonth() + 1).toString().padStart(2, '0');
  monthInput.value = `${year}-${month}`;
  canva1 = document.getElementById("myChart").getContext('2d');
  createChart(chartData)
})
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand mx-auto ms-lg-0 ms-3 text-uppercase fw-bold" href="#">CopyBase</a>
      <div class="mx-auto">
        <div class="input-group">
          <select class="form-select" v-model="planihaInput">
            <option disabled value="">Please select one</option>
            <option v-for="planilha in planilhas" :value="planilha.id" :key="planilha.id">{{ planilha.id }} - {{
            planilha.nome_planilha }}</option>
          </select>
          <input id="fileInput" type="file" @change="handleFileChange">
        </div>
      </div>
      <div class="mx-auto">
        <input id="monthInput" type="month" v-model="monthInput">
      </div>
    </div>
  </nav>
  <!-- top navigation bar -->
  <main class="mt-5 pt-3">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-12">
          <h4>Dashboard</h4>
        </div>
      </div>
      <div class="row">
        <div class="col-md-3 mb-3">
          <div class="card bg-success text-white h-100">
            <div class="card-body py-5">{{ stats.clientes_ativos }}</div>
            <div class="card-footer d-flex">
              Ativos total
              <span class="ms-auto">
                <i class="bi bi-chevron-right"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card bg-danger text-white h-100">
            <div class="card-body py-5">{{ stats.clientes_cancelados }}</div>
            <div class="card-footer d-flex">
              Cancelados mês
              <span class="ms-auto">
                <i class="bi bi-chevron-right"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card bg-primary text-white h-100">
            <div class="card-body py-5">{{ stats.churm_rate }}%</div>
            <div class="card-footer d-flex">
              Churm Rate
              <span class="ms-auto">
                <i class="bi bi-chevron-right"></i>
              </span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card bg-info text-white h-100">
            <div class="card-body py-5">R$ {{ stats.mrr }}</div>
            <div class="card-footer d-flex">
              MRR
              <span class="ms-auto">
                <i class="bi bi-chevron-right"></i>
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col mb-3">
          <div class="card h-100">
            <div class="card-header">
              <div class="row">
                <div class="col">
                  <span class="me-2"><i class="bi bi-bar-chart-fill"></i></span>
                  Ativos/Cancelados
                </div>
              </div>
            </div>
            <div class="card-body">
              <canvas id="myChart" class="chart" width="400" height="200"></canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12 mb-3">
          <div class="card">
            <div class="card-header">
              <span><i class="bi bi-table me-2"></i></span> Data Table
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table id="example" class="table table-striped data-table" style="width: 100%">
                  <thead>
                    <tr>
                      <th>Assinante</th>
                      <th>Status</th>
                      <th>Data Inicio</th>
                      <th>Cobranças/Frequencia</th>
                      <th>Data Cancelamento</th>
                      <th>Valor</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="cobranca in cobrancas" :key="cobranca.id">
                      <td>{{ cobranca.id_assinante }}</td>
                      <td>{{ cobranca.status }}</td>
                      <td>{{ cobranca.data_inicio }}</td>
                      <td>{{ cobranca.quantidade_cobrancas }}/{{ cobranca.frequencia_dias }}</td>
                      <td>{{ cobranca.data_cancelamento }}</td>
                      <td>{{ cobranca.valor }}</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr>
                      <th>Assinante</th>
                      <th>Status</th>
                      <th>Data Inicio</th>
                      <th>Cobranças/Frequencia</th>
                      <th>Data Cancelamento</th>
                      <th>Valor</th>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap");

body,
button {
  font-family: "Inter", sans-serif;
}

:root {
  --offcanvas-width: 270px;
  --topNavbarHeight: 56px;
}

.sidebar-nav {
  width: var(--offcanvas-width);
}

.sidebar-link {
  display: flex;
  align-items: center;
}

.sidebar-link .right-icon {
  display: inline-flex;
}

.sidebar-link[aria-expanded="true"] .right-icon {
  transform: rotate(180deg);
}

@media (min-width: 992px) {
  body {
    overflow: auto !important;
  }

  main {
    margin-left: var(--offcanvas-width);
  }

  /* this is to remove the backdrop */
  .offcanvas-backdrop::before {
    display: none;
  }

  .sidebar-nav {
    -webkit-transform: none;
    transform: none;
    visibility: visible !important;
    height: calc(100% - var(--topNavbarHeight));
    top: var(--topNavbarHeight);
  }
}
</style>