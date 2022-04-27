<template>
  <Dialog
    v-if="test"
    :show="show"
    @changeVisibility="$emit('changeVisibility', $event)"
  >
    <template v-slot:header>
      <slot name="header"> {{ test.id }} - {{ test.config.description }} </slot>
    </template>

    <template v-slot:body>
      <slot name="body">
        <TestConfigDisplay :test="test" />
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
              <QuestionCard :index="i" :question="q" :isReplacement="false" />
            </v-col>
          </v-row>
        </v-container>
      </slot>
    </template>

    <template v-slot:actions>
      <slot name="actions">
        <v-btn text @click="$emit('changeVisibility', false)">Fechar</v-btn>
      </slot>
    </template>
  </Dialog>
</template>

<script>
import Dialog from '@/components/UI/Dialog'
import TestConfigDisplay from '@/components/UI/TestConfigDisplay'
import QuestionCard from '@/components/UI/QuestionCard'

export default {
  name: 'TestDisplayDialog',
  props: ['show', 'test'],
  components: { TestConfigDisplay, QuestionCard, Dialog }
}
</script>
