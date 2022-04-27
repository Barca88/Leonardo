<template>
  <v-form ref="configForm" :disabled="loading">
    <!-- Dominio -->
    <v-select
      v-model="selectedDomain"
      :items="domainIds"
      label="Escolha o dominio"
      :disabled="domainValues.length == 0"
      @change="$emit('change', $event)"
      clearable
    />
  </v-form>
</template>

<script>
import * as configApi from '@/utils/api/config'

export default {
  name: 'ConfigForm',
  model: {
    prop: 'domain',
    event: 'change'
  },
  props: { testConfigs: Object },

  data: () => ({
    loading: true,
    selectedDomain: null,
    domainValues: []
  }),
  methods: {
    fetchDomains() {
      this.loading = true
      configApi
        .getAvailableDomains()
        .then((data) => {
          this.domainValues = data
          this.loading = false
        })
        .catch((err) => {
          this.$emit('fetchFail')
          console.log('Error fetching tests', err)
        })
    }
  },
  computed: {
    // Doing computed properties in a weird way so that vetur doesnt break template interpolation :^/
    domainIds() {
      const getdomainIds = (x) => {
        return x.domainValues.map((d) => d._id) || []
      }

      const compDomainIds = getdomainIds(this)

      return compDomainIds
    }
  },
  async created() {
    this.fetchDomains()
    if (this.domain)
      this.selectedDomain = `${this.domain.study_cycle}-${this.domain.scholarity}-${this.domain.description}`
  }
}
</script>
