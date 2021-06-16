<template>
  <v-card
    :class="{
      'yellow lighten-4': isReplacement,
      'pa-2 d-flex flex-column': true
    }"
    height="100%"
  >
    <v-card-title>
      <h4>
        {{ index + 1 + '. ' + question.id }}
      </h4>
      <v-spacer />
      <div class="d-flex flex-column">
        <div class="d-flex align-center">
          {{ question.answering_time }}
          <v-icon :color="'orange'" class="px-1" v-text="'mdi-timer-outline'" />
        </div>
      </div>
    </v-card-title>
    <v-card-subtitle
      class="d-flex align-center justify-space-between align-center"
    >
      <p class="mb-0 d-flex align-center">
        <v-icon class="pe-1" v-text="'mdi-account'" />
        <span class="pe-4"> {{ question.inserted_by }} </span>
        <v-icon class="pe-1" v-text="'mdi-calendar'" />
        {{ question.inserted_at }}
      </p>

      <v-rating :value="parseInt(question.difficulty_level)">
        <template v-slot:item="props">
          <v-icon
            :color="props.isFilled ? 'orange' : 'grey lighten-1'"
            class="px-0"
            size="25px"
            v-text="'mdi-head-cog'"
          />
        </template>
      </v-rating>
    </v-card-subtitle>
    <v-card-text>
      {{ question.header }}
    </v-card-text>
    <!-- Solucoes -->
    <v-card-text class="pt-0">
      <ol style="list-style-type: lower-alpha">
        <li
          v-for="(answer, i) in question.body"
          :key="i"
          :class="(answer.correction ? 'green--text ' : 'red--text ') + 'py-1'"
        >
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
  props: ['question', 'isReplacement', 'index']
}
</script>

<style>
</style>