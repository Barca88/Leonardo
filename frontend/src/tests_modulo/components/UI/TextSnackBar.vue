<template>
  <v-snackbar
    top
    text
    :color="color"
    timeout="4000"
    :value="show"
    @input="$emit('close')"
  >
    <section class="d-flex align-center">
      <span class="black--text">
        {{ text }}
      </span>
      <v-spacer />
      <v-btn :color="color" text @click="$emit('close')"> Fechar </v-btn>
    </section>
  </v-snackbar>
</template>

<script>
export default {
  name: 'TextSnackBar',
  props: { color: String, show: Boolean, text: String }
}
</script>

