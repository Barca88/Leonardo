<template>
  <v-card class="pa-2 d-flex flex-column" height="100%">
    <v-card-title>
      <h4>
        {{ index + 1 + '. ' + question._id }}
      </h4>
      <v-spacer />
      <div class="d-flex flex-column">
        <div class="d-flex align-center">
          {{ question.answering_time }}
          <v-icon :color="'orange'" class="px-1" v-text="'mdi-timer-outline'" />
        </div>
      </div>
    </v-card-title>
    <v-card-text>
      {{ question.header }}
    </v-card-text>
    <!-- Solucoes -->
    <v-card-text class="pt-0">
      <ol style="list-style-type: lower-alpha">
        <li
          v-for="(answer, i) in question.body"
          :key="i"
          :class="
            (answer.selected  && answer.correction ==1
                ? 'green--text '
                  : (answer.selected  && answer.correction ==0)
                  ? 'red--text ' 
                : ( answer.correction ==1) 
                ? 'green--text '
                : 'red--text ' 
             ) + 'py-1'
          "
        >
          <v-icon v-if="answer.selected" v-text="'mdi-close-box-outline'" />
          <v-icon v-else v-text="'mdi-checkbox-blank-outline'" />
          {{ answer.answer }}
        </li>
      </ol>
    </v-card-text>
    <v-spacer />
    <v-card-actions>
      <slot name="actions" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'QuestionCard',
  props: ['question', 'index']
}
</script>

<style>
</style>