<template>
  <section>
    <h6 class="text-h6 mb-4 text-center">{{ header[type] }}</h6>
    <div class="d-flex">
      <div>
        <div>
          <div class="d-flex align-center my-5" style="width: 100%">
            <span style="width: 85px">Preparados</span>

            <span
              class="mx-1 py-1 text-center"
              :style="`width: 70px; background-color: ${colors[type].prepared}`"
              >{{ data.prepared }}
            </span>
          </div>
          <div class="d-flex align-center my-5" style="width: 100%">
            <span style="width: 85px"> Realizados</span>

            <span
              class="mx-1 py-1 text-center"
              :style="`width: 70px; background-color: ${colors[type].completed}`"
              >{{ data.completed }}</span
            >
          </div>
          <div class="d-flex align-center my-5" style="width: 100%">
            <span style="width: 85px"> Questoes</span>

            <span
              class="mx-1 py-1 text-center"
              :style="`width: 70px; background-color: ${colors[type].questions}`"
              >{{ data.questions }}
            </span>
          </div>
        </div>
      </div>
      <div>
        <ChartDoughnut
          :chartData="{
            labels: ['Realizados', 'Por Realizar'],
            datasets: [
              {
                backgroundColor: ['#0ab878', '#cfd6d6'],
                hoverBackgroundColor: ['#0ab878', '#cfd6d6'],
                data: [data.completed, data.prepared - data.completed]
              }
            ]
          }"
          class="px-2"
          style="width: 135px; height: 135px"
        />
        <h6 class="text-h6 mb-4 text-center" style="color: #0ab878">
          {{ ((data.completed * 100) / data.prepared).toFixed(0) }}%
        </h6>
      </div>
    </div>
  </section>
</template>

<script>
import ChartDoughnut from '@/components/Dashboards/ChartDoughnut.js'

export default {
  props: { data: Object, type: String },
  components: { ChartDoughnut },
  data: () => ({
    header: {
      total: 'Testes Totais',
      assessment: 'Testes de Avaliação',
      gauging: 'Testes de Aferição'
    },
    colors: {
      total: {
        prepared: '#E2F0D9',
        completed: '#C5E0B4',
        questions: '#A9D18E'
      },
      assessment: {
        prepared: '#FFF2CC',
        completed: '#FFE699',
        questions: '#FFD966'
      },
      gauging: {
        prepared: '#FBE5D6',
        completed: '#F8CBAD',
        questions: '#F4B183'
      }
    },
    chartData: {
      labels: ['Realizados', 'Por Realizar'],
      datasets: [
        {
          backgroundColor: ['#0ab878', '#cfd6d6'],
          hoverBackgroundColor: ['#0ab878', '#cfd6d6'],
          data: [20, 40]
        }
      ]
    }
  })
}
</script>

<style></style>
