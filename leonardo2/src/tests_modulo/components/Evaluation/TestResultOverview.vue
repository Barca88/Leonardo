<template>
  <section v-if="test">
    <v-card class="d-flex flex-column" elevation="0">
      <h4 class="pt-6 pb-0 text-h4 text-center" color="primary ">
        Resultado : {{ (test.result * 100).toFixed(0) }}%
      </h4>

      <v-card-text
        class="d-flex flex-column"
        style="overflow-y: auto; overflow-x: hidden"
      >
        <h4 class="text-h4 py-4">Questoes</h4>
        <v-container>
          <v-row justify="center">
            <v-col
              cols="12"
              md="10"
              lg="6"
              v-for="(q, i) in test.questions"
              align-self="stretch"
              :key="i"
            >
              <QuestionResultCard :index="i" :question="q" />
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
    </v-card>
  </section>
</template>

<script>
import QuestionResultCard from '@/tests_modulo/components/UI/QuestionResultCard'

export default {
  name: 'TestResultOverview',
  props: ['test'],
  components: { QuestionResultCard }
}
</script>
