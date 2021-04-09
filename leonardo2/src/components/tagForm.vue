<template>
  <div id="consultar">
      <v-card height="100%" width="100%">
        <v-card-title>
          <h1>{{$t('tForm.vT')}}</h1>
        </v-card-title>
        <v-card-actions>
          <v-form ref="form" method="post" enctype="multipart/form-data">
              <v-container>
                  <v-simple-table class="table">
                    <template v-slot:default>
                        <tbody>
                            <tr>
                                <td class="text-left">{{$t('indForm.id')}}</td>
                                <td>
                                    <v-layout justify-center>
                                        {{tag.id}}
                                    </v-layout>
                                </td>
                            </tr>
                            <tr>
                                <td class="text-left">{{$t('indForm.files')}}</td>
                                <td>
                                    <v-layout justify-center>
                                        <v-list disabled flat>
                                          <v-list-item-group v-model="tag.ref" color="indigo">
                                              <v-list-item
                                              v-for="(ref, i) in tag.ref"
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
                                <td class="text-left">{{$t('indForm.noco')}}</td>
                                <td>
                                    <v-layout justify-center>
                                        {{tag.n_oco}}
                                    </v-layout>
                                </td>
                            </tr>
                        </tbody>
                    </template>
                  </v-simple-table>
                  <v-btn color="#c9302c" class="white--text" @click="emiteFecho">{{$t('indForm.close')}}</v-btn>
              </v-container>
          </v-form>
          </v-card-actions>
      </v-card>
  </div>
</template>

<script>

export default {
  data(){
    return{
      tag:{
        id:"",
        //ocorrencias:[],
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
      this.tag.id = this.passedData._id
      //this.tag.ocorrencias = this.passedData.ocorrencias
      this.tag.ref = this.passedData.ref
      this.tag.n_oco = this.passedData.n_ocorrencias
    },
    emiteFecho:function(){
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
