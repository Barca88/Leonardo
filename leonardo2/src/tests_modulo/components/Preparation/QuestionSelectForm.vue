<template>
  <v-form>
    <TestConfigDisplay :test="test" />
    <h4 class="text-h4 py-4 text-center">Selecao de Questoes</h4>
    <v-main>
      <v-row justify="center">
        <v-col
          cols="12"
          md="10"
          lg="6"
          v-for="(q, i) in test.questions"
          align-self="stretch"
          :key="i"
        >
          <QuestionCard
            :index="i"
            :question="q"
            :isReplacement="i >= notReplacedQuestions"
          >
            <template v-slot:actions>
              <v-spacer />
              <v-chip class="mx-6 my-2">
                <v-checkbox
                  label="Substituir"
                  @click="updateReplacingQuestions(i)"
                  :value="arrayIncludes(replacingQuestions, i)"
                  color="warning"
                />
              </v-chip>
            </template>
          </QuestionCard>
        </v-col>
      </v-row>
    </v-main>
  </v-form>
</template>

<script>
import TestConfigDisplay from '@/tests_modulo/components/UI/TestConfigDisplay'
import QuestionCard from '@/tests_modulo/components/UI/QuestionCard'

export default {
  name: 'QuestionSelectForm',
  model: {
    prop: 'replacingQuestions',
    event: 'change'
  },
  props: {
    test: Object,
    replacingQuestions: Array,
    replacedQuestions: Array,
    notReplacedQuestions: Number
  },
  components: { TestConfigDisplay, QuestionCard },
  methods: {
    updateReplacingQuestions(i) {
      console.log(`index`, i)
      let newReplacingQuestions
      if (this.replacingQuestions.includes(i))
        newReplacingQuestions = this.replacingQuestions.filter((n) => n != i)
      else newReplacingQuestions = this.replacingQuestions.concat([i])
      this.$emit('change', [...newReplacingQuestions])
    },
    //Vue template is not js :^(
    arrayIncludes(arr, val) {
      return arr.includes(val)
    }
  }
}
</script>
