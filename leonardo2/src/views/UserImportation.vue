<template>
<div id="usersImport">
    <appHeader></appHeader>
    <navDraw></navDraw>
    <v-container class="pa-10">
        <h4 class="text-h4 mb-4">
            Importação de Dados de Utilizador
        </h4>

        <v-container>
            <v-row no-gutters align="center" justify>
                <v-col cols="12" sm="2" md="1">
                    <span>
                        Ficheiro:
                    </span>
                </v-col>
                <v-col cols="12" sm="5">

                    <v-file-input truncate-length="150" show-size v-model="file" :clearable="false" label="<Ficheiro.csv>"></v-file-input>
                </v-col>

            </v-row>
            <v-row no-gutters>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn v-on="{ ...tooltip}" @click="loadCSV($event)" class="mr-5" dark color="amber lighten">
                            <v-icon>mdi-checkbox-marked-outline</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        Confirmar
                    </span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn v-on="{ ...tooltip}" @click="file='', parse_csv =[] , parse_header=[], selected=[]" class="mr-5" dark color="green accent-3">
                            <v-icon>mdi-broom</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        Limpar
                    </span>
                </v-tooltip>
                <v-tooltip bottom>
                    <template v-slot:activator="{ on: tooltip }">
                        <v-btn v-on="{ ...tooltip}" class="mr-5" dark color="blue-grey darken-4">
                            <v-icon>mdi-help</v-icon>
                        </v-btn>
                    </template>
                    <span>
                        Ajuda
                    </span>
                </v-tooltip>
            </v-row>

        </v-container>

    </v-container>

    <template>
        <v-row justify="center">
            <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                    <v-data-table v-model="selected" show-select @click:row="handleClick" :headers="headersTable" item-key="Nome" :items="parse_csv" :items-per-page="5" class="elevation-1"></v-data-table>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="close()">
                            Close
                        </v-btn>
                        <v-btn color="blue darken-1" text @click="dialog=false, onFileChanged()">
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card>

            </v-dialog>
        </v-row>
    </template>

    <v-snackbar v-model="snackbar" timeout="-1">
        Pedidos de Utilizadores adicionados com sucesso

        <template v-slot:action="{ attrs }">

            <v-btn color="green" text v-bind="attrs" @click="snackbar = false; $router.push('/pedidos')">
                Continuar
            </v-btn>
            <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
                Fechar
            </v-btn>
        </template>
    </v-snackbar>
</div>
</template>

<script>
import axios from 'axios'
import Header from '../components/header.vue'
import NavDraw from '../components/navDraw.vue'
export default {
    data() {
        return {
            channel_name: '',
            channel_fields: [],
            channel_entries: [],
            parse_header: [],
            parse_csv: [],
            sortOrders: {},
            sortKey: '',
            active: [],
            selected: [],
            dialog: false,
            headersTable: [{
                    text: 'Nome',
                    align: 'start',
                    sortable: false,
                    value: 'Nome',
                },
                {
                    text: 'Género',
                    value: 'Género'
                },
                {
                    text: 'Identificador',
                    value: 'Identificador'
                },
                {
                    text: 'Domínio',
                    value: 'Domínio'
                },
                {
                    text: 'Instituição',
                    value: 'Instituição'
                },
                {
                    text: 'Curso',
                    value: 'Curso'
                },
                {
                    text: 'Disciplina',
                    value: 'Disciplina'
                },
                {
                    text: 'eMail',
                    value: 'eMail'
                },
                {
                    text: 'Tipo',
                    value: 'Tipo'
                },
                {
                    text: 'Validade',
                    value: 'Validade'
                }

            ],
            headers: [{
                    text: `${this.$t('users.nome')}`,
                    value: '_id'
                },
                {
                    text: `${this.$t('hist.adate')}`,
                    value: 'stamp'
                }
            ],
            file: "",
            snackbar: false
        }
    },
    components: {
        'appHeader': Header,
        'navDraw': NavDraw
    },
    filters: {
        capitalize: function (str) {
            return str.charAt(0).toUpperCase() + str.slice(1)
        }
    },
    methods: {
        close() {
            
            this.dialog = false
        },
        onFileChanged() {
            
            this.selectedFile = this.selected
            var jsonUsers = JSON.stringify(this.selectedFile)
            // console.log(this.file)
            if(this.selectedFile != null){
                let formData = new FormData()
                formData.append('newUsers', jsonUsers)
                axios.post(`${process.env.VUE_APP_BACKEND}/users/import_registos`, formData, {
                    responseType: 'arraybuffer',
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        Authorization: `Bearer: ${this.$store.state.jwt}`
                    }
                }).then(() => {
                    this.snackbar = true
                }).catch(e => {
                    this.errors.push(e)
                })}
        },

        sortBy: function (key) {
            var vm = this
            vm.sortKey = key
            vm.sortOrders[key] = vm.sortOrders[key] * -1
        },
        csvJSON(csv) {
            var vm = this
            var lines = csv.split("\n")
            var result = []
            var headers = lines[0].split(";")
            vm.parse_header = lines[0].split(";")
            lines[0].split(";").forEach(function (key) {
                vm.sortOrders[key] = 1
            })

            lines.map(function (line, indexLine) {
                if (indexLine < 1) return // Jump header line

                var obj = {}
                var currentline = line.split(";")

                headers.map(function (header, indexHeader) {
                    obj[header] = currentline[indexHeader]
                })

                result.push(obj)
            })

            result.pop() // remove the last item because undefined values

            return result // JavaScript object
        },
        loadCSV() {
            var vm = this
            if (window.FileReader) {
                var reader = new FileReader();
                reader.readAsText(this.file);
                // Handle errors load
                reader.onload = function (event) {
                    var csv = event.target.result;
                    vm.parse_csv = vm.csvJSON(csv)

                };
                reader.onerror = function (evt) {
                    if (evt.target.error.name == "NotReadableError") {
                        alert("Canno't read file !");
                    }
                };
                this.dialog = true
            } else {
                alert('FileReader are not supported in this browser.');
            }
        }
    },

    //Active
    created: function () {
        axios.get(`${process.env.VUE_APP_BACKEND}/users/active?nome=${this.$store.state.user._id}`, {
                headers: {
                    Authorization: `Bearer: ${this.$store.state.jwt}`
                }
            })
            .then(response => {
                this.active = response.data.users

            }).catch(e => {
                this.errors.push(e)
            })
    }
}
</script>

<style scoped>
.v-data-table /deep/ th {
    background-color: #4b779e;
}

.v-data-table /deep/ tr {
    color: #73879C;
    font-size: 13px;
}

.v-data-table /deep/ tr:nth-child(even) {
    background-color: rgb(245, 245, 245);
}

label {
    color: white;
    padding: 8px;
    font-family: Arial, sans-serif;
    font-weight: bold;
    font-size: 15px;
}

.container {
    margin: 20px auto 80px auto;
    max-width: 1100px;
}
</style>
