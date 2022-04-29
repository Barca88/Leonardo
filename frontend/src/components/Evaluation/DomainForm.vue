<template>
  <v-form ref="configForm">
    <!-- Dominio -->
    <v-select
      v-model="selectedDomain"
      :items="this.idDomain"
      label="Escolha o dominio"
      @change="$emit('change', $event)"
      clearable
    />
  </v-form>
</template>

<script>
import * as configApi from '@/utils/api/config'
import axios from 'axios';
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
    domainValues: [],
    Domain: [],
    idDomain: []
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
    axios.get(`${process.env.VUE_APP_BACKEND}/question/getQuestions`,{
          headers: {
            'Content-Type': 'multipart/form-data',
            'Access-Control-Allow-Origin': "*"    
          },
        })
      .then((response)=>{
        response.data.domains.forEach((obj) =>{
          console.log('found something')
          this.Domain.push(obj)
          this.idDomain.push(obj._id)
        });
      },(error) =>{
          console.log(error);
    });
  }
}
</script>
