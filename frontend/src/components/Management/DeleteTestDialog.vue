<template>
  <Dialog :show="show" @changeVisibility="$emit('changeVisibility', $event)">
    <template v-slot:header>
      Eliminar {{ test.id }} - {{ test.config.description }}
    </template>

    <template v-slot:body>
      <h5 class="pa-10 text-h5 pt-8 pb-4 text-center">
        Tem a certeza que pretende eliminar este teste?
      </h5>
      <v-container>
        <v-row justify="center">
          <v-col cols="6" md="4" lg="3" class="d-flex justify-center">
            <v-btn large @click="$emit('changeVisibility', false)">
              Cancelar
            </v-btn>
          </v-col>
          <v-col cols="6" md="4" lg="3" class="d-flex justify-center">
            <v-btn color="error" large @click="$emit('delete', test._id)">
              Eliminar
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </template>

    <template v-slot:actions>
      <v-btn text @click="$emit('changeVisibility', false)">Fechar</v-btn>
    </template>
  </Dialog>
</template>

<script>
import Dialog from '@/components/UI/Dialog'

export default {
  name: 'DeleteTestDialog',
  props: ['show', 'test'],
  components: { Dialog }
}
</script>
