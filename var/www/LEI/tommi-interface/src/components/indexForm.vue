<template>
  <div id="consultar">  
      <v-card height="100%" width="100%">
        <v-toolbar color="#2A3F54" dark>
          <h1>{{$t('navd.indexes')}}</h1>
        </v-toolbar>
        <v-card-title>
          <h2>{{$t('indForm.visInd')}}</h2>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left"><b>{{$t('indForm.id')}}</b></td>
                                <td>
                                    <v-layout>
                                        {{index.id}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('indForm.oco')}}</b></td>
                                <td>
                                    <v-layout>
                                        <v-list disabled flat>
                                          <v-list-item-group v-model="index.ocorrencias" color="indigo">
                                              <v-list-item
                                              v-for="(ocorrencia, i) in index.ocorrencias"
                                              :key="i"
                                              >

                                                <v-list-item-content>
                                                    <v-list-item-title v-text="Object.keys(ocorrencia) + ': ' + Object.values(ocorrencia)"></v-list-item-title>
                                                </v-list-item-content>
                                              </v-list-item>
                                          </v-list-item-group>
                                        </v-list>
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('indForm.files')}}</b></td>
                                <td>
                                    <v-layout>
                                        <v-list disabled flat>
                                          <v-list-item-group v-model="index.ref" color="indigo">
                                            <v-list-item
                                            v-for="(ref, i) in index.ref"
                                            :key="i"
                                            >
                                            
                                              <v-list-item-content>
                                                  <v-list-item-title v-text="ref"></v-list-item-title>
                                              </v-list-item-content>
                                            </v-list-item>
                                          </v-list-item-group>
                                        </v-list>
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left"><b>{{$t('indForm.noco')}}</b></td>
                                <td>
                                    <v-layout>
                                        {{index.n_oco}}
                                    </v-layout>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                  </v-simple-table>
              </v-container>
          </v-form>
          </v-card-actions>
          <v-toolbar flat>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on: tooltip }">
                  <v-btn @click="emiteFecho" v-on="{ ...tooltip}"><v-icon>mdi-exit-to-app</v-icon></v-btn>
              </template>
              <span>
                  {{$t('indForm.close')}}
              </span>
            </v-tooltip>
          </v-toolbar>
      </v-card>
  </div>
</template>


<script>

export default {
  data(){
    return{
      index:{
        id:"",
        ocorrencias:[],
        ref:[],
        n_oco:"",
      }
    }
  },
  props:{
    passedData:{
      type:Object
    }
  },
  watch:{
    passedData: {
        immediate: true,
        deep: true,
        handler(){
            this.onUpdate()
        }
    }
  },methods:{
    onUpdate(){
      this.index.id = this.passedData._id
      this.index.ocorrencias = this.passedData.ocorrencias
      this.index.ref = this.passedData.ref
      this.index.n_oco = this.passedData.n_ocorrencias
    },
    emiteFecho(){
      this.$emit('emiteFecho')
    }
  },
  created(){
    this.onUpdate()
  }
}
</script>
<style scoped>
  #consultar *{
            box-sizing: border-box;
  }
  #consultar{
            margin: 20px auto;
            max-width: 800px;
  }
</style>
