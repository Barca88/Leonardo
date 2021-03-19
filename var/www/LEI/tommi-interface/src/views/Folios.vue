<template>
  <div id="folios">
    <appHeader :ajuda="ajuda"></appHeader>
    <div v-if="this.$store.state.user.tipo === 'Admin'">
      <navDraw></navDraw>
    </div>
    <div v-else>
      <navDrawLeitor></navDrawLeitor>
    </div>
    <v-data-table
      id="tabelaFolios"
      :headers="headers"
      :items="folios"
      :items-per-page="15"
      :sort-by="['_id']"
      :search="search"
      multi-sort
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title
            ><b>{{ $t("fol.title") }}</b></v-toolbar-title
          >
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            :label="`${$t('navd.se')}`"
            single-line
            hide-details
            class="mr-5"
          ></v-text-field>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                v-if="$store.state.user.tipo === 'Admin'"
                link
                to="/admin/import"
                color="#2A3F54"
                dark
                v-on="{ ...tooltip }"
                class="mr-5"
              >
                <v-icon>mdi-text-box-plus</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("fol.insert") }}
            </span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                link
                color="#2A3F54"
                dark
                v-on="{ ...tooltip }"
                @click="printSection"
              >
                <v-icon>mdi-printer</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("fol.print") }}
            </span>
          </v-tooltip>

          <v-dialog persistent v-model="dialog" max-width="500px">
            <folioForm
              :passedData="item"
              @emiteFecho="emiteFecho($event)"
            ></folioForm>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:header._id="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.descricao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.versao="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.sumario="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.tipo="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:header.options="{ header }">
        <label> {{ header.text }} </label>
      </template>
      <template v-slot:item.options="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-eye </v-icon>
        <v-icon small class="mr-2" @click="verFolioFoto(item)">
          mdi-camera
        </v-icon>
        <v-icon
          v-if="$store.state.user.tipo === 'Admin'"
          small
          @click="
            deleteDialog = true;
            tempValue = item;
          "
        >
          mdi-trash-can
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="picDialog" width="800px">
      <v-card>
        <v-img v-bind:src="folioPic" contain aspect-ratio="1.5" />
      </v-card>
      <v-tooltip bottom>
        <template v-slot:activator="{ on: tooltip }">
          <v-btn
            color="#c9302c"
            dark
            @click="picDialog = false"
            v-on="{ ...tooltip }"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </template>
        <span>
          {{ $t("indForm.close") }}
        </span>
      </v-tooltip>
    </v-dialog>
    <v-dialog v-model="noPicDialog" width="500px">
      <v-card>
        <v-toolbar color="#2A3F54" dark>
          <h2>{{ $t("fol.title") }}</h2>
        </v-toolbar>
        <v-row>
          <v-col
            style="
              margin-left: 1cm;
              margin-right: 1cm;
              max-width: 20px;
              margin-top: 15px;
            "
          >
            <v-icon x-large color="blue" dark>mdi-message-text</v-icon>
          </v-col>
          <v-col>
            <v-card-text>
              <h3>{{ $t("fol.noPicText") }}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="noPicDialog = false" v-on="{ ...tooltip }">
                <v-icon>mdi-exit-to-app</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("indForm.close") }}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="deleteDialog" scrollable width="500" persistent>
      <v-card>
        <v-toolbar color="#2A3F54" dark>
          <h2>{{ $t("fol.title") }}</h2>
        </v-toolbar>
        <v-row>
          <v-col
            style="
              margin-left: 1cm;
              margin-right: 1cm;
              max-width: 20px;
              margin-top: 15px;
            "
          >
            <v-icon x-large color="#9e8f4b" dark>mdi-message-alert</v-icon>
          </v-col>
          <v-col>
            <v-card-text>
              <h3>{{ $t("fol.elim") }}</h3>
            </v-card-text>
          </v-col>
        </v-row>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                class="mr-5"
                @click="
                  deleteDialog = false;
                  deleteItem(tempValue);
                "
                v-on="{ ...tooltip }"
              >
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("navd.confirm") }}
            </span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn @click="deleteDialog = false" v-on="{ ...tooltip }">
                <v-icon>mdi-exit-to-app</v-icon>
              </v-btn>
            </template>
            <span>
              {{ $t("navd.nao") }}
            </span>
          </v-tooltip>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import axios from "axios";
