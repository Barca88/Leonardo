<template>
  <v-dialog
    max-width="1200"
    :value="show"
    @input="$emit('changeVisibility', $event)"
  >
    <template v-slot:default>
      <v-card class="d-flex flex-column" style="max-height: 90vh">
        <v-toolbar color="#4b779e" class="text-h5 px-4" dark>
          <slot name="header" />
        </v-toolbar>
        <v-card-text
          class="d-flex flex-column"
          style="overflow-y: auto; overflow-x: hidden"
        >
          <slot name="body" />
        </v-card-text>
        <v-card-actions class="justify-end">
          <slot name="actions" />
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
export default {
  name: 'DialogLayout',
  props: ['show']
}
</script>