import Header from "../components/header.vue";
import NavDraw from "../components/navDraw.vue";
import navDrawLeitor from "../components/navDrawLeitor.vue";
import FolioForm from "../components/folioForm.vue";
export default {
  data() {
    return {
      headers: [
        {
          text: `${this.$t("fol.id")}`,
          align: "start",
          value: "_id",
        },
        {
          text: `${this.$t("fol.desc")}`,
          value: "descricao",
        },
        {
          text: `${this.$t("fol.versao")}`,
          value: "versao",
        },
        {
          text: `${this.$t("fol.sum")}`,
          value: "sumario",
        },
        {
          text: `${this.$t("fol.tipo")}`,
          value: "tipo",
        },
        {
          text: `${this.$t("fol.opt")}`,
          value: "options",
          sortable: false,
        },
      ],
      search: "",
      ajuda: "folios",
      ver: "ver",
      folios: [],
      errors: [],
      folioPic: "",
      dialog: false,
      picDialog: false,
      noPicDialog: false,
      deleteDialog: false,
      tempValue: "",
      item: {},
    };
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
  },
  components: {
    appHeader: Header,
    navDraw: NavDraw,
    navDrawLeitor: navDrawLeitor,
    folioForm: FolioForm,
  },
  created() {
    axios
      .get(
        `https://tommi2.di.uminho.pt/api/folios/folios?nome=${this.$store.state.user._id}`,
        {
          headers: {
            Authorization: `Bearer: ${this.$store.state.jwt}`,
          },
        }
      )
      .then((response) => {
        // JSON responses are automatically parsed.
        //console.log(response.data)
        this.folios = response.data.folios;
      })
      .catch((e) => {
        //console.log(e)
        this.errors.push(e);
      });
  },
  methods: {
    printSection() {
      // Pass the element id here
      this.$htmlToPaper("tabelaFolios");
    },
    editItem(item) {
      this.item = item;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
      this.item = {};
    },
    deleteItem(item) {
      const index = this.folios.indexOf(item);
      //console.log('Index: ' + index + ' folioname: ' + this.folios[index]._id)
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/folios/apagar/` +
            this.folios[index]._id +
            `?nome=${this.$store.state.user._id}`,
          {
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          //console.log(response.data)
          this.folios = response.data.folios;
          this.tempValue = {};
        })
        .catch((e) => {
          //console.log(e)
          this.errors.push(e);
        });
    },
    emiteFecho: function () {
      this.dialog = false;
    },
    verFolioFoto: function (item) {
      const index = this.folios.indexOf(item);
      axios
        .get(
          `https://tommi2.di.uminho.pt/api/folios/ver/${this.folios[index]._id}/foto`,
          {
            responseType: "arraybuffer",
            headers: {
              Authorization: `Bearer: ${this.$store.state.jwt}`,
            },
          }
        )
        .then((response) => {
          var image = new Buffer(response.data, "binary").toString("base64");
          this.folioPic = `data:${response.headers[
            "content-type"
          ].toLowerCase()};base64,${image}`;
          this.picDialog = true;
        })
        .catch((e) => {
          this.noPicDialog = true;
          //console.log(e)
          this.errors.push(e);
        });
    },
  },
};
</script>
<style scoped>
@media print {
  body {
    overflow: auto;
    height: auto;
  }
  .page-break {
    display: block;
    page-break-before: always;
  }
}
/* .tommitable .v-data-table .table{ */
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
#folios * {
  box-sizing: border-box;
}
#folios {
  margin: 20px auto;
  max-width: 1100px;
  margin-bottom: 80px;
}
label {
  color: white;
  padding: 8px;
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 15px;
}
b {
  font-size: 20px;
}
</style>